from bs4 import BeautifulSoup as soup
from urllib.request import urlopen

"""
USE https://js-beautify.com/ to BEAUTIFY JAVASCRIPT TO MAKE IT MORE READABLE
"""
'''
----------------------- Newegg Playstation 5 dicount games webscraper ------------------------------------------------------------------
'''

# storing website destination as my_url variable
my_url = 'https://www.newegg.com/PS5-Video-Games/SubCategory/ID-3763?Tid=1696841'

# calls urlopen function from request function in urllib
# opens up connection and grabs the page
uClient = urlopen(my_url)

# reads and stores the raw html data into the variable page_html
page_html = uClient.read()
uClient.close()

# parses page
page_soup = soup(page_html, "html.parser")

# finds all "div" class:"item-container" and stores the data into the variable containers
# (grabs all products on page)
containers = page_soup.findAll("div", {"class" : "item-container"})

# Grabs number of pages
num_of_pages_search = page_soup.find('span', {'class': 'list-tool-pagination-text'})
num_of_pages_search_str = str(num_of_pages_search)
num_of_pages_count = 0
num_of_pages_str = ''
for num in num_of_pages_search_str:
    if num in '0123456789':
        num_of_pages_count += 1
        if num_of_pages_count > 1:
            num_of_pages_str += num

num_of_pages_int = int(num_of_pages_str)

'''
---------------------------------Starts loop after grabbing number of pages to collect data-----------------------------
'''
newegg_playstation5games_list = []
for num in range(num_of_pages_int):
    # calls urlopen function from request function in urllib
    # opens up connection and grabs the page
    num_of_pages_str = str(num + 1)
    my_url2 = my_url + '&page=' + num_of_pages_str
    uClient2 = urlopen(my_url2)



    # reads and stores the raw html data into the variable page_html
    page_html2 = uClient2.read()
    uClient2.close()

    # parses page
    page_soup2 = soup(page_html2, "html.parser")

    # finds all "div" class:"item-container" and stores the data into the variable containers
    # (grabs all products on page)
    containers = page_soup2.findAll("div", {"class": "item-container"})

    # grabs product data from item containers
    for container in containers:

        # Title of product
        title = container.a.img['title']

        # Image of product
        image_source_find = container.findAll('a', {'class': 'item-img'})
        image_source_find_str = str(image_source_find)
        image_source_list = image_source_find_str.split()
        for string_ in image_source_list:
            if string_[0:3] == 'src':
                image_source = string_[5:-1]

        # Grabs model number
        model_numb_find = container.find('ul', {'class': 'item-features'})
        model_numb_find_str = str(model_numb_find)
        model_num_find_str_split = model_numb_find_str.split('Model #: </strong>')
        model_num_count = 0
        model_num =''
        for digit in model_num_find_str_split[1]:
            if digit in '<':
                model_num_count += 1
            if model_num_count == 0:
                model_num += digit

        # finds product web link
        search_link = container.a
        search_link_str = str(search_link)
        search_link_str_split = search_link_str.split()
        search_link_str_split_count = 0
        for string_ in search_link_str_split:
            if string_[0:4] == 'href':
                search_link_str_split_count += 1
                if search_link_str_split_count == 1:
                    web_link = string_[6:-6]

        # finds current price
        search_current_price = container.find('li', {'class': 'price-current'})
        search_current_price_str = str(search_current_price)
        price_current_str = ''
        price_current_dec_count = 0
        for letter in search_current_price_str:
            if letter in '.0123456789':
                if letter == '.':
                    price_current_dec_count += 1
                if price_current_dec_count < 2:
                    price_current_str += letter

        # Finds what price was
        price_was_search = container.findAll('li', {'class': 'price-was'})
        price_was_search_str = str(price_was_search)
        price_was_search_str_split = price_was_search_str.split()
        price_was_str = ''
        for string_ in price_was_search_str_split:
            if string_[7:21] == 'price-was-data':
                search_str = string_[21:]
                for letter in search_str:
                    if letter in '.0123456789':
                        price_was_str += letter

        # calculates savings
        if len(price_was_str) > 0 and len(price_current_str) > 0:
            price_was_float = float(price_was_str)
            price_current_float = float(price_current_str)
            price_savings_float = round(price_was_float - price_current_float, 2)
            price_savings_str = str(price_savings_float)

            product_details = {'Title': title, 'Image': image_source, 'Price-was': '$' + price_was_str,
                               'Current price': '$' + price_current_str, 'Price savings': '$' + price_savings_str,
                               'Web link': web_link, 'Model number' : model_num}

            newegg_playstation5games_list.append(product_details)



for item in newegg_playstation5games_list:
    print(item)
