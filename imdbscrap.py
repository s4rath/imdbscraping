# Sarath Sreedhar 
#  29/11/2021
# For Educational Purpose
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import requests 
import time 
class search():  
    driver= webdriver.Chrome()
    driver.get('https://www.imdb.com/')
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="nav-search-form"]/div[1]/div/label/div').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="navbar-search-category-select-contents"]/ul/a[7]').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="main"]/div[2]/div[1]/a').click()
    time.sleep(1)
    driver.maximize_window()
    feature_film=driver.find_element_by_xpath('//*[@id="title_type-1"]')
    feature_film.click()
    tv_movie=driver.find_element_by_xpath('//*[@id="title_type-2"]')
    tv_movie.click()
    year_from=driver.find_element_by_xpath('//*[@id="main"]/div[3]/div[2]/input[1]')
    year_from.send_keys('1990')
    year_to=driver.find_element_by_xpath('//*[@id="main"]/div[3]/div[2]/input[2]')
    year_to.send_keys('2020')
    rating_from=driver.find_element_by_xpath('//*[@id="main"]/div[4]/div[2]/select[1]/option[2]')
    rating_from.click()
    rating_to=driver.find_element_by_xpath('//*[@id="main"]/div[4]/div[2]/select[2]/option[91]')
    rating_to.click()
    oscar_nominated=driver.find_element_by_xpath('//*[@id="groups-7"]')
    oscar_nominated.click()
    color_film=driver.find_element_by_xpath('//*[@id="colors-1"]')
    color_film.click()
    english_film=driver.find_element_by_xpath('//*[@id="languages"]/div[2]/select/option[80]')
    english_film.click()
    total_page=driver.find_element_by_xpath('//*[@id="search-count"]/option[3]')
    total_page.click()
    submit=driver.find_element_by_xpath('//*[@id="main"]/p[3]/button')
    submit.click()
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, 200)")
    driver.execute_script("window.scrollTo(200, 600)")
    #driver.execute_script("window.scrollTo(40, 60)")
    current_url=driver.current_url
    driver.close()

search()
url=search.current_url
title_name_list=[]
movie_year_list=[]
movie_nbr_list=[]
movie_certificate_list=[]
movie_rating_list=[]
movie_genre_list=[]
movie_runtime_list=[]
movie_metascore_list=[]
movie_director_list=[]
movie_actor_list=[]
movie_votes_list=[]
movie_gross_list=[]
def moviescrap():
    html_txt= requests.get(url).text
    soup=BeautifulSoup(html_txt,'lxml')
    movie_liststag=soup.find('div',class_='lister-list')
    movie_listtags=movie_liststag.find_all('div',class_='lister-item mode-advanced')
    for movie_listtag in movie_listtags:
        movie_listtagcontent=movie_listtag.find('div',class_='lister-item-content')
        #lower_deck=movie_listtagcontent.find('div',class_='text-muted ')
        gross_section=movie_listtagcontent.find('p',class_='sort-num_votes-visible')
        movie_votes=int(gross_section.find('span',class_='text-muted').find_next('span').text.replace(',',''))
        movie_votes_list.append(movie_votes)
        if gross_section.find('span', class_='text-muted', text='Gross:') is not None:
            movie_gross=gross_section.find('span', class_='text-muted', text='Gross:').find_next('span').text
            movie_gross_list.append(movie_gross)
        else:
            movie_gross_list.append('NA')
        movie_director=movie_listtagcontent.find('p',class_='').a.text
        movie_director_list.append(movie_director)
        movie_actors_=movie_listtagcontent.find('p',class_='')
        movie_actor=movie_actors_.find('span',class_='ghost').find_next('a').text
        movie_actor_list.append(movie_actor)
        movie_metascore=int(movie_listtagcontent.find('div',class_='inline-block ratings-metascore').span.text)
        movie_metascore_list.append(movie_metascore)
        movie_runtime=movie_listtagcontent.find('span',class_='runtime').text
        movie_runtime_list.append(movie_runtime)
        if movie_listtagcontent.find('span',class_='certificate').text is not None:
            movie_certificate=movie_listtagcontent.find('span',class_='certificate').text
            movie_certificate_list.append(movie_certificate)
        else:
            movie_certificate_list.append('NA')
        movie_rating=float(movie_listtagcontent.find('div',class_='inline-block ratings-imdb-rating').strong.text)
        movie_rating_list.append(movie_rating)
        movie_genre=movie_listtagcontent.find('span',class_='genre').text.replace('\n','')
        movie_genre_list.append(movie_genre)
        header=movie_listtagcontent.find('h3',class_='lister-item-header')
        movie_nbr=int(header.find('span',class_='lister-item-index unbold text-primary').text.replace('.',''))
        movie_nbr_list.append(movie_nbr)
        movie_year=header.find('span',class_='lister-item-year text-muted unbold').text
        movie_year_cleaned=int(movie_year[-5:-1])
        movie_year_list.append(movie_year_cleaned)
        title_name=header.find('a').text
        title_name_list.append(title_name)
moviescrap()


def panda_scrap():
    panda_scrap.movie_data={ "Movie Title": title_name_list,
    "Year":movie_year_list,
    "Certificate":movie_certificate_list,
    "Rating":movie_rating_list,
    "Genre":movie_genre_list,
    "Runtime":movie_runtime_list,
    "Metascore":movie_metascore_list,
    "Director":movie_director_list,
    "Actor":movie_actor_list,
    "Votes":movie_votes_list,
    "Gross":movie_gross_list}
    panda_scrap.data=pd.DataFrame(panda_scrap.movie_data,index=movie_nbr_list)
    print(panda_scrap.data)
    
panda_scrap()
print(panda_scrap.data.info()) 
print(panda_scrap.data.loc[78])