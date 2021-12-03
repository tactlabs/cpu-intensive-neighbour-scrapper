from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options
import time
import os
from fake_useragent import UserAgent
import requests
import json
from  bs4 import BeautifulSoup
from datetime import datetime
from pprint import pprint
import pandas as pd
import csv
from selenium.webdriver.common.by import By


load_dotenv()

DRIVER_PATH = os.environ.get('DRIVER_PATH')
chrome_options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
chrome_options.add_argument(f'user-agent={userAgent}')
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

# user_agent = 'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'

chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(options=chrome_options, executable_path=DRIVER_PATH)

total_links_list = []

try:
    os.mkdir(os.path.join(os.getcwd(), 'images'))
    with open('info.csv', 'w'):
        pass
except Exception as e:
    print(e)
    pass



def id_count():
    count = 1
    # f = open('info.json',)
    # data = json.load(f)
    # try:
    #     for i in data['pages']:
    #         if i['id']:
    #             count +=1    
    try:
        df = pd.read_csv('info.csv', usecols = ['id'] )
        temp = df.to_dict()
        for val in temp['id'].values():
            # print(val)
            if val:
                # print("in if")
                count +=1
        # print(count)
        return count
    except Exception as e:
        print(e)
        return 1


def get_scraped_links():
    
    # f = open('info.json',)
    # data = json.load(f)
    # try:
    #     for i in data['pages']:
    #         total_links_list.append(i['url']) 
    # except Exception as e:
    # print(e)

    #     pass
    try:
        df = pd.read_csv('info.csv',usecols = ['url'])
        temp = df.to_dict()
        for val in temp['url'].values():
            total_links_list.append(val)
    except Exception as e:
        print(e)
        pass
        



def get_price(link):

    price_dict = {}

    time.sleep(3)

    driver.get(link)

    time.sleep(5) 


    try:
        subtotal = driver.find_element(By.XPATH,'//*[@id="default_reserve_card_subtotal"]/div').text
    except Exception as e:
        print(e)
        subtotal = "None"
    # print(subtotal)                            //*[@id="default_reserve_card_subtotal"]/div/p

    try:
        
        try:
            service_tax = driver.find_element(By.XPATH,'//*[@id="reserve"]/div/div[3]/div[1]/div/div[2]/span/div/p[1]').text
        except Exception as e:
            print(e)

            service_tax = driver.find_element(By.XPATH,'//*[@id="reserve"]/div/div[2]/div[1]/div/div[2]/span/div/p').text
    except Exception as e:
        print(e)
        service_tax = "None"
    # print(service_tax)

    try:
        
        try:
            total = driver.find_element(By.XPATH,'//*[@id="reserve"]/div/div[2]/div[2]/div[1]/p[2]').text
        except Exception as e:
            print(e)

            total = driver.find_element(By.XPATH,'//*[@id="reserve"]/div/div[3]/div[2]/span/div/span').text
    except Exception as e:
        print(e)
        total = "None"
        

    price_dict['subtotal'] = subtotal
    price_dict['service tax'] = service_tax
    price_dict['total'] = total

    return price_dict

def description():
    # driver.get('https://www.neighbor.com/listings/texas/winters/175079')

    html = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(html,"html.parser")
    specs = {}
    keys =['Size','Height','Storage Type','Access','Hours']
    
    data = soup.select('div.d-flex.flex-column-reverse.flex-md-column.w-100')
    if not (data):
        return

    # specs_list = []
    i=1

    for values in data:
        for p in values.select('p'):
            if i%2 == 1:
                specs[p.get_text()] = ''
                prev = p

            else:
                try:
                    val = p.get_text().replace('\xa0', '')
                    specs[prev.get_text()] = val
                except Exception as e:
                    print(e)
        
                    specs[prev.get_text()] = p.get_text()

            i+=1
    try:
        for key in keys:
            if key not in specs:
                # print(key)
                # print(keys.index(key))
                spec_list = list(specs.items())
                spec_list.insert(keys.index(key),(key,'None'))
                spec_dict=dict(spec_list)
        # print(spec_dict)
        return spec_dict

    except Exception as e:
        print(e)
        # print(specs)
        return specs

    # if 'Height' in specs and "Hours" in specs:
    #     return specs
    # elif "Height" not in specs or "Hours" not in specs:
    #     spec_list = list(specs.items())

    #     if 'Height' not in specs:
    #         spec_list.insert(1,('Height','None'))
    #     # print(dict(spec_list))
    #         spec_dict = dict(spec_list)
    #     # return spec_dict

    #     elif 'Hours' not in specs:
    #         spec_list.insert(4,('Hours',"None"))
    #         spec_dict=dict(spec_list)

    #     return spec_dict

    # elif "Height" not in specs and "Hours" not in specs:

    #     spec_list = list(specs.items())
    #     spec_list.insert(1,('Height','None'))
    #     spec_list.insert(4,('Hours',"None"))
    #     spec_dict = dict(spec_list)

    #     return spec_dict
        
    # print(specs)

    
    


