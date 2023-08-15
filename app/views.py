from telnetlib import LOGOUT
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib import messages 
import csv

# Create your views here.
from bs4 import BeautifulSoup as soup
import csv
from django.conf import settings
import time
import requests

def About(request):
    return render(request, 'about.html')
# Create your views here.
@login_required(login_url='login')
def HomePage(request):
    return render(request,'index.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        
        if pass1!=pass2:
            return HttpResponse("not done")
        else:
            my_user= User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
    return render(request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user = authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('Grossary')
        else:
            return HttpResponse("incorrect")
    return render(request,'login.html')


def LogoutPage(request):
    logout(request)
    return redirect('/')

def Clothes(request):
    mylist = []
    if request.method == 'POST':
        product_name = request.POST['name'].strip().replace(' ', '+')
        mylist = scrape_amazon_data(product_name)
    return render(request, 'clothes.html',{'mylist':mylist})

def Medicine(request):
    return render(request,'medicine.html')
def Grocery(request):
    return render(request,'grocery.html')

def Grossary(request):
    return render(request,'grossary.html')

def get_html_content(url):
    import requests
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    session =requests.Session()
    session.headers['User-Agents']= USER_AGENT
    #url= url.replace(' ','+')
    html_content = session.get(url).text
    return html_content


from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import numpy as np

def scrape_amazon_data(product_name):
    url = f'https://www.amazon.com/s?k={product_name}+4&ref=nb_sb_noss_2'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'}
    webpage = requests.get(url, headers=headers)
    soup = BeautifulSoup(webpage.content, "html.parser")
    links = soup.find_all("a", attrs={'class': 'a-link-normal s-no-outline'})
    links_list = [link.get('href') for link in links]
    d = {"title": [], "price": [], "rating": [], "reviews": [], "availability": [],"prod_url":[]}
    
    for link in links_list:
        new_webpage = requests.get("https://www.amazon.com" + link, headers=headers)
        prod_url = "https://www.amazon.com" + link
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")
        # Function calls to display all necessary product information
        d['title'].append(get_title(new_soup))
        d['price'].append(get_price(new_soup))
        d['rating'].append(get_rating(new_soup))
        d['reviews'].append(get_review_count(new_soup))
        d['availability'].append(get_availability(new_soup))
        d['prod_url'].append(prod_url)
    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df['title'].replace('', np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['title'])
    file_name = "static/amazon_data.csv"
    file = open(file_name, 'w')

    amazon_df.to_csv("static/amazon_data.csv", header=True, index=False)
    #file.write(amazon_df)
    mylis = zip(d['title'], d['price'], d['rating'], d['reviews'], d['availability'], d['prod_url'])
    mylist = list(mylis)
    #print(mylist)
    return mylist
def About(request):
    mylist = []
    if request.method == 'POST':
        product_name = request.POST['name'].strip().replace(' ', '+')
        mylist = scrape_amazon_data(product_name)
    return render(request, 'about.html',{'mylist':mylist})

def get_title(soup):
    try:
        title = soup.find("span", attrs={"id": 'productTitle'})
        title_value = title.text
        title_string = title_value.strip()
    except AttributeError:
        title_string = ""
    return title_string

# Rest of the get_price, get_rating, get_review_count, and get_availability functions remain unchanged.

# Function to extract Product Price
def get_price(soup):

    try:
        price = soup.find("span", attrs={'class':'a-offscreen'}).string.strip()

    except AttributeError:

        try:
            # If there is some deal price
            price = soup.find("span", attrs={'id':'priceblock_dealprice'}).string.strip()

        except:
            price = ""

    return price

# Function to extract Product Rating
def get_rating(soup):

    try:
        rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
    
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = "" 

    return rating

# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()

    except AttributeError:
        review_count = ""   

    return review_count

# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id':'availability'})
        available = available.find("span").string.strip()

    except AttributeError:
        available = "Not Available" 

    return available


def scrape_flipkart_data(product_name):
    url = f'https://www.flipkart.com/search?q={product_name}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
    headers = {'User-Agent': 'Mozilla/5.0'}
    webpage = requests.get(url, headers=headers)
    soup = BeautifulSoup(webpage.content, "html.parser")
    products = soup.find_all("div", attrs={"class": "_1AtVbE"})
    d = {"title": [], "price": [], "rating": [], "reviews": [], "availability": [], "prod_url": []}
    
    for product in products:
        title_element = product.find("a", attrs={"class": "IRpwTa"})
        price_element = product.find("div", attrs={"class": "_30jeq3 _1_WHN1"})
        rating_element = product.find("div", attrs={"class": "_3LWZlK"})
        reviews_element = product.find("span", attrs={"class": "_2_R_DZ"})
        availability_element = product.find("div", attrs={"class": "_3A6ZiH"})
        
        title = title_element.get("title") if title_element else ""
        price = price_element.text if price_element else ""
        rating = rating_element.text if rating_element else ""
        reviews = reviews_element.text.split()[0] if reviews_element else ""
        availability = availability_element.text if availability_element else ""
        prod_url = "https://www.flipkart.com" + title_element.get("href") if title_element else ""
        
        d['title'].append(title)
        d['price'].append(price)
        d['rating'].append(rating)
        d['reviews'].append(reviews)
        d['availability'].append(availability)
        d['prod_url'].append(prod_url)
    
    flipkart_df = pd.DataFrame.from_dict(d)
    flipkart_df['title'].replace('', np.nan, inplace=True)
    flipkart_df = flipkart_df.dropna(subset=['title'])
    file_name = "static/flipkart_data.csv"
    flipkart_df.to_csv(file_name, header=True, index=False)
    
    mylist2 = zip(d['title'], d['price'], d['rating'], d['reviews'], d['availability'], d['prod_url'])
    return mylist2
