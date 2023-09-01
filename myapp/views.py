import json
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from .utils import *
from django.conf import settings
from operator import itemgetter



def home(request):
    return render(request, "home.html", locals())


def about(request):
    return render(request, "about.html", locals())


# def contact(request):
#     return render(request, "contact.html", locals())


def register(request):
    if request.method == "POST":
        re = request.POST
        rf = request.FILES
        user = User.objects.create_user(
            username=re['username'], first_name=re['first_name'], last_name=re['last_name'], password=re['password'])
        # register = Register.objects.create(user=user, address=re['address'], mobile=re['mobile'], image=rf['image'])
        messages.success(request, "Registration Successful")
        return redirect('signin')
    return render(request, "signup.html", locals())


def update_profile(request):
    if request.method == "POST":
        re = request.POST
        rf = request.FILES
        try:
            image = rf['image']
            data = Register.objects.get(user=request.user)
            data.image = image
            data.save()
        except:
            pass
        user = User.objects.filter(id=request.user.id).update(
            username=re['username'], first_name=re['first_name'], last_name=re['last_name'])
        # register = Register.objects.filter(user=request.user).update(address=re['address'], mobile=re['mobile'])
        messages.success(request, "Updation Successful")
        return redirect('update_profile')
    return render(request, "update_profile.html", locals())


def signin(request):
    if request.method == "POST":
        re = request.POST
        user = authenticate(username=re['username'], password=re['password'])
        if user:
            login(request, user)
            messages.success(request, "Logged in successful")
            return redirect('home')
    return render(request, "signin.html", locals())


def admin_signin(request):
    if request.method == "POST":
        re = request.POST
        user = authenticate(username=re['username'], password=re['password'])
        print("here.................", user)

        if user.is_staff:
            login(request, user)
            messages.success(request, "Logged in successful")
            return redirect('home')
    return render(request, "admin_signin.html", locals())


def change_password(request):
    if request.method == "POST":
        re = request.POST
        user = authenticate(username=request.user.username,
                            password=re['old-password'])
        if user:
            if re['new-password'] == re['confirm-password']:
                user.set_password(re['confirm-password'])
                user.save()
                messages.success(request, "Password changed successfully")
                return redirect('home')
            else:
                messages.success(request, "Password mismatch")
        else:
            messages.success(request, "Wrong password")
    return render(request, "change_password.html", locals())


