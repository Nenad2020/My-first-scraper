# imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
import time
import csv
import re
from selenium.webdriver.common.keys import Keys


# *******************************
M_Links = []
Final_lst = []
# *******************************
def Loop():
    try:
        links = driver.find_elements_by_partial_link_text("")
        for link in links:
            link = link.get_attribute('href')
            if link is None:
                continue
            elif not link.endswith('#REVIEWS'):
                continue
            else:
                if link in M_Links:
                    continue
                else:
                    M_Links.append(link)
    except:
        print('\n')


# base setup of Selenium
win_size="1980,1080"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])

    #input for city.
print('*****_WELCOME_TO_TRIPADVISOR_RESTAURANT_SCRAPER*****\nIf you wish to exit program type QUIT when asked for city or number of pages.')
path=input('Please input your chromedriver.exe path here:')
while True:
    while True:
        city = input('Type name of the city,country: ')
        if city.isdigit():
            print('City is not a number')
            pass
        elif city.lower()=='quit':
            quit()
            print('Quiting...')
            break
        elif len(city)<2:
            print('Please enter full name of city...')
            pass
        else:
            break

    #input number of pages to scrape.
    while True:
        print('How many pages would you like to procces?\nIf you would like all, type ALL or number for certain amount')
        Num_pages =input('\nPages:')
        if Num_pages.lower()=='all':
            print('Number of pages set to ALL')
            Num_pages=10000
            break
        elif Num_pages.lower()=='quit':
            quit()
            break
        try:
            if int(Num_pages) < 0:
                print("Can't be negative number. Try again...")
                pass
            elif int(Num_pages) == 0 :
                print("It can't be zero. Try again...")
                pass
        except:
            print('Not a number. Try again...')
            pass
        if Num_pages.isdigit() and int(Num_pages)>0:
            print('Number of pages set to',Num_pages)
            Num_pages=int(Num_pages)
            break
        else:
            pass



    file_name=input('How would you like to call output file: ')
    print('\n*****Depending on the number of the restaurants in your chosen city, the process might take up to a few hours*****\nProcessing data...')
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % win_size)
    driver = webdriver.Chrome(path, options=chrome_options)
    driver.get('https://www.tripadvisor.com/')


    #**************************************************
    time.sleep(15)
    box=driver.find_element_by_name('q')
    box.send_keys(city)
    time.sleep(3)
    box.clear()
    box.send_keys(Keys.ARROW_DOWN)
    time.sleep(1)
    box.clear()
    box.send_keys(Keys.ENTER)
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="component_5"]/div/div/div/span[3]/div/a').click()#restaurant button
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="component_94"]/div/div[1]/div[2]/div[5]/span[1]').click()#expand,showmore
    time.sleep(5)
    filter_index=2
    #types of restaurants
    try:
        for i in range(10):
            i= filter_index + i
            driver.find_element_by_xpath('//*[@id="component_94"]/div/div[1]/div[2]/div['+str(i)+']/div/label').click()
            time.sleep(12)
    except:
        pass

    # now search for a links:
    if Num_pages==1:
        Loop()
        print(str(len(M_Links)),'restaurants found...')
        time.sleep(15)
        driver.close()

    elif Num_pages==2:
        Loop()
        print(str(len(M_Links)),'restaurants found...')
        time.sleep(15)
        driver.find_element_by_xpath(
        '/html/body/div[4]/div[3]/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[6]/div[3]/div[5]/div[2]/div/a[1]').click()
        time.sleep(15)
        Loop()
        print(str(len(M_Links)),'restaurants found...')
        driver.close()

    elif Num_pages>2:
        Mod_page=Num_pages-2
        Loop()
        print(str(len(M_Links)), 'restaurants found...')
        time.sleep(15)
        driver.find_element_by_xpath(
        '/html/body/div[4]/div[3]/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[6]/div[3]/div[5]/div[2]/div/a[1]').click()
        time.sleep(15)
        Loop()
        print(str(len(M_Links)), 'restaurants found...')
        time.sleep(15)
        try:
            for i in range(Mod_page):
                driver.find_element_by_xpath(
                    '/html/body/div[4]/div[3]/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[6]/div[3]/div[5]/div[2]/div/a[2]').click()
                time.sleep(15)
                Loop()
                print(str(len(M_Links)), 'restaurants found...')
                time.sleep(15)
            driver.close()
        except:
            time.sleep(5)
            driver.close()
    time.sleep(5)
    print('Link fetch complete!\nScanning for emails,names,telephone and locations...')
    num = len(M_Links)+1
    for each in M_Links:
        page = requests.get(each).text
        num = num - 1
        print(num, "remaining...")
        time.sleep(5)
        soup = BeautifulSoup(page, 'lxml')
        for tags in soup.find_all('a'):
            tag = str(tags)
            if not tag.startswith('<a href="mailto'):
                continue
            else:
                email = re.split('\:|\?', tag)[1]
                name = soup.find('h1').text
                try:
                    name = str(name)
                    name = name.split(',')[0]
                    try:
                        location=city.split(',')[0]
                    except:
                        location=city.capitalize()
                except:
                    pass
                try:
                    for tags in soup.find_all('a'):
                        tag = str(tags)
                        if not tag.startswith('<a href="tel:'):
                            continue
                        elif tag.startswith('<a href="tel:'):
                            phone = re.split('\:|"', tag)[2]
                            print('Email found with phone number.')
                        else:
                            phone='No Number'
                except:
                    print('Email found without phone number.')
            mytupple=(email,name,phone,location)
            Final_lst.append(mytupple)

    file_name=file_name+'.csv'
    with open(file_name, 'w') as new_file:
        csv_writer = csv.writer(new_file)
        for line in Final_lst:
            csv_writer.writerow(line)
    print('ALL DONE!')
    q_or_cont=input('If you wish to make another scrape type Contiue, or if you wish to exit type Quit\nType your choice: ')
    if q_or_cont.lower()=='quit':
        quit()
    else:
        pass
