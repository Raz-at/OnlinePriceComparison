import imp
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.conf import settings
import math


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}


def flipkart(name):
    try:
        search_query = name.replace(" ", "+")
        flipkart_link = f'https://www.flipkart.com/search?q={search_query}'
        response = requests.get(flipkart_link, headers=headers)

        print("\nSearching in Flipkart for details...")

        soup = BeautifulSoup(response.text, 'html.parser')
        product = soup.select_one('._13oc-S, ._1xHGtK._373qXS, ._4ddWXP')

        if product:
            element_with_href = soup.select_one('._1fQZEK, ._2rpwqI')
            if element_with_href:
                href_value = element_with_href['href']
                flipkart_product_link = 'https://www.flipkart.com' + href_value
                print("Product Link:", flipkart_product_link)

                res1 = requests.get(flipkart_product_link, headers=headers)
                soup1 = BeautifulSoup(res1.text, 'html.parser')

                product_name_element = soup1.select_one('._1fTJQ7, .B_NuCI')
                if product_name_element:
                    flipkart_name = product_name_element.getText().strip()
                    flipkart_name = flipkart_name.split("(")[0]
                    print('Name:', flipkart_name)
                else:
                    print("Product name not found on Flipkart.")
                    flipkart_name = 'Product Not Found'

                product_price_element = soup1.select_one('._30jeq3._16Jk6d') 
                if product_price_element:
                    flipkart_price = product_price_element.getText().strip()
                    print("Price:", flipkart_price)
                else:
                    print("Product price not found on Flipkart.")
                    flipkart_price = 0
                
                product_image_element = soup1.select_one('._396cs4._2amPTt._3qGmMb')
                if product_image_element:
                    flipkart_image = product_image_element['src']
                    print("Image:", flipkart_image)
                else:
                    print("Image not found on Flipkart.")
                    flipkart_image = ''

                product_rating_element = soup.select_one('._3LWZlK')
                if product_rating_element:
                    product_rating = product_rating_element.getText().strip()
                    print('Rating:', product_rating)
                else:
                    print("No rating found.")
                    product_rating = ''
                
                product_review_element = soup.select_one(".t-ZTKy")
                if product_review_element:
                    product_review = product_review_element.getText().strip()
                    product_review = product_review.split("Read")[0]
                    print('Review:', product_review)
                else:
                    print("No Review found.")
                    product_review = "not found"
        else:
            print("No product found on Flipkart.")
            flipkart_name = 'Product Not Found'
            flipkart_price = 0
            flipkart_product_link=''
            flipkart_image = ''
            product_rating = ''


        return flipkart_price, flipkart_name[:40], flipkart_image, flipkart_product_link ,product_rating 

    except:
        print("Flipkart: An error occurred:")
        print("---------------------------------")
        flipkart_name = 'Product Not Found'
        flipkart_price = 0
        flipkart_image = ''
        flipkart_product_link = ''
        product_rating = ''

    return flipkart_price, flipkart_name[:40], flipkart_image, flipkart_product_link , product_rating

# def amazon(name):
#     try:
#         name2 = name.replace(" ", "-")
#         amazon_link = f'https://www.gadgetbytenepal.com/product/{name2}/'

#         res = requests.get(amazon_link, headers=headers)
#         print("\nSearching in Amazon...")
#         soup = BeautifulSoup(res.text, 'html.parser')

#         # Find the product name element
#         product_name_element = soup.select_one('.title-toolbar h1')

#         if product_name_element:
#             amazon_name = product_name_element.getText().strip()
#             amazon_name = amazon_name.split("(")[0]

#             print('Name:', amazon_name)
#         else:
#             print("Product name not found on gadgetbyte.")
#             return None

#         # Find the product price element
#         product_price_element = soup.select_one('.product-brand-price')
#         if product_price_element:
#             amazon_price = product_price_element.getText().strip()
#             print("Price:", amazon_price)
#         else:
#             print("Product price not found on gadgetbyte.")
#             return None

#         # Extract product image information
#         product_image_element = soup.select_one('.attachment-thumbnail.size-thumbnail')
        
