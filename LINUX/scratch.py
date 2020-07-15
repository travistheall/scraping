for x in range(78, len(brandsbyletter)):
    print("Line 2: Entering into the X loop (All Brands Page)")
    # Currently on the Main page with all the different brands per letter
    print("Line 4: There are ", len(brandsbyletter), " brands on this page")
    click1text = driver.find_elements_by_xpath('//*[@id="C"]/ul/li')[x].text
    print("Line 6: sleeping for 1 seconds clicking on brand link number x: ", x, " named: ", click1text)
    element = driver.find_element_by_xpath('//*[@id="C"]/ul/li[' + str(x + 1) + ']/a')
    pyautogui.click(2197, 89)
    pyautogui.hotkey('ctrl', 'f')
    pyautogui.click(2197, 89)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('backspace')
    pyautogui.typewrite(click1text)
    pyautogui.hotkey('enter')
    for scrollDown in range(2):
        pyautogui.click(2549, 1390)
    element.click()
    print("Line 18: Sleeping 10 seconds after click to load Brand Products Page")
    time.sleep(6)
    links = driver.find_elements_by_class_name('hidden-product-link')
    linkslen = len(links)

    for y in range(23, linkslen):
        print("Line 23: Entering into the Y loop (Brand Products Page)")
        print("Line 24: There are ", len(links), " on this page. We are on number ", y)
        # Currently on the Brand page with all the different products per that brand
        titles = driver.find_elements_by_class_name('title')
        print("line 27: There should be ", len(links), " on this page with ", len(titles), " titles")
        print('line 29: clicking on product....', titles[y].text)
        if len(links) >= 23:
            if y == 23:
                linkslen += 1
            if y > 24:
                driver.find_element_by_class_name('load-more').click()
                pyautogui.click(330, 784)
                pyautogui.hotkey('down')
                time.sleep(3)
                links = driver.find_elements_by_class_name('hidden-product-link')
        driver.find_elements_by_class_name('hidden-product-link')[y].click()
        print("Line 32: Sleeping 10 seconds after click to load Brand Detail Page")
        time.sleep(5)
        title = driver.find_element_by_class_name('product_name').text
        if title.count(' BY') >= 1:
            print("Line 34: Title: ", title)
            brand = title[(title.index(' BY') + 4):]
            print("line 36: Brand: ", brand)
            flavor = title[:title.index(' BY')]
            print("line 38: Flavor: ", flavor)
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
                elif z.text.count('mg') == 1 or z.text.count('MG') == 1:
                    strength.append(z.text)
        except NoSuchElementException:
            pass

        try:
            for z in driver.find_elements_by_partial_link_text('VG'):
                ratio.append(z.text)
        except NoSuchElementException:
            pass

        print("Line 63: Finished a brand/flavor", title)
        print("Brand: ", brand)
        print("Flavor: ", flavor)
        print("Size: ", size)
        print("Strength: ", strength)
        print("Ratio: ", ratio)
        print("In loop X number: ", x)
        this_dict[title] = {'brand': brand, 'flavor': flavor, 'size': size, 'strength': strength, 'ratio': ratio}

        print("Line 76: End of Y loop. Going back to Brand Products Page")
        driver.back()
        print("Line 78: End of Y loop. Sleeping before starting the whole Y loop over again")
        time.sleep(3)

    print("Line 83: We are going back to the All brands page now. We are in X loop")
    driver.back()
    print("Line 85: End of X loop. Sleeping before moving onto the next Brand Product Page in the list.")
    for scrollUp in range(50):
        pyautogui.click(2551, 81)
    pyautogui.click(888, 754)
    print("Clicking on the correct Category Letter")