def logout_user(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect('home')


def search_product(request):
    product = []
    dictobj = {'object': []}
    if request.method == "POST":
        re = request.POST
        name = re['search']

        flipkart_price, flipkart_name, flipkart_image, flipkart_link,fk_product_rating  = flipkart(name)
        
        amazon_price, amazon_name, amazon_image, amazon_link,a_product_rating = amazon(name)

        gadgetsnow_price, gadgetsnow_name, gadgetsnow_image, gadgetsnow_link,gn_product_rating  = gadgetsnow(name)
        
        dealAyo_price, dealAyo_name, dealAyo_image, dealAyo_link, da_product_rating = dealAyo(
            name)
        
        olizstore_price, olizstore_name, olizstore_image, olizstore_link, o_product_rating  = olizstore(
            name)

        dictobj["object"].append({'logo': '/static/assets/' + 'img/' + 'flipkart-logo.png', 'price': convert(
            flipkart_price), 'name': flipkart_name, 'link': flipkart_link, 'image': flipkart_image
            ,'rating':fk_product_rating  })
        
        dictobj["object"].append({'logo': '/static/assets/' + 'img/' + 'gadgetbyte.jpg', 'price': convert(
            amazon_price), 'name': amazon_name, 'link': amazon_link, 'image': amazon_image,
            'rating':a_product_rating })
        
        dictobj["object"].append({'logo': '/static/assets/' + 'img/' + 'gadgetsnow-logo.png', 'price': convert(
            gadgetsnow_price), 'name': gadgetsnow_name, 'link': gadgetsnow_link, 'image': gadgetsnow_image,
            'rating':gn_product_rating })
        
        dictobj["object"].append({'logo': '/static/assets/' + 'img/' + 'deal_ayo.png', 'price': convert(
            dealAyo_price), 'name': dealAyo_name, 'link': dealAyo_link, 'image': dealAyo_image,
            'rating':da_product_rating })

        dictobj["object"].append({'logo': '/static/assets/' + 'img/' + 'olizstore.png', 'price': convert(
            olizstore_price), 'name': olizstore_name, 'link': olizstore_link, 'image': olizstore_image,
            'rating':o_product_rating})

        data = dictobj['object']
        # data = sorted(data, key=itemgetter('price'))
        # history = History.objects.create(user=request.user, product=dictobj)
        # messages.success(request, "History Saved")
    return render(request, "search_product.html", locals())


def search(request):
    product_list = {'object': []}

    if request.method == "POST":
        re = request.POST
        name = re['search']

        gadgetbyte_name1, gadgetbyte_price, product_weight, product_display, product_resolution, \
            product_processor, product_OS, product_RAM, product_storage, product_back, \
            product_Front, product_battery, product_cpu, product_sim, product_image, gadgetbyte_link, product_model,product_rating,price_g,product_review_g = gb(
                name)

        flipkart_price1, flipkart_name1, product_Storage1, product_back_camera1, \
            product_front_camera1, product_Resolution_element1, product_RAM_element1, product_Processor1, \
            product_Display1, product_Weight1, product_SIM1, product_OS1, product_Model1, product_Battery1, \
            product_Performance1, flipkart_image1, flipkart_product_link1,product_rating1,price_f,product_review_f = flipkart_d(
                name)
        
        if price_f < price_g:
            if product_rating1 > product_rating:
                this_product_f = 'This is good. Price is low and rating is high'
                this_product_g = "Price is higher than the other product and rating is also low"
                
            else:
                this_product_f = "Price is low as well as rating is also low"
                this_product_g = "Price is higher than the other product, but rating is great"
       
        else:
            if product_rating1 < product_rating:
                this_product_g = 'This is good. Price is low and rating is high'
                this_product_f = "Price is higher than the other product, and rating is also low"
            else:
                this_product_g = "Price is low as well as rating is also low"
                this_product_f = "Price is higher than the other product, but rating is also higher"
        
        if price_f ==0:
                this_product_f = "No product found...."
                
        if price_g ==0:       
                this_product_g = "No product found...." 
            

        product_list["object"].append({
            'logo': '/static/assets/img/flipkart-logo.png',
            # Implement the 'convert' function
            'price': convert(flipkart_price1),
            'name': flipkart_name1,
            'RAM': product_RAM_element1,
            'back': product_back_camera1,
            'storage': product_Storage1,
            'front': product_front_camera1,
            'resolution': product_Resolution_element1,
            'processor': product_Processor1,
            'display': product_Display1,
            'weight': product_Weight1,
            'sim': product_SIM1,
            'os': product_OS1,
            'model': product_Model1,
            'battery': product_Battery1,
            'performance': product_Performance1,
            'image': flipkart_image1,
            'link': flipkart_product_link1,
            'rating':product_rating1,
            "thought":this_product_f,
            "review":product_review_f
        })

        product_list["object"].append({
            'logo': '/static/assets/img/gadgetbyte.jpg',
            # Implement the 'convert' function
            'price': convert(gadgetbyte_price),
            'name': gadgetbyte_name1,
            'RAM': product_RAM,
            'back': product_back,
            'storage': product_storage,
            'front': product_Front,
            'resolution': product_resolution,
            'processor': product_processor,
            'display': product_display,
            'weight': product_weight,
            'sim': product_sim,
            'os': product_OS,
            'model': product_model,
            'battery': product_battery,
            'performance': product_cpu,
            'image': product_image,
            'link': gadgetbyte_link,
            'rating':product_rating,
            "thought":this_product_g,
            "review":product_review_g
        })

        data = product_list["object"]
        data = sorted(data, key=itemgetter('price'))

    return render(request, "search.html", locals())


# def search(request):
#     product_list = {'object': []}

#     if request.method == "POST":
#         re = request.POST
#         name = re['search']

#         # Call the flipkart_d function to get product details
#         flipkart_price1, flipkart_name1, product_Storage, product_back_camera, \
#             product_front_camera, product_Resolution_element, product_RAM_element, product_Processor, \
#             product_Display, product_Weight, product_SIM, product_OS, product_Model, product_Battery, \
#             product_Performance, flipkart_image, flipkart_product_link = flipkart_d(
#                 name)

#         gadgetbyte_name, gadgetbyte_price, product_weight, product_display, product_resolution,
#         product_processor, product_OS, product_RAM, product_storage, product_back, product_model,
#         product_Front, product_battery, product_cpu, product_sim, product_image, gadgetbyte_link = gadgetbyte(
#             name)

#         # Append Flipkart product details to the list
#         product_list["object"].append({
#             'logo': '/static/assets/img/flipkart-logo.png',
#             'price': convert(flipkart_price1),
#             'name': flipkart_name1,
#             'RAM': product_RAM_element,
#             'back': product_back_camera,
#             'storage': product_Storage,
#             'front': product_front_camera,
#             'resolution': product_Resolution_element,
#             'processor': product_Processor,
#             'display': product_Display,
#             'weight': product_Weight,
#             'sim': product_SIM,
#             'os': product_OS,
#             'model': product_Model,
#             'battery': product_Battery,
#             'performance': product_Performance,
#             'image': flipkart_image,
#             'link': flipkart_product_link
#         })

#         # Append GadgetByte product details to the list
#         product_list["object"].append({
#             'logo': '/static/assets/img/gadgetbyte-logo.png',
#             'price': convert(gadgetbyte_price),
#             'name': gadgetbyte_name,
#             'RAM': product_RAM,
#             'back': product_back,
#             'storage': product_storage,
#             'front': product_Front,
#             'resolution': product_resolution,
#             'processor': product_processor,
#             'display': product_display,
#             'weight': product_weight,
#             'sim': product_sim,
#             'os': product_OS,
#             'model': product_model,
#             'battery': product_battery,
#             'performance': product_cpu,
#             'image': product_image,
#             'link': gadgetbyte_link
#         })

#         data = product_list["object"]
#         data = sorted(data, key=itemgetter('price'))

#     return render(request, "search.html", locals())


def all_user(request):
    data = Register.objects.filter()
    return render(request, "all_user.html", locals())


def delete_user(request, pid):
    user = User.objects.get(id=pid)
    user.delete()
    messages.success(request, "User Deleted")
    return redirect('all_user')
