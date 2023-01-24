import requests
import certifi
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from django.shortcuts import render
from .models import DiseaseSearch
from . import website_scraping


BASE_JUMIA_URL = 'https://www.jumia.co.ke/catalog/?q={}'
BASE_NAIVAS_URL = 'https://e-mart.co.ke/index.php?category_id=0&search={}&submit_search=&route=product%2Fsearch'

# Create your views here.
def home(request):
    return render(request, 'health/index.html')

def about(request):
    return render(request, 'health/about.html')


def jumia_site_scraping(food_item):
    food_item_searched = food_item
    supermarket_site_url = 'https://www.jumia.co.ke/catalog/?q={}'

    bs4_object = website_scraping.SupermarketSite(food_item_searched, supermarket_site_url)
    soup = bs4_object.soup
    try:
        price = soup.find('div', class_='prc').text
    except AttributeError:
        price = "Price not found"
    return [price, bs4_object.searched_url]

def emart_site_scraping(food_item):
    food_item_searched = food_item
    supermarket_site_url = 'https://e-mart.co.ke/index.php?category_id=0&search={}&submit_search=&route=product%2Fsearch'
    bs4_object = website_scraping.SupermarketSite(food_item_searched, supermarket_site_url)
    soup = bs4_object.soup
    try:
        price = soup.find('span', class_='price-new').text
    except AttributeError:
        price = "Price not found"
    return [price, bs4_object.searched_url]

def greenspoon_site_scraping(food_item):
    url = 'https://greenspoon.co.ke/?s={}'
    bs4_object = website_scraping.SupermarketSite(food_item, url)
    soup = bs4_object.soup
    try:
        price = soup.find('span', class_='woocommerce-Price-currencySymbol').next_sibling.text.strip()
    except AttributeError:
        price = "Price not found"
    return [price, bs4_object.searched_url]



def disease_search(request):
    if request.method == "POST":
        search = request.POST.get('search')
        url  = 'https://www.britannica.com/science/nutritional-disease'

        html_file = requests.get(url).text
        soup = BeautifulSoup(html_file, "lxml")
        table = soup.find('div', class_ = 'md-drag md-table-wrapper').tbody
        table_rows = table.find_all('tr')

        disease_list = []
        for table_row in table_rows:
            disease_name_and_cause = table_row.find('td', scope = 'row').text.strip().split(' ')
            ddisease_name = disease_name_and_cause[0]
            disease_list.append(ddisease_name)

        frontend_display = dict()
        if search.lower() in disease_list:
            
            for table_row in table_rows:
                disease_name_and_cause = table_row.find('td', scope = 'row').text.strip().split(' ')
                ddisease_name = disease_name_and_cause[0]
                if ddisease_name == search.lower():
                    other_table_data = table_row.find_all('td', scope = '')
                    disease_symptoms = other_table_data[0].text.strip()
                    disease_diet = other_table_data[1].text.strip().split(',')
            
                    food_type = dict()
                    disease_diet_in_database = ()
                    for food_item in disease_diet:
                        food_type[food_item] = [jumia_site_scraping(food_item), emart_site_scraping(food_item), greenspoon_site_scraping(food_item)]
                        for food in food_type:
                            disease_diet_in_database += tuple(food.strip())
                            print(food.strip())
                        print(food_type[food_item])


                    print(disease_diet_in_database)
                    frontend_display = {
                            'search': ddisease_name,
                            'disease_symptoms': disease_symptoms,
                            'disease_diet': disease_diet,
                            'food_type': food_type,
                        }

                    
                    DiseaseSearch.objects.create(disease_name=search, disease_symptoms=disease_symptoms, disease_diet=disease_diet_in_database)
                    

            print(food_type)

        elif DiseaseSearch.objects.filter(disease_name = search.lower()).exists():#count() > 0:
            disease = DiseaseSearch.objects.get(disease_name = search.lower())
            print(disease.disease_diet)
            frontend_display = {
                            'search': f"{search} is not in our database currently",
                            'disease_symptoms': "none",
                            'disease_diet': [],
                            'food_type': [],
                        }
        

        else:
            print('not in database')
            frontend_display = {
                            'search': f"{search} is not in our database currently",
                            'disease_symptoms': "none",
                            'disease_diet': [],
                            'food_type': [],
                        }
        
        return render(request, 'health/details.html', frontend_display)

        
        
    else:
        return render(request, 'health/details.html')