#         if product_image_element:
#             product_image = product_image_element['data-src']
#             print("Image:", product_image)
#         else:
#             product_image = ''
#             print("Image not found on gadgetbyte.")

#         product_rating_element = soup.select_one('.rating-number')
#         if product_rating_element:
#             product_rating = product_rating_element.find_next('span').getText().strip()
#             print('Rating is', product_rating)
#         else:
#             product_rating = 'Rating not found'

#         product_review = "Not found on this website"

#         return amazon_price, amazon_name, product_image, amazon_link, product_rating
    
#     except Exception as e:
#         print("Amazon: An error occurred!")
#         print("Error:", e)
#         print("---------------------------------")
#         return None

def amazon(name):
    name2 = name.replace(" ", "-")
    gadgetbyte_link = f'https://www.gadgetbytenepal.com/product/{name2}/'

    res = requests.get(gadgetbyte_link, headers=headers)
    print("\nSearching in gadgetbyte...")
    soup = BeautifulSoup(res.text, 'html.parser')

    # Find the product name element
    product_name_element = soup.select_one('.title-toolbar h1')

    if product_name_element:
        gadgetbyte_name1 = product_name_element.getText().strip()
        print('Name:', gadgetbyte_name1)

    else:
        gadgetbyte_name1 = 'Name not found'
        print("Product name not found on gadgetbyte.")

    # Find the product price element
    product_price_element = soup.select_one('.woocommerce-Price-amount.amount') or soup.select_one('.product-brand-price') 
    if product_price_element:
        gadgetbyte_price = product_price_element.getText().strip()
        print("Price:", gadgetbyte_price)
        price = gadgetbyte_price.replace("NPR ","")
        price = price.replace(",","")
        price = price.replace("रु ","")
        price = price.replace("INR ","")
        price = price.replace("रु\xa0","")
        price_g = int(price)
        print('this is the  actual price ',price_g)

    else:
        gadgetbyte_price = ''
        print("Product price not found on gadgetbyte.")
        price_g = 0

    # Extract product image information
    product_image_element = soup.select_one('.attachment-thumbnail.size-thumbnail')
    
    if product_image_element:
        product_image = product_image_element['data-src']
        print("Image:", product_image)

    else:
        product_image = ''
        print("Image not found on gadgetbyte.")

    
    # product rating
    product_rating_element = soup.select_one('.rating-number')
    if product_rating_element:
        product_rating = product_rating_element.find_next('span').getText().strip()
        print('Rating is ',product_rating)

    else:
        product_rating=''
        print("no rating found")

    return gadgetbyte_price, gadgetbyte_name1, product_image, gadgetbyte_link, product_rating


def gadgetsnow(name):
    try:
        global gadgetsnow
        # name1 = name.replace(" ", "-")
        name2 = name.replace(" ", "+")
        gadgetsnow = f'https://shop.gadgetsnow.com/mtkeywordsearch?SEARCH_STRING={name2}'
        gadgetsnow_link = gadgetsnow
        res = requests.get(
            f'https://shop.gadgetsnow.com/mtkeywordsearch?SEARCH_STRING={name2}', headers=headers)
        print("\nSearching in gadgetsnow...")
        soup = BeautifulSoup(res.text, 'html.parser')

        gadgetsnow_link = soup.select_one('.product-anchor')
        if gadgetsnow_link:
            href_value = gadgetsnow_link['href']
            # print(href_value)
            gadgetsnow_product_link = 'https://shop.gadgetsnow.com/' + href_value
            print("Product Link:", gadgetsnow_product_link)

            res1 = requests.get(gadgetsnow_product_link, headers=headers)
            soup1 = BeautifulSoup(res1.text, 'html.parser')

            gadgetsnow_name = soup1.find('h1', itemprop='name').text            
            gadgetsnow_name = gadgetsnow_name.split("(")[0]
            print('Name:', gadgetsnow_name)
        
            gadgetsnow_price = soup1.find('span', class_='offerprice')
            gadgetsnow_price = gadgetsnow_price.get_text(strip=True).split()[-1]
            gadgetsnow_price = gadgetsnow_price.split("`")[-1]
            gadgetsnow_price = "INR "+gadgetsnow_price
            print("Price: ",gadgetsnow_price)

            rating_div = soup1.find('div', class_='product-view-rating')
            rating_span = rating_div.find('span')
            product_rating = rating_span.get_text(strip=True).replace('(', '').replace(')', '')
            print("Rating: ",product_rating)

           
            image_a = soup1.find('a', class_='cloud-zoom')
            gadgetsnow_image = image_a['href']
            print("Image: ",gadgetsnow_image)

        return gadgetsnow_price, gadgetsnow_name[0:40], gadgetsnow_image, gadgetsnow_product_link , product_rating 
    except:
        print("GadgetSnow: No product found!")
        print("---------------------------------")
        gadgetsnow_price = ''
        gadgetsnow_name = 'Product Not Found'
        gadgetsnow_image = '0'
        gadgetsnow_product_link = ''
        product_rating =''
    return gadgetsnow_price, gadgetsnow_name[0:40], gadgetsnow_image, gadgetsnow_product_link ,product_rating 


