# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 15:49:27 2020

@author: Owner
"""

from wordcloud import WordCloud
import numpy as np
import pandas as pd
import nltk
#nltk.download()
#conda update nltk
import re
import os
import matplotlib.pyplot as plt
from PIL import Image                         # Pillow 패키지의 영상 핸들링 클래스.
import matplotlib 
from IPython.display import set_matplotlib_formats
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
%matplotlib inline
from wordcloud import WordCloud
## 입력값 제거 함수
def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]

## Path

os.chdir(r'C:\Users\Owner\Desktop\Minnie\project\project_intel\네트워크_그래프')
## 파일 불러오기
test=pd.read_excel('삼성카드.xlsx')


n_min = 2                                                           # 최소 문자 개수. 
corpus = []
#lemmatizer = WordNetLemmatizer()
for a_line in test['title']:
    pre = re.sub(r'\W', ' ', a_line)                                # 특수문자 제외.
    pre = re.sub(r'_', ' ', pre)                                    # 특수문자 제외.
    pre = re.sub(r'\d+','', pre)                                    # 수자 제외. 
    pre = nltk.word_tokenize(pre)
    pre = [x for x in pre if len(x) > n_min]                        # 최소 길이 충족.
    corpus +=pre                                                 # 단어를 말뭉치에 추가.


## 입력값 제거
x = remove_values_from_list(corpus, '삼성카드')
x = remove_values_from_list(x, '삼성')
x = remove_values_from_list(x, '카드')



# Series 로 변환.
my_series = pd.Series(x)

# 도수 분포표. Top 10
my_word_counts = my_series.value_counts().sort_values(ascending=False)
my_word_counts[:10]

#################################################################
my_words_2 = [""]
for a_word in x:
    if len(a_word) > 1:
        my_words_2[0] += " " + a_word
        
# 도수 분포표. Top 20
my_word_counts = my_series.value_counts().sort_values(ascending=False)
my_word_counts[:10]


#################### 2-gram 

from sklearn.feature_extraction.text import CountVectorizer
n = 2                                                            # Can be changed to a number equal or larger than 2.
n_min = n
n_max = n
n_gram_type = 'word'                                             # n-Gram with words.
vectorizer = CountVectorizer(ngram_range=(n_min,n_max), analyzer = n_gram_type)

n_grams = vectorizer.fit(my_words_2).get_feature_names()            # Get the n-Grams as a list.
n_gram_cts = vectorizer.transform(my_words_2).toarray()             #  The output is an array of array.
n_gram_cts = list(n_gram_cts[0])         

res_dict = {}
for z, zz in zip(n_grams, n_gram_cts):
    res_dict[z] = zz

list_resdict = sorted(res_dict.items(), key=(lambda x: x[1]), reverse=True)
#res_dict[:30]

##########################################################################
#######################################################
###### 쪼개기

test=[]
for i in range(len(list_resdict)):
    pre=list_resdict[i][0]
    pre = pre.split(" ")
    test.append((pre[0],pre[1],list_resdict[i][1]))

relation_word=pd.DataFrame(test,columns=['word1','word2','count'])
#relation_dict=dict(test)

word_50=relation_word[:50]
word_20=relation_word[:20]
word_10=relation_word[:10]

#relation_word2['word1']
########################################################
#########################################################
## 네트워크 분석    
import networkx as nx #% 라이브러리를 nx로 불러오기
import matplotlib.pyplot as plt # plt로 불러오기

G = nx.Graph() # 빈 그래프 구조 G 생성
### 1) 노드 정의 & 속성 부여
#### 중복 제거해야할듯
du_word1=set(list(word_50['word1']))

for word in word_50['word1']:
    G.add_node(word)
# 확인
G.node()
G.nodes(data=True)

### 2) 엣지(링크) 정의
for i in range(len(word_50)):
    G.add_edge(word_50['word1'][i],word_50['word2'][i],color='r')

G.edges() #엣지들 보기
G.edges(data=True)

degree = nx.degree(G)

############################## 그래프 설정
import networkx as nx
import matplotlib.pyplot as plt

# 힌글 폰트
import matplotlib.font_manager as fm
font_name=fm.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()

%matplotlib qt

#### 색 지정 필요
count_color =[c for w,c in degree ]
count_color=sorted(set(count_color),reverse=True)

my_color={28:'#FF1744',5:'#ff5777',4:'#ffbdca',3:'#ffbdca',2:'#ffbdca',1:'#BDBDBD'}
#my_color={16:'#FF1744',12:'#FF1744',9:'#ff5777',8:"#ff8aa0",4:'#ffbdca',3:'#ffbdca',2:'#ffbdca',1:'#BDBDBD'}

       
############# 실행 type 2
pos=nx.draw_random(G)
           
fig, ax = plt.subplots()
nx.draw_networkx(G, font_family=font_name, font_size=20,node_shape='*',
                 pos=pos,font_weight='bold',font_color='w',
                 node_size=[v*100 for k,v in degree],
                 edge_color='gray',
                 node_color=[my_color[v] for k,v in degree if my_color[v]],
                 alpha=0.9,cmap=plt.cm.YlGn)
ax.set_facecolor("#00000F")
ax.axis('off')
fig.set_facecolor("#00000F")
plt.show()
