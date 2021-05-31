from bs4 import BeautifulSoup as soup
from urllib.request import urlopen

"""
USE https://js-beautify.com/ to BEAUTIFY JAVASCRIPT TO MAKE IT MORE READABLE
"""
'''
----------------------- Newegg fill product webscraper ------------------------------------------------------------------
def newegg_product_fill(): fills a list with discounted items from website address
'''


def newegg_product_fill(website, console_str):
    # storing website destination as my_url variable
    my_url = 'https://www.newegg.com/p/pl?N=100021799%204803'

    # calls urlopen function from request function in urllib
    # opens up connection and grabs the page
    uClient = urlopen(website)

    # reads and stores the raw html data into the variable page_html
    page_html = uClient.read()
    uClient.close()

    # parses page
    page_soup = soup(page_html, "html.parser")

    # finds all "div" class:"item-container" and stores the data into the variable containers
    # (grabs all products on page)
    containers = page_soup.findAll("div", {"class": "item-container"})

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
    product_list = []
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
            model_num = ''
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
                                   'Web link': web_link, 'Model number': model_num, 'Console type': console_str}

                product_list.append(product_details)

    return product_list

'''
-----------------------------------------END OF FUNCTION----------------------------------------------------------------
'''
#  Xbox One
xbox1_website = 'https://www.newegg.com/p/pl?N=100021799%204803'
newegg_xbox1_product_list = newegg_product_fill(xbox1_website, 'xbox1')

for item in newegg_xbox1_product_list:
    print(item)

# Xbox X and S
xboxX_website = 'https://www.newegg.com/Xbox-Series-X-S-Games/SubCategory/ID-3760?Tid=1696837'
newegg_xboxX_product_list = newegg_product_fill(xboxX_website, 'xbox x')

for item in newegg_xboxX_product_list:
    print(item)

# Playstation 4
ps4_website = 'https://www.newegg.com/PS4-Video-Games/SubCategory/ID-3141?Tid=21831'
newegg_ps4_product_list = newegg_product_fill(ps4_website, 'ps4')

for item in newegg_ps4_product_list:
    print(item)

# Playstation 5
ps5_website = 'https://www.newegg.com/PS5-Video-Games/SubCategory/ID-3763?Tid=1696841'
newegg_ps5_product_list = newegg_product_fill(ps5_website, 'ps5')

for item in newegg_ps5_product_list:
    print(item)

# Playstation Vita
psvita_website = 'https://www.newegg.com/PS-Vita-Games/SubCategory/ID-2808?Tid=252386'
newegg_psvita_product_list = newegg_product_fill(psvita_website, 'ps vita')

for item in newegg_psvita_product_list:
    print(item)

# Nintendo Switch
switch_website = 'https://www.newegg.com/Nintendo-Switch-Video-Games/SubCategory/ID-3733?Tid=252381'
newegg_switch_product_list = newegg_product_fill(switch_website, 'switch')

for item in newegg_switch_product_list:
    print(item)

# PC
pc_website = 'https://www.newegg.com/p/pl?N=100007756%204803'
newegg_pc_product_list = newegg_product_fill(pc_website, 'pc')

for item in newegg_pc_product_list:
    print(item)

# Mac
mac_website = 'https://www.newegg.com/p/pl?SubCategory=580&N=40000580'
newegg_mac_product_list = newegg_product_fill(mac_website, 'mac')

for item in newegg_mac_product_list:
    print(item)

# Wii
wii_website = 'https://www.newegg.com/Nintendo-Wii-Games/SubCategory/ID-544?Tid=1698973'
newegg_wii_product_list = newegg_product_fill(wii_website, 'wii')

for item in newegg_wii_product_list:
    print(item)

# VR
vr_website = 'https://www.newegg.com/VR-Games/SubCategory/ID-3722?Tid=245657'
newegg_vr_product_list = newegg_product_fill(vr_website, 'vr')

for item in newegg_vr_product_list:
    print(item)
