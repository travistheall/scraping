import os
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import re
import requests
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(executable_path=r"C:\Users\travi\PycharmProjects\SeleniumScraping\chromedriver.exe")
over24 =[]
letter = "a"
# for letter in letters:
driver.get('https://www.eliquid.com/pages/brand-navigation#' + str(letter))
time.sleep(5)
letterID = '//*[@id="' + str(letter).upper() + '"]/ul/li'
js_script = '''\
    document.getElementsByClassName('swelltab')[0].setAttribute("hidden","");
     '''
driver.execute_script(js_script)
brandsbyletter = driver.find_elements_by_xpath(letterID)
BrandLoop = 0
ProductLoop = 0
    # This loop looks at All the Brands that start with a letter.
    # We grab all the links cycle through them and click
for x in range(BrandLoop, len(brandsbyletter)):
    print(str(letter.upper()), " x loop ", x, " of ", len(brandsbyletter))
    element = driver.find_element_by_xpath(letterID + '[' + str(x + 1) + ']/a')
    element.click()
    time.sleep(3)
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
        driver.execute_script(js_script)
        titles = driver.find_elements_by_class_name('title')
        if len(titles) > 23:
            over24.append(titles[0].text)
        for y in range(len(titles)):
            img = driver.find_elements(By.XPATH, '//img')[7 + y]
            driver.execute_script("return arguments[0].scrollIntoView();", img)
            src = img.get_attribute('src')
            try:
                src1 = src[:src.index('?')]
            except ValueError:
                print('ValueError @ product: ', titles[y], ' y loop ', y, ' x loop ', x)
            file_ext = os.path.splitext(src1)[1]
            title = str(re.sub("[^0-9a-zA-Z ]",
                               "",
                               titles[y].text))
            brand = str(re.sub("[^0-9a-zA-Z ]",
                               "",
                               driver.find_element_by_xpath("/html/body/div[5]/div/div[2]/div[1]/h1").text))
            if title.count(' BY ') >= 1:
                flavor = str(re.sub("[^0-9a-zA-Z ]",
                                    "",
                                    title[:title.index(' BY')]))
                brand = str(re.sub("[^0-9a-zA-Z ]",
                                   "",
                                   title[(title.index(' BY') + 4):]))
                dirname = brand
                temp_filename = flavor + file_ext
                temp_filename_full_path = os.path.join('eliquids', letter, dirname, temp_filename)
            else:
                dirname = brand
                temp_filename = title + file_ext
                temp_filename_full_path = os.path.join('eliquids', letter, dirname, temp_filename)
            current_path = os.getcwd()
            path = os.path.join(current_path, 'eliquids', letter, dirname)
            if not os.path.exists(path):
                os.makedirs(path)
            response = requests.get(src1, stream=True)
            open(temp_filename_full_path, 'wb').write(response.content)

    driver.get('https://www.eliquid.com/pages/brand-navigation#' + str(letter))
    time.sleep(2)
    driver.execute_script(js_script)
    brandsbyletter = driver.find_elements_by_xpath(letterID)

