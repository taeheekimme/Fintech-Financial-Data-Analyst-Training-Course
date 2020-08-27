import os
from selenium import webdriver
import bs4,re
import pandas as pd
import numpy as np
import time

#크롬드라이버, 링크엑섹 저장위치
os.chdir(r'C:\Users\Gram\Desktop\네이버지식인카드불편사항\2. 네이버지식인 본문\4-2. 링크 저장')

#검색 키워드
search='국민카드설계사'
save_name="국민카드설계사_본문"

driver2 = webdriver.Chrome("./chromedriver")
re_excel=pd.read_excel(search+".xlsx")

#제목,본문 저장할 리스트 생성
title=[]
content=[]


#크롤링 시작
for link in re_excel['link']:
    driver2.get(link)
    
    #제목저장
    driver2.find_elements_by_css_selector("div#content")
    subject=driver2.find_element_by_css_selector("div.question-content>div>div>div>div>div.title")
    title.append(subject.text)
    time.sleep(1)
   
    #본문저장
    try:
        subject=driver2.find_element_by_css_selector("div.question-content>div>div>div.c-heading__content")
        content.append(subject.text)
    except:
        content.append('')


#중복제거 코드
re_data = []
for i in range(len(title)):
    re_data.append((title[i],content[i]))

re_data=set(re_data)


#저장하기
df_data=pd.DataFrame(re_data,columns=['title','content'])
save_doc={"title":df_data['title'],"content":df_data['content']}
df_news=pd.DataFrame(save_doc,columns=["title","content"])
df_news.to_excel(save_name+".xlsx")


