import asyncio
import json
import aiohttp
import aiofiles
import pyodbc

from base_url import (get_urls_df as base_get_urls_df,
                      load_site_map as base_load_site_map)
from products_url import (get_urls_df as prod_get_urls_df,
                          load_site_map as prod_load_site_map)
from sqlalchemy import create_engine

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pj = "products.json"
    sm_file = "sitemap.xml"
    sites = ["https://blazedvapes.com"]
    #for site in sites:
    url = sites[0]
    sitemap = base_load_site_map(url, sm_file)
    urls = base_get_urls_df(sitemap)
    # for sitemap_url in urls.itteritems():
    sm_url = urls.loc[0]["url"]
    smp1_sitemap = prod_load_site_map(sm_url)
    smp1_urls = prod_get_urls_df(smp1_sitemap)
    # for prod_url in smp1_urls.itteritems():
    prod_url = smp1_urls.loc[0]["url"]
    col_url = urls.loc[3]["url"]
    col_sitemap = prod_load_site_map(col_url)
    col_urls = prod_get_urls_df(col_sitemap)
    # for prod_url in smp1_urls.itteritems():
    col_url = col_urls.loc[0]["url"]



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
