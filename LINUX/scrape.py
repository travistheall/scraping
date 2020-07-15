from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import csv
import time
import pyautogui
driver = webdriver.Chrome(executable_path=r"/home/tnt/Downloads/chromedriver")
driver.get('https://www.eliquid.com/pages/brand-navigation')
this_dict = {}
print("Sleeping for 30s. Close dumb ads....")
time.sleep(30)
pyautogui.click(1913, 1449)
actions = ActionChains(driver)
brandsbyletter = driver.find_elements_by_xpath('//*[@id="A"]/ul/li')

for x in range(17, len(brandsbyletter)):
    print("Line 13: Entering into the X loop (All Brands Page)")
    # Currently on the Main page with all the different brands per letter
    print("Line 15: There are ", len(brandsbyletter), " brands on this page")
    click1text = driver.find_elements_by_xpath('//*[@id="M"]/ul/li')[x].text
    print("Line 17: sleeping for 1 seconds clicking on brand link number x: ", x, " named: ", click1text)
    element = driver.find_element_by_xpath('//*[@id="M"]/ul/li[' + str(x + 1) + ']/a')
    pyautogui.click(1913, 1449)
    pyautogui.hotkey('ctrl', 'f')
    pyautogui.click(2527, 238)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('backspace')
    pyautogui.typewrite(click1text)
    pyautogui.hotkey('enter')
    for x in range(3):
        pyautogui.click(3047, 1783)
    element.click()
    print("Line 19: Sleeping 10 seconds after click to load Brand Products Page")
    time.sleep(6)
    links = driver.find_elements_by_class_name('hidden-product-link')

    for y in range(len(links)):
        print("Line 24: Entering into the Y loop (Brand Products Page)")
        print("Line 25: There are ", len(links), " on this page. We are on number ", y)
        # Currently on the Brand page with all the different products per that bran
        titles = driver.find_elements_by_class_name('title')
        print("line 28: There should be ", len(links), " on this page with ", len(titles), " titles")
        print('line 30: clicking on product....', titles[y].text)
        driver.find_elements_by_class_name('hidden-product-link')[y].click()
        print("Line 32: Sleeping 10 seconds after click to load Brand Detail Page")
        time.sleep(6)
        title = driver.find_element_by_class_name('product_name').text
        if title.count('BY') >= 1:
            print("Line 35: Title: ", title)
            brand = title[(title.index(' BY') + 4):]
            print("line 37: Brand: ", brand)
            time.sleep(1)
            flavor = title[:title.index(' BY')]
            print("line 40: Flavor: ", flavor)
        else:
            brand = ''
            flavor = ''
        size = []
        strength = []
        ratio = []

        try:
            size_strength = driver.find_elements_by_class_name('swatch-element')
            for z in driver.find_elements_by_class_name('swatch-element'):
                if z.text.count('ml') == 1 or z.text.count('ML') == 1:
                    size.append(z.text)
                    print("Line 50: inside try block this is size ", size)
                elif z.text.count('mg') == 1 or z.text.count('MG') == 1:
                    strength.append(z.text)
                    print("Line 53: inside try block this is strength", strength)
        except NoSuchElementException:
            print("Line 55: Product is sold out No size strength data")

        try:
            for z in driver.find_elements_by_partial_link_text('VG'):
                ratio.append(z.text)
            print("line 59: Inside try block this is ratio: ", ratio)
        except NoSuchElementException:
            print("Line 61: There is no ratio information")

        print("Line 63: Finished a brand/flavor", title)
        print("Brand: ", brand)
        print("Flavor: ", flavor)
        print("Size: ", size)
        print("Strength: ", strength)
        print("Ratio: ", ratio)
        this_dict[title] = {'brand': brand, 'flavor': flavor, 'size': size, 'strength': strength, 'ratio': ratio}

        for line in this_dict:
            print("Line 72: Line in this_dict: ", line)

        print("Line 76: End of Y loop. Going back to Brand Products Page")
        driver.back()
        print("Line 78: End of Y loop. Sleeping before starting the whole Y loop over again")
        time.sleep(6)

    print("Line 83: We are going back to the All brands page now. We are in X loop")
    driver.back()
    print("Line 85: End of X loop. Sleeping before moving onto the next Brand Product Page in the list.")
    time.sleep(6)
    for x in range(50):
        pyautogui.click(3053, 217)
    pyautogui.click(517, 1454)
    print("Clicking on the correct Category Letter")

print("We have scraped all of the first page successfully. Fuck Yeah.")

try:
    with open('VapeNum.csv', 'w', newline='') as csvfile:
        fieldnames = ['title', 'brand', 'flavor', 'size', 'strength', 'ratio']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for x in this_dict:
            writer.writerow({'title': x,
                             'brand': this_dict[x]['brand'],
                             'flavor': this_dict[x]['flavor'],
                             'size': this_dict[x]['size'],
                             'strength': this_dict[x]['strength'],
                             'ratio': this_dict[x]['ratio']})
except IOError:
    print("I/O error")
