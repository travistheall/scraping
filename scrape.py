import os
import re
import requests
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import csv

driver = webdriver.Chrome(executable_path=r"C:\Users\travi\PycharmProjects\SeleniumScraping\chromedriver.exe")
this_dict = {}
# lettersToScrape = ["a", "b", "c",]
# for letter in lettersToScrape:
letter = "a"
letterScraped = str(letter)
letterID = '//*[@id="' + str(letter.upper()) + '"]/ul/li'
driver.get('https://www.eliquid.com/pages/brand-navigation#' + letterScraped)
time.sleep(5)
js_script = '''\
    document.getElementsByClassName('swelltab')[0].setAttribute("hidden","");
     '''
driver.execute_script(js_script)
brandsbyletter = driver.find_elements_by_xpath(letterID)
BrandLoop = 0
ProductLoop = 0
over24 = []
# This loop looks at All the Brands that start with a letter.
# We grab all the links cycle through them and click
for x in range(BrandLoop, len(brandsbyletter)):
    print("Line 22: BrandLoop = ", x)
    click1text = driver.find_elements_by_xpath(letterID)[x].text
    element = driver.find_element_by_xpath(letterID + '[' + str(x + 1) + ']/a')
    element.click()
    time.sleep(5)

    try:
        try:
            if driver.find_element_by_class_name('quote').text == 'No products found in this collection':
                pass
        except NoSuchElementException:
            if driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/h1').text == "WE'RE SORRY, BUT THE PAGE " \
                                                                                       "YOU REQUESTED COULD NOT " \
                                                                                       "BE FOUND.":
                pass

    except NoSuchElementException:
        links = driver.find_elements_by_class_name('hidden-product-link')
        for y in range(ProductLoop, len(links)):
            links = driver.find_elements_by_class_name('hidden-product-link')
            titles = driver.find_elements_by_class_name('title')
            if len(links) > 23:
                over24.append(titles[0].text)
            driver.find_elements_by_class_name('hidden-product-link')[y].click()
            time.sleep(3)
            print("Line 32: Opening product " + str(y) + " of Brand: ")
            time.sleep(3)
            title = driver.find_element_by_class_name('product_name').text
            picTitle = str(re.sub("[^0-9a-zA-Z ]",
                                  "",
                                  title))
            src = driver.find_elements(By.XPATH, '//img')[7].get_attribute('src')
            try:
                src1 = src[:src.index('?')]
            except ValueError:
                print('ValueError @ product: ', titles[y], ' y loop ', y, ' x loop ', x)
                src1 = src

            file_ext = os.path.splitext(src1)[1]
            current_path = os.getcwd()
            if title.count(' BY ') >= 1:
                brand = title[(title.index(' BY') + 4):]
                flavor = title[:title.index(' BY')]
                picFlavor = str(re.sub("[^0-9a-zA-Z ]",
                                       "",
                                       picTitle[:picTitle.index(' BY')]))
                picBrand = str(re.sub("[^0-9a-zA-Z ]",
                                      "",
                                      picTitle[(picTitle.index(' BY') + 4):]))
                dirname = brand
                temp_filename = flavor + file_ext
                temp_filename_full_path = os.path.join('eliquids', letter, dirname, temp_filename)
            else:
                brand = ''
                flavor = ''
                dirname = picTitle
                temp_filename = picTitle + file_ext
                temp_filename_full_path = os.path.join('eliquids', letter, dirname, temp_filename)

            path = os.path.join(current_path, 'eliquids', letter, dirname)
            if not os.path.exists(path):
                os.makedirs(path)
            response = requests.get(src1, stream=True)
            open(temp_filename_full_path, 'wb').write(response.content)

            prodtype = "E-Liquid"
            if title.count("SALT") or title.count("salt") >= 1:
                prodtype = "Salt"

            size = []
            strength = []
            ratio = []

            try:
                size_strength = driver.find_elements_by_class_name('swatch-element')
                for z in driver.find_elements_by_class_name('swatch-element'):
                    if z.text.count('ml') == 1 or z.text.count('ML') == 1:
                        size.append(z.text)
                    elif z.text.count('mg') == 1 or z.text.count('MG') == 1:
                        strength.append(z.text)
            except NoSuchElementException:
                pass

            try:
                vgpg = driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div/div[1]/div[2]/div[4]/p['
                                                    '2]/span[2]')
                if vgpg.text.count('VG') > 0:
                    ratio.append(vgpg.text)
            except NoSuchElementException:
                pass

            print("Line 70: Finished a brand/flavor", title)
            print("Brand: ", brand)
            print("Flavor: ", flavor)
            print("Type: ", prodtype)
            print("Size: ", size)
            print("Strength: ", strength)
            print("Ratio: ", ratio)
            this_dict[title] = {'brand': brand, 'flavor': flavor, 'type': prodtype, 'size': size, 'strength': strength,
                                'ratio': ratio}
            driver.back()
            time.sleep(3)

    driver.get('https://www.eliquid.com/pages/brand-navigation#' + letterScraped)
    print("Line 87: Sleeping 3 seconds to load Page")
    time.sleep(5)
    driver.execute_script(js_script)

try:
    with open('Vape.csv', 'w', newline='') as csvfile:
        fieldnames = ['title', 'brand', 'flavor', 'type', 'size', 'strength', 'ratio']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for x in this_dict:
            writer.writerow({'title': x,
                             'brand': this_dict[x]['brand'],
                             'flavor': this_dict[x]['flavor'],
                             'type': this_dict[x]['type'],
                             'size': this_dict[x]['size'],
                             'strength': this_dict[x]['strength'],
                             'ratio': this_dict[x]['ratio']})
except IOError:
    print("I/O error")
