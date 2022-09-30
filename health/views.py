import requests
import certifi
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from django.shortcuts import render
from . import models

BASE_JUMIA_URL = 'https://www.jumia.co.ke/catalog/?q={}'
BASE_NAIVAS_URL = 'https://e-mart.co.ke/index.php?category_id=0&search={}&submit_search=&route=product%2Fsearch'

# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'health/about.html')

def price_search(item):
    #search = request.POST.get('search')
    print(quote_plus(item))
    print(certifi.where())
    final_url = BASE_JUMIA_URL.format(quote_plus(item))
    print(final_url)
    html_object = requests.get(final_url, verify=certifi.where())
    webpage = html_object.text
    soup = BeautifulSoup(webpage, features='html.parser')
    #print(soup.prettify())
    price = soup.find_all('div', {'class': 'prc'})

    try:
        money = price[0].text
    except IndexError:
        money = "Price not found"
    #disease_search()
    
    return money, final_url

def price_search_naivas(item):
    print(quote_plus(item))
    print(certifi.where())
    final_url = BASE_NAIVAS_URL.format(quote_plus(item))
    print(final_url)
    html_object = requests.get(final_url, verify = certifi.where())
    webpage = html_object.text
    soup = BeautifulSoup(webpage, features = 'html.parser')
    price = soup.find_all('span', {'class': 'price-new'})
    print(price)

    try:
        money = price[0].text
    except IndexError:
        money = "Price not found"
    
    
    print(money)

    return money, final_url

def disease_search(request):
    if request.method == "POST":
        SITE_URL = 'https://www.britannica.com/science/nutritional-disease'
        web_page = requests.get(SITE_URL, verify=certifi.where())
        html_doc = web_page.content
        scraper = BeautifulSoup(html_doc, features='html.parser')
        table = scraper.body.table.find_all('tr')
        search = request.POST.get('search')
        models.DiseaseSearch.objects.create(search=search)
        tr = list(table)
        link_ = []
        link_to_get_parent = None
        for i in range(3, 9):
            disease_data = tr[i].find_all('td', {'scope': 'row'})
            for a in disease_data:
                link = a.find('a')
                link_ += a.find('a').parent
                print(link_)
        print(link_)

        disease_name = search
        disease_symptoms = "Not found"
        diet_list = []
        food_type = {
            'Nothing here': ["Not found", "Not found"]
        }


        for food_link in link_:
            if search.lower() in food_link.text:
                link_to_get_parent = food_link
                print(link_to_get_parent)
                list_of_all_data_in_parent = list(link_to_get_parent.parent.parent.find_all('td'))
                disease_name = list_of_all_data_in_parent[0].text
                disease_symptoms = list_of_all_data_in_parent[1].text
                disease_diet = list_of_all_data_in_parent[2].text
                print(disease_name)
                print(disease_symptoms)
                diet_list = disease_diet.split(',')
                
                food_type = dict()

                for food in diet_list:
                    food_type[food] = [price_search_naivas(food), price_search(food)]
                    print(type(food_type[food]))

                print(food_type)
            else:
                print('not in database')

        
        
                

        frontend_display = {
            'search': disease_name,
            'disease_symptoms': disease_symptoms,
            'disease_diet': diet_list,
            'food_type': food_type,
        }
        return render(request, 'health/details.html', frontend_display)
    else:
        return render(request, 'health/details.html')