def get_info1(link,price,images,count):

    info_dict = {}

    # price = get_price()

    time.sleep(3)    

    try:
        title = driver.find_element(By.XPATH,'//*[@id="root"]/div/div[4]/div/div/div/div/div/div/div[1]/div[1]/div[2]/div[1]/h2').text
    except Exception as e:
        print(e)
        title = "None"
    # print(title)                        

    specs = description()

    size = driver.find_element(By.XPATH,'//*[@id="root"]/div/div[4]/div/div/div/div/div/div/div[1]/div[1]/div[2]/div[2]/div[1]/div/div[1]/div/p').text
    # print(size)

    storage = driver.find_element(By.XPATH,'//*[@id="root"]/div/div[4]/div/div/div/div/div/div/div[1]/div[1]/div[2]/div[2]/div[1]/div/div[2]/p[2]').text
    # print(storage)


    access =  driver.find_element(By.XPATH,'//*[@id="root"]/div/div[4]/div/div/div/div/div/div/div[1]/div[1]/div[2]/div[2]/div[1]/div/div[3]/div[1]/p[2]').text
    # print(access)
                                        

    hours = driver.find_element(By.XPATH,'//*[@id="root"]/div/div[4]/div/div/div/div/div/div/div[1]/div[1]/div[2]/div[2]/div[1]/div/div[4]/div[1]/div/p').text
    # print(hours)
    try:                    
        host = driver.find_element(By.XPATH,'//*[@id="root"]/div/div[4]/div/div/div/div/div/div/div[1]/div[1]/div[2]/div[1]/div/span').text
    except Exception as e:
        print(e)
        host = "None"
    # print(host)

    try:
        summary = driver.find_element(By.XPATH,'//*[@id="root"]/div/div[4]/div/div/div/div/div/div/div[1]/div[1]/div[2]/div[3]/p[2]').text
    except Exception as e:
        print(e)
        summary = "None"

    try:
        location = driver.find_element(By.XPATH,'//*[@id="root"]/div/div[4]/div/div/div/div/div/div/div[1]/div[1]/div[3]/div[2]/p[3]/a').text
    except Exception as e:
        print(e)
        location = "None"
    # print(summary)

    # images = driver.find_elements_by(By.CLASS_NAME"listing-img listing-img-large w-100 h-100")
    # for image in images:
    #     image_link = image.get_attribute('src')
    #     print(image_link)
    
    
    images_dic=','.join(images)

    info_dict['id'] = count
    info_dict['url'] = link
    info_dict['host'] = host
    info_dict['title'] = title
    # info_dict['price'] = price
    # info_dict['specs'] = specs
    info_dict.update(price)
    info_dict.update(specs)

    info_dict['location'] = location
    info_dict['summary'] = summary
    info_dict['images'] = [images_dic]
    # info_dict.update(images)

    print(info_dict)


    # with open("info.json", "r") as file:
    #     data = json.load(file)

    #     try:
    #         data['pages'].append(info_dict)
    #         # data['user'].append(listing)
    #     except Exception as e

# print(e)    #         data = {
    #                 "pages" : [info_dict],
    #                 # "user" : [listing]
    #             }
                

    # with open("info.json", "w") as file:
    #         json.dump(data, file, indent=4)

    df = pd.DataFrame.from_dict(info_dict)
    if os.stat("info.csv").st_size == 0:
        df.to_csv('info.csv', mode='a', index=False, header=True)
    else:
        df.to_csv('info.csv', mode='a', index=False, header=False)
    # ['id','url','host','title','subtotal','service tax','total','Size','Storage Type','Access','Hours','height','summary','images'])


    # return info_dict

# def is_empty_csv():
#     with open('info.json') as csvfile:
#         reader = csv.reader(csvfile)
#         for i, _ in enumerate(reader):
#             if i:  # found the second row
#                 return False
#     return True

def get_images():

    image_list = []
    # driver.get('https://www.neighbor.com/listings/texas/san-leon/159415')
    image_links=[]

    try:
        images=driver.find_elements(By.XPATH,"//img[@class='listing-img listing-img-large w-100 h-100']")
        for image in images:
            link=image.get_attribute('src')

            image_links.append(link)

        for link in image_links:
            name = link.split('/')[-1] 

            with open("images/"+name,'wb') as f:

                im = requests.get(link)
                f.write(im.content)

            image_list.append("images/"+name)

        # print(image_list)

        return image_list

    except Exception as e:
        print(e)
        return "None"

    
