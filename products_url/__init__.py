import xml.etree.ElementTree as ET
import pandas as pd
import requests
from all_urls import get_site_name, mk_sitemap_path, connect_to_db
from sqlalchemy import create_engine

# https://blazedvapes.com/sitemap_products_1.xml?from=287200215070&to=6193489313967
def create_sitemap_products_file_name(url):
    file = url[url.find('.com/') + len('.com/'):]
    file = file[:file.find('?')]
    return file


# https://blazedvapes.com/sitemap_products_1.xml?from=287200215070&to=6193489313967
def load_site_map(url):
    site = get_site_name(url)
    file = create_sitemap_products_file_name(url)
    resp = requests.get(url)
    sitemap = mk_sitemap_path(site, file, resp)
    return sitemap


# sitemap_products_1.xml
def get_urls_df(sitemap):
    tree = ET.parse(sitemap)
    root = tree.getroot()
    urls = pd.DataFrame([x for x in root.itertext()])
    urls = urls.rename({0: "url"}, axis=1)
    urls = urls[urls["url"].str.startswith('https')]
    urls = urls[urls["url"].str.find('/files/') == -1]
    urls = urls.reset_index()
    urls = urls.drop(labels='index', axis=1)
    urls = urls.drop(labels=0, axis=0)
    urls = urls.reset_index()
    urls = urls.drop(labels='index', axis=1)
    urls["url"] += '/products.json'
    return urls


def create_products(url):
    engine = create_engine("mssql+pyodbc://TNTDEV/ecig?driver=SQL Server Native Client 11.0?Trusted_Connection=yes")
    df = pd.DataFrame(requests.get(url).json())
    df = pd.json_normalize(df['products'])
    prod_df = df[["id", "title", "handle", "published_at", "created_at", "updated_at", "vendor", "product_type", "body_html"]]
    prod_df["id"] = prod_df["id"].astype(str)
    prod_df["title"] = prod_df["title"].astype(str)
    prod_df["handle"] = prod_df["handle"].astype(str)
    prod_df["published_at"] = pd.to_datetime(prod_df["published_at"])
    prod_df["created_at"] = pd.to_datetime(prod_df["created_at"])
    prod_df["updated_at"] = pd.to_datetime(prod_df["updated_at"])
    prod_df["vendor"] = prod_df["vendor"].astype(str)
    prod_df["product_type"] = prod_df["product_type"].astype(str)
    prod_df["body_html"] = prod_df["body_html"].astype(str)
    prod_df.set_index('id', inplace=True)
    prod_df.to_sql('product', con=engine, if_exists="append")


import pyodbc

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=TNTDEV;'
                      'Database=ecig;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()


#def create_images(prod_url):
engine = create_engine("mssql+pyodbc://TNTDEV/ecig?driver=SQL Server Native Client 11.0?Trusted_Connection=yes")
df = pd.DataFrame(requests.get(col_url).json())
prod_df = pd.json_normalize(df['products'])
prod_df = prod_df[["id", "images"]]
prod_df = pd.json_normalize(prod_df['images'].str)
# TODO: Fix this
# prod_df.drop("variant_ids", axis=1, inplace=True)
prod_df["id"] = prod_df["id"].astype(str)
prod_df["product_id"] = prod_df["product_id"].astype(str)
prod_df.rename({"product_id": "product"}, axis=1, inplace=True)
prod_df["position"] = prod_df["position"].astype(int)
prod_df["created_at"] = pd.to_datetime(prod_df["created_at"])
prod_df["updated_at"] = pd.to_datetime(prod_df["updated_at"])
prod_df["alt"] = prod_df["alt"].astype(str)
prod_df["src"] = prod_df["src"].astype(str)
prod_df["width"] = prod_df["width"].astype(int)
prod_df["height"] = prod_df["height"].astype(int)
prod_df = prod_df[["product", "id", "created_at", "position", "updated_at", "src", "width", "height", "alt"]]
prod_df.set_index('id', inplace=True)
prod_df.to_sql('image', con=engine, if_exists="append")


#def create_images(prod_url):
engine = connect_to_db()
df = pd.DataFrame(requests.get(col_url).json())
prod_df = pd.json_normalize(df['products'])
#prod_df = df.T[["id", "variants"]]
prod_df = pd.json_normalize(prod_df['variants']['product'])
prod_df["id"] = prod_df["id"].astype(str)
prod_df["product_id"] = prod_df["product_id"].astype(str)
prod_df.rename({"product_id": "product"}, axis=1, inplace=True)
prod_df["position"] = prod_df["position"].astype(int)
prod_df["created_at"] = pd.to_datetime(prod_df["created_at"])
prod_df["updated_at"] = pd.to_datetime(prod_df["updated_at"])
prod_df["title"] = prod_df["title"].astype(str)
prod_df["option1"] = prod_df["option1"].astype(str)
prod_df["option2"] = prod_df["option2"].astype(str)
prod_df["option3"] = prod_df["option3"].astype(str)
prod_df["sku"] = prod_df["sku"].astype(str)
prod_df["requires_shipping"] = prod_df["requires_shipping"].astype(bool)
prod_df["taxable"] = prod_df["taxable"].astype(bool)
prod_df["available"] = prod_df["available"].astype(bool)
prod_df["price"] = prod_df["price"].astype(float)
prod_df["grams"] = prod_df["grams"].astype(int)
prod_df["compare_at"] = prod_df["compare_at"].astype(float)
prod_df = prod_df[["product","id","title","option1","option2","option3","sku","requires_shipping","taxable","available","price","grams","compare_at","position","created_at","updated_at"]]
prod_df.set_index('id', inplace=True)
prod_df.to_sql('variant', con=engine, if_exists="append")






def parse_json():
    pass