def olizstore(name):
    try:
        global olizstore
        name2 = name.replace(" ", "+")
        olizstore_link = f'https://www.olizstore.com/catalogsearch/result/?q={name2}'
        res = requests.get(olizstore_link, headers=headers)
        print("\nSearching in OlizStore...")
        soup = BeautifulSoup(res.text, 'html.parser')

        product = soup.select_one('.product-item-info')
        print(product)
        if product:
            olizstore_name_element = (
                product.select_one('.product-item-name a')
            )

            if olizstore_name_element:
                olizstore_name = olizstore_name_element.getText().strip()
                print(olizstore_name)
            else:
                olizstore_name = "Name not found"

            olizstore_price_element = (
                product.select_one(
                    '.special-price') or product.select_one('.price-wrapper')
            )

            if olizstore_price_element:
                olizstore_price = olizstore_price_element.getText().strip()
                olizstore_price = olizstore_price.replace('.00', '')
            else:
                olizstore_price = "Price not found"

            olizstore_images = (
                product.select(
                    '.product-image-photo.default_image.porto-lazyload')
            )
            if olizstore_images:
                olizstore_image = olizstore_images[0]['data-src']
            else:
                olizstore_image = "Image not found"

            product_rating = "Not found in this website"
            product_review = "Not found in this website"

            print(olizstore_name)
            print(olizstore_price)
            print(olizstore_image)
            print(olizstore_link)  # Print the product link
            print("---------------------------------")

        return olizstore_price, olizstore_name[0:40], olizstore_image, olizstore_link , product_rating 
    except:
        print("olizstore: No product found!")
        print("---------------------------------")
        olizstore_price = ''
        olizstore_name = 'Product Not Found'
        olizstore_image = '0'
        olizstore_link = ''
        product_rating=''

    return olizstore_price, olizstore_name[0:40], olizstore_image, olizstore_link ,product_rating 


def dealAyo(name):
    try:
        name2 = name.replace(" ", "+")
        dealAyo_link = f'https://www.dealayo.com/catalogsearch/result/index/?dir=desc&order=price&q={name2}'
        res = requests.get(dealAyo_link, headers=headers)
        print("\nSearching in DealAyo...")
        soup = BeautifulSoup(res.text, 'html.parser')

        # Find the first product item
        product = soup.select_one('.product-item')

        if product:
            dealAyo_name = product.select_one(
                '.product-name').getText().strip()
            dealAyo_name = dealAyo_name.split("(")[0]
            # dealAyo_price = product.select_one('.regular-price').getText().strip()

            special_price = product.select_one('.special-price .price')
            regular_price = product.select_one('.regular-price')

            if special_price:
                dealAyo_price = special_price.getText().strip()
            elif regular_price:
                dealAyo_price = regular_price.getText().strip()
            else:
                dealAyo_price = "Price not found"
            # dealAyo_price = dealAyo_price.replace("Rs.", "").strip()

            dealAyo_images = product.select(
                '.product-image.no-alt-img img.img-responsive')
            if dealAyo_images:
                dealAyo_image = dealAyo_images[0]['src']
            else:
                dealAyo_image = "Image not found"
            
            product_rating = "Not found in this website"
            product_review = "Not found in this website"

            print("DealAyo...")
            print(dealAyo_name)
            print(dealAyo_price)
            print("---------------------------------")
        else:
            print("No product found on DealAyo.")
        return dealAyo_price, dealAyo_name[:40], dealAyo_image, dealAyo_link ,product_rating 

    except:
        print("dealAyo: No product found!")
        print("---------------------------------")
        dealAyo_price = ''
        dealAyo_name = 'Product Not Found'
        dealAyo_image = '0'
        dealAyo_link = ''
        product_rating=''
    return dealAyo_price, dealAyo_name, dealAyo_image, dealAyo_link ,product_rating 