def get_info2(link,price,images,count):

    info_dict = {}

    specs = {}

    # price = get_price(link)

    time.sleep(5)

    try:
        size = driver.find_element(By.XPATH,'//*[@id="root"]/div/div[4]/div/div/div/div/div/div/div[1]/div[1]/div[2]/div[1]/div').text
    except Exception as e:
        print(e)
        size = "None"

    try:
        access = driver.find_element(By.XPATH,'//*[@id="root"]/div/div[4]/div/div/div/div/div/div/div[1]/div[1]/div[3]/div/div[1]/div[1]/p[1]').text
    except Exception as e:
        print(e)
        access = "None"

    try:
        location = driver.find_element(By.XPATH,'//*[@id="root"]/div/div[4]/div/div/div/div/div/div/div[1]/div[1]/div[2]/div[2]/div/p').text
    except Exception as e:
        print(e)
        location = "None"

    try:
        time.sleep(3)                        
        host = driver.find_element(By.XPATH,'//*[@id="root"]/div/div[4]/div/div/div/div/div/div/div[1]/div[1]/div[6]/div/a/div/div/div/p')
            # driver.execute_script("arguments[0].scrollIntoView(true);",host)
        host.location_once_scrolled_into_view

        host_text = host.text
    except Exception as e:
        print(e)

        host_text = "None"
    
    try:
        summary = driver.find_element(By.XPATH,'//*[@id="root"]/div/div[4]/div/div/div/div/div/div/div[1]/div[1]/div[4]/p').text
    except Exception as e:
        print(e)
        summary = "None"

    try:
        hours = driver.find_element(By.XPATH,'//*[@id="root"]/div/div[4]/div/div/div/div/div/div/div[1]/div[1]/div[3]/div/div[1]/div[1]/p[2]').text
    except Exception as e:
        print(e)
        hours = "None"

    try:
        height = driver.find_element(By.XPATH,'//*[@id="root"]/div/div[4]/div/div/div/div/div/div/div[1]/div[1]/div[2]/div[1]/div[2]/p').text
    except Exception as e:
        print(e)
        height = "None"
   


    # count = id_count()

    images_dic=','.join(images)

    specs['size'] = size
    specs['height'] = height
    specs['Storage Type'] = size
    specs['access'] = access   
    specs['Hours'] = hours

    info_dict['id'] = count
    info_dict['url'] = link
    info_dict['host'] = host_text
    info_dict['title'] = size
    # info_dict['price'] = price
    # info_dict['specs'] = specs
    info_dict.update(price)
    info_dict.update(specs)

    info_dict['location'] = location
    info_dict['summary'] = summary
    info_dict['images'] = [images_dic]

    print(info_dict)

    # with open("info.json", "r") as file:
    #     data = json.load(file)

    #     try:
    #         data['pages'].append(info_dict)
    #         # data['user'].append(listing)
    #     except Exception as e:
    # print(e)

    #         data = {
    #                 "pages" : [info_dict],
    #                 # "user" : [listing]
    #             }
                

    # with open("info.json", "w") as file:
    #         json.dump(data, file, indent=4)

    # return info_dict

    df = pd.DataFrame.from_dict(info_dict)
    # var = is_empty_csv()
    if os.stat("info.csv").st_size == 0:
        df.to_csv('info.csv', mode='a', index=False, header=True)
    else:
        df.to_csv('info.csv', mode='a', index=False, header=False)
    
    # ['id','url','host','title','subtotal','service tax','total','Size','Storage Type','Access','Hours','height','location','summary','images'])


def run():

    links = get_links()


    get_scraped_links()

    for link in links:
        
        if link not in total_links_list:
            count = id_count()
            price = get_price(link)
            images = get_images()
            # get_info1(link)

            try: 
                get_info1(link,price,images, count)

            except Exception as e:
                print(e)
    
                get_info2(link,price,images, count)
        else:
            print("link already scraped")



def get_links():

    link_list = []

    final_list = []

    while True:

        try:

            time.sleep(3)
            div = driver.find_element(By.ID,"search_listing_cards")
            a_tags = div.find_elements(By.CLASS_NAME,"card-body-container")
            more = driver.find_element(By.ID,"rentals_search_show_more")
            # more = driver.find_element(By.CLASS_NAME,"sc-pFZIQ.gbgfMs.inner")
            more.click()

            print("getting links...")

            for a_tag in a_tags:
                # print(a_tag.text)
                link = a_tag.get_attribute("href")
                # print(link)
                link_list.append(link)    
            time.sleep(2)
        except Exception as e:
            print(e)

            break

    for link in link_list:
        if link not in final_list:
            final_list.append(link)

        
    return final_list

def trying(res):

    time.sleep(3)
    
    soup = BeautifulSoup(res.content,'html.parser')
    divs = soup.find('div', class_ = "d-flex flex-column-reverse flex-md-column w-100")

    print(divs.text)

def cities():

    # cities_list=['New York','Chicago','Miami','Dallas','Toronto','Montreal','Vancouver','Ottawa','Quebec City']

    # for city in cities_list:
    driver.get('https://www.neighbor.com/')
    time.sleep(3)
    search = driver.find_element(By.ID,"splash-search-input")
    search.send_keys("texas")
    search.send_keys(Keys.RETURN)
    run()


def startpy():
    driver.get("https://www.neighbor.com/")
    
    # driver.maximize_window()
    
    # column_names=['city','city_ascii']
    # df= pd.read_csv('uscities.csv',names=column_names)
    
    # cities=df.city.to_list()


    # get_links()

    cities()    
    
    # get_images()
    
if __name__ == '__main__':
    
    startpy()
    # id_count()
    # description()
    