import xml.etree.ElementTree as ET
import pandas as pd
import requests
from all_urls import mk_sitemap_path


def load_site_map(site, file):
    url = site + "/" + file
    resp = requests.get(url)
    sitemap = mk_sitemap_path(site, file, resp)
    return sitemap

# sitemap = data\sitemaps\WEBSITE\sitemap.xml
def get_urls_df(sitemap):
    tree = ET.parse(sitemap)
    root = tree.getroot()
    urls = pd.DataFrame([x for x in root.itertext()])
    urls = urls.rename({0: "url"}, axis=1)
    urls = urls[urls["url"].str.startswith('https')]
    urls = urls.reset_index()
    urls = urls.drop(labels='index', axis=1)
    return urls