##


def flipkart_d(name):
    try:
        name2 = name.replace(" ", "+")

        # Construct the Flipkart search URL
        flipkart_link1 = f'https://www.flipkart.com/search?q={name2}'

        # Send a GET request to Flipkart's search page
        res = requests.get(flipkart_link1, headers=headers)

        print("\nSearching in Flipkart for details...")

        # Parse the HTML content of the search results page
        soup = BeautifulSoup(res.text, 'html.parser')

        # Find the first product item
        product = (
            soup.select_one('._13oc-S') or
            soup.select_one('._1xHGtK._373qXS') or
            soup.select_one('._4ddWXP')
        )

        if product:
            # Extract the link to the product details page
            element_with_href = (
                soup.select_one('._1fQZEK') or
                soup.select_one('._2rpwqI')
            )
            if element_with_href:

                href_value = element_with_href['href']
                flipkart_product_link = 'https://www.flipkart.com' + href_value

                # Send a GET request to the product details page
                res1 = requests.get(flipkart_product_link, headers=headers)
                soup1 = BeautifulSoup(res1.text, 'html.parser')

                # Extract product name
                product_name_element = (
                    soup1.select_one('._1fTJQ7') or
                    soup1.select_one('.B_NuCI')
                )
                if product_name_element:

                    flipkart_name1 = product_name_element.getText().strip()
                    print('Name:', flipkart_name1)
                else:
                    print("Product name not found on Flipkart.")

                # Extract product price
                product_price_element = soup1.select_one('._30jeq3._16Jk6d') 
                if product_price_element:
                    flipkart_price1 = product_price_element.getText().strip()
                    print("Price:", flipkart_price1)
                    price = flipkart_price1.replace("₹","").replace(",","")
                    price = price.replace("INR ","")
                    price = int(price)
                    price_f = price*1.6
                    price_f = math.ceil(price_f)
                    print("this is flipkart price ",price_f)
                else:
                    print("Product price not found on Flipkart.")
                    flipkart_price1 = 0
                    price_f = 0

                # Extract product Internal Storage information
                product_Storage_element = soup1.find(
                    'td', text='Internal Storage')
                if product_Storage_element:
                    product_Storage = product_Storage_element.find_next(
                        'td').getText().strip()
                    print('Internal Storage:', product_Storage)
                else:
                    print("Product Internal Storage not found on Flipkart.")
                    product_Storage = ''

                # Extract product back camera information
                product_back_camera_element = soup1.find(
                    'td', text='Primary Camera')
                if product_back_camera_element:
                    product_back_camera = product_back_camera_element.find_next(
                        'td').get_text().strip()
                    print('Primary Camera:', product_back_camera)
                else:
                    product_back_camera = ''
                    print("Primary Camera information not found on Flipkart.")

                # Extract product front camera information
                product_front_camera_element = soup1.find(
                    'td', text='Secondary Camera')
                if product_front_camera_element:
                    product_front_camera = product_front_camera_element.find_next(
                        'td').get_text().strip()
                    print('Secondary Camera:', product_front_camera)
                else:
                    product_front_camera = ''
                    print("Front Camera information not found on Flipkart.")

                # Extract product Resolution information
                product_Resolution_element = soup1.find(
                    'td', text='Resolution')
                if product_Resolution_element:
                    product_Resolution = product_Resolution_element.find_next(
                        'td').get_text().strip()
                    print('Resolution:', product_Resolution)
                else:
                    product_Resolution = ''
                    print("Resolution information not found on Flipkart.")

                # Extract product RAM information
                product_RAM_element = soup1.find('td', text='RAM')
                if product_RAM_element:
                    product_RAM = product_RAM_element.find_next(
                        'td').get_text().strip()
                    print('RAM:', product_RAM)
                else:
                    product_RAM = ''
                    print("RAM information not found on Flipkart.")

                # Extract product Processor Type information
                product_Processor_element = soup1.find(
                    'td', text='Processor Type')
                if product_Processor_element:
                    product_Processor = product_Processor_element.find_next(
                        'td').get_text().strip()
                    print('Processor:', product_Processor)
                else:
                    product_Processor = ''
                    print("Processor information not found on Flipkart.")

             # Extract product Display Size Type information
                product_Display_element = soup1.find('td', text='Display Size')
                if product_Display_element:
                    product_Display = product_Display_element.find_next(
                        'td').get_text().strip()
                    print('Display:', product_Display)
                else:
                    product_Display = ''
                    print("Display information not found on Flipkart.")

                # Extract product Weight  Type information
                product_Weight_element = soup1.find('td', text='Weight')
                if product_Weight_element:
                    product_Weight = product_Weight_element.find_next(
                        'td').get_text().strip()
                    print('Weight:', product_Weight)
                else:
                    product_Weight = ''
                    print("Weight information not found on Flipkart.")

                # Extract product SIM Size Type information
                product_SIM_element = soup1.find('td', text='SIM Size')
                if product_SIM_element:
                    product_SIM = product_SIM_element.find_next(
                        'td').get_text().strip()
                    print('SIM:', product_SIM)
                else:
                    product_SIM = ''
                    print("SIM information not found on Flipkart.")

                # Extract product Operating System Type information
                product_OS_element = soup1.find('td', text='Operating System')
                if product_OS_element:
                    product_OS = product_OS_element.find_next(
                        'td').get_text().strip()
                    print('OS:', product_OS)
                else:
                    product_OS = ''
                    print("Operating System information not found on Flipkart.")

                # Extract product Model Name Type information
                product_Model_element = soup1.find('td', text='Model Name')
                if product_Model_element:
                    product_Model = product_Model_element.find_next(
                        'td').get_text().strip()
                    print('Model:', product_Model)
                else:
                    product_Model = ''
                    print("Model information not found on Flipkart.")

                # Extract product Battery Capacity  Type information
                product_Battery_element = soup1.find(
                    'td', text='Battery Capacity')
                if product_Battery_element:
                    product_Battery = product_Battery_element.find_next(
                        'td').get_text().strip()
                    print('Battery:', product_Battery)
                else:
                    product_Battery = ''
                    print("Battery information not found on Flipkart.")

                # Extract product Performance  Type information
                product_Performance_element = soup1.find(
                    'td', text='Processor Core')
                if product_Performance_element:
                    product_Performance = product_Performance_element.find_next(
                        'td').get_text().strip()
                    print('Performance:', product_Performance)
                else:
                    product_Performance = ''
                    print("Performance information not found on Flipkart.")

                # Extract product image
                product_image_element = soup1.select_one(
                    '._396cs4._2amPTt._3qGmMb')
                if product_image_element:
                    flipkart_image = product_image_element['src']
                    print("Image:", flipkart_image)
                else:
                    flipkart_image = ''
                    print("Image not found on Flipkart.")

                # product rating
                product_rating_element = soup.select_one('._3LWZlK')
                if product_rating_element:
                    product_rating = product_rating_element.getText().strip()
                    print('Rating is ',product_rating)
                else:
                    product_rating=''
                    print("no rating found")

                product_review_element = soup.select_one(".t-ZTKy")
                if product_review_element:
                    product_review = product_review_element.getText().strip()
                    product_review = product_review.split("Read")[0]
                    print('Review:', product_review)
                else:
                    print("No Review found.")
                    product_review = "not found"


            else:
                print("No product found on Flipkart.")

            return (
                flipkart_price1, flipkart_name1, product_Storage,
                product_back_camera, product_front_camera,
                product_Resolution, product_RAM, product_Processor, product_Display, product_Weight,
                product_SIM, product_OS, product_Model, product_Battery, product_Performance, flipkart_image, 
                flipkart_product_link,product_rating,price_f,product_review
            )

    except:
        print("Flipkart: No product detail found!")
        print("---------------------------------")
        flipkart_price1 = ''
        flipkart_name1 = 'Product Not Found'
        product_Storage = ''
        product_back_camera = ''
        product_front_camera = ''
        product_Resolution = ''
        product_RAM = ''
        product_Processor = ''
        product_Display = ''
        product_Weight = ''
        product_SIM = ''
        product_OS = ''
        product_Model = ''
        product_Battery = ''
        product_Performance = ''
        flipkart_product_link = ''
        product_rating=''
        price_f=''
        product_review=''

    return (
        flipkart_price1, flipkart_name1, product_Storage,
        product_back_camera, product_front_camera,
        product_Resolution, product_RAM,  product_Processor, product_Display, product_Weight,
        product_SIM, product_OS, product_Model, product_Battery, product_Performance, flipkart_product_link,product_rating,price_f,product_review
    )


