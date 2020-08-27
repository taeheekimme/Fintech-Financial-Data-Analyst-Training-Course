import os
from selenium import webdriver
import bs4,re
import pandas as pd
import numpy as np
import time

#크롬드라이버 위치
os.chdir(r'C:\Users\Gram\Desktop\네이버뉴스 립스틱효과')

driver1 = webdriver.Chrome("./chromedriver")

#검색 키워드
search_list = ['구독','책','핫플레이스','휴가비']     #교양오락문화생활비
search="구독"

#검색 사이트 주소
driver1.get("https://search.naver.com/search.naver?where=news&query="+search+"&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=3&ds=2017.11.01&de=2018.05.01&docid=&nso=so%3Ar%2Cp%3Afrom20171101to20180501%2Ca%3Aall&mynews=0&refresh_start=0&related=0")

#크롤링 시작
page=0
title_text=[]
while(True):
        
    html = driver1.page_source
    soup = bs4.BeautifulSoup(html, 'html.parser')
    
    if page == 1:
        page+=2
    else:
        page+=1
        
    # 뉴스 헤드라인
    atags=soup.select('._sp_each_title')
    for atag in atags:
        title_text.append(atag.text)
        
    ## 페이지 넘기기 ## 
    # try except 사용하기 while문 추가하기
    try:
        driver1.find_element_by_css_selector("a.next").click()
    except:
        break
    
    
#저장하기
news={"title":title_text}

df_news=pd.DataFrame(news,columns=['title'])

df_news.to_excel(search+".xlsx")
