import os
from sqlalchemy import create_engine

def write_file(path, content):
    with open(path, 'wb') as f:
        f.write(content)


def get_site_name(site):
    front_index = site.find("https://") + len("https://")
    back_index = site.find(".com")
    site_name = site[front_index:back_index]
    return site_name


# site = "https://blazedvapes.com/"
# file = "sitemap.xml"
# resp is the response from "https://blazedvapes.com/sitemap.xml"
def mk_sitemap_path(site, file, resp):
    site_name = get_site_name(site)
    path_to_sitemap = f'data\\sitemaps\\{site_name}'
    path_w_file = f'{path_to_sitemap}\\{file}'
    try:
        write_file(path_w_file, resp.content)
    except FileNotFoundError:
        os.mkdir(path_to_sitemap)
        write_file(path_w_file, resp.content)
    return path_w_file

# SQL Server Native Client 11.0
# ODBC Driver 17 for SQL Server
# SQL Server
def connect_to_db():
    #TODO: Find Out hot to connect to the db
    engine = create_engine("mssql+pyodbc://TNTDEV/ecig?driver=SQL Server Native Client 11.0?Trusted_Connection=yes")
    return engine