def gb(name):

    # name = 'oneplus 10'
    name2 = name.replace(" ", "-")
    gadgetbyte_link = f'https://www.gadgetbytenepal.com/product/{name2}/'

    res = requests.get(gadgetbyte_link, headers=headers)
    print("\nSearching in gadgetbyte...")
    soup = BeautifulSoup(res.text, 'html.parser')

    # Find the product name element
    product_name_element = soup.select_one('.title-toolbar h1')

    if product_name_element:
        gadgetbyte_name1 = product_name_element.getText().strip()
        print('Name:', gadgetbyte_name1)

    else:
        gadgetbyte_name1 = 'Name not found'
        print("Product name not found on gadgetbyte.")

    # Find the model name element
    product_model_element = soup.select_one('.title-toolbar h1')

    if product_model_element:
        product_model = product_model_element.getText().strip()
        print('Model:', product_model)

    else:
        product_model = ''
        print("model name not found on gadgetbyte.")

    # Find the product price element
    product_price_element = soup.select_one('.woocommerce-Price-amount.amount') or soup.select_one('.product-brand-price') 
    if product_price_element:
        gadgetbyte_price = product_price_element.getText().strip()
        print("Price:", gadgetbyte_price)
        price = gadgetbyte_price.replace("NPR ","")
        price = price.replace(",","")
        price = price.replace("रु ","")
        price = price.replace("INR ","")
        price = price.replace("रु\xa0","")
        price_g = int(price)
        print('this is the  actual price ',price_g)

    else:
        gadgetbyte_price = ''
        print("Product price not found on gadgetbyte.")
        price_g = 0

    # Extract product Weight information
    product_weight_element = soup.find('td', text='Weight')
    if product_weight_element:
        product_weight = product_weight_element.find_next(
            'td').get_text().strip()
        print('Weight:', product_weight)

    else:
        product_weight = ''
        print("Product weight not found on gadgetbyte.")

    # Extract product Display Size information
    product_display_element = soup.find('td', text='Size')
    if product_display_element:
        product_display = product_display_element.find_next(
            'td').get_text().strip()
        print('Display:', product_display)

    else:
        product_display = ''
        print("Product display not found on gadgetbyte.")

    # Extract product Resolution information
    product_resolution_element = soup.find('td', text='Resolution')
    if product_resolution_element:
        product_resolution = product_resolution_element.find_next(
            'td').get_text().strip()
        if 'pixels' in product_resolution:
            product_resolution = product_resolution.split('pixels')[
                0].strip()
            product_display = product_display+' pixels'
            print('Resolution:', product_resolution)

    else:
        product_resolution = ''
        print("Product resolution not found on gadgetbyte.")

    # Extract product Processor Type information
    product_processor_element = soup.find('td', text='Chipset')
    if product_processor_element:
        product_processor = product_processor_element.find_next(
            'td').get_text().strip()
        print('Processor:', product_processor)

    else:
        product_processor = ''
        print("Processor information not found on gadgetbyte.")

    # Extract product OS Type information
    product_OS_element = soup.find('td', text='OS')
    if product_OS_element:
        product_OS = product_OS_element.find_next('td').get_text().strip()
        print('OS:', product_OS)

    else:
        product_OS = ''
        print("OS information not found on gadgetbyte.")

    # Extract product RAM Type information
    product_RAM_element = soup.find('h4', text='Memory')
    if product_RAM_element:
        product_RAM = product_RAM_element.find_next(
            'div').get_text().strip()
        print('RAM:', product_RAM)

    else:
        product_RAM = ''
        print("RAM information not found on gadgetbyte.")

    # Extract product storage Type information
    product_storage_element = soup.find('h4', text='Storage')
    if product_storage_element:
        product_storage = product_storage_element.find_next(
            'div').get_text().strip()
        product_storage = product_storage.split('/')[0].strip()
        print('Storage:', product_storage)

    else:
        product_storage = ''
        print("Storage information not found on gadgetbyte.")

    # Extract product back camera Type information
    product_back_element = soup.find('h4', text='Camera')
    if product_back_element:
        product_back = product_back_element.find_next(
            'div').get_text().strip()
        print('Back Camera:', product_back)

    else:
        product_back = ''
        print("Back camera information not found on gadgetbyte.")

    # Extract product Processor Type information
    product_Front_element = soup.find('td', text='Single')
    if product_Front_element:
        product_Front = product_Front_element.find_next(
            'td').get_text().strip()
        print('Front Camera:', product_Front)

    else:
        product_Front = ''
        print("Front Camera information not found on gadgetbyte.")

    # Extract battery Processor Type information
    product_battery_element = soup.find('h4', text='Battery')
    if product_battery_element:
        product_battery = product_battery_element.find_next(
            'div').get_text().strip()
        print('Battery:', product_battery)

    else:
        product_battery = ''
        print("Battery information not found on gadgetbyte.")

    # Extract product cpu Type information
    product_cpu_element = soup.find('td', text='CPU')
    if product_cpu_element:
        product_cpu = product_cpu_element.find_next(
            'td').get_text().strip()
        if 'core' in product_cpu:
            product_cpu = product_cpu.split('core')[0].strip()
            product_cpu = product_cpu + 'core'
            print('CPU:', product_cpu)

    else:
        product_cpu = ''
        print("CPU information not found on gadgetbyte.")

    # Extract product SIM Type information
    product_sim_element = soup.find('td', text='SIM')
    if product_sim_element:
        product_sim = product_sim_element.find_next(
            'td').get_text().strip()
        print('SIM:', product_sim)

    else:
        product_sim = ''
        print("SIM information not found on gadgetbyte.")

    # Extract product image information
    product_image_element = soup.select_one('.attachment-thumbnail.size-thumbnail')
    
    if product_image_element:
        product_image = product_image_element['data-src']
        print("Image:", product_image)

    else:
        product_image = ''
        print("Image not found on gadgetbyte.")



    
    # product rating
    product_rating_element = soup.select_one('.rating-number')
    if product_rating_element:
        product_rating = product_rating_element.find_next('span').getText().strip()
        print('Rating is ',product_rating)

    else:
        product_rating=''
        print("no rating found")

    product_review='review not found'




    return gadgetbyte_name1, gadgetbyte_price, product_weight, product_display, product_resolution, \
        product_processor, product_OS, product_RAM, product_storage, product_back, \
        product_Front, product_battery, product_cpu, product_sim, product_image, gadgetbyte_link, \
        product_model, product_rating, price_g,product_review


def convert(a):
    return a
