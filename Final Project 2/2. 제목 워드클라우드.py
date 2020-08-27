#처음엔 설치 필요!
#!pip install wordcloud
#!pip install nltk

# 다음은 한번만 실행한다.
from wordcloud import WordCloud
import numpy as np
import pandas as pd
import nltk
nltk.download()
conda update nltk
import re
import os
import matplotlib.pyplot as plt
from PIL import Image                         # Pillow 패키지의 영상 핸들링 클래스.
import matplotlib 
from IPython.display import set_matplotlib_formats
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
%matplotlib inline

## 입력값 제거 함수
def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]

## Path
os.chdir(r'C:\Users\Gram\Desktop\네이버지식인\1. 네이버지식인 제목\2. 카드별 네이버 지식인 제목 크롤링 결과')

## 파일 불러오기
test=pd.read_excel("카카오페이카드.xlsx")

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
x = remove_values_from_list(corpus, '카카오페이카드')
x = remove_values_from_list(x, '카카오페이')
x = remove_values_from_list(x, '카카오')
x = remove_values_from_list(x, '카드를')


# Series 로 변환.
my_series = pd.Series(x)

# 도수 분포표. Top 10
my_word_counts = my_series.value_counts().sort_values(ascending=False)
my_word_counts[:20]

# 다음은 워드클라우드의 요구사항.
## 한글 폰트 설정
import matplotlib
matplotlib.rc('font',family = 'Malgun Gothic') 
# 폰트 선명하게
set_matplotlib_formats('retina') 
# 그래프 음수 수치 오류 방지
matplotlib.rc('axes',unicode_minus = False)

##### max_words 설정!
max_words = 200

a_long_sentence = ' '.join(x)
wc = WordCloud(font_path = 'C:/Windows/Fonts/malgun.ttf',background_color='white',  max_words=max_words,max_font_size=300)              # 바탕색, 단어 개수 등 설정.
wc.generate(a_long_sentence)
wc.words_


plt.figure(figsize=(10,10))
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")                                    # 축을 꺼줌.
plt.show()



"""
# 백그라운드 마스크
#img = Image.open('background_1.png')                    # 타원형.
#img = Image.open('background_2.png')                   # 말풍선.
img = Image.open('background_3.png')                    # 하트.
back_mask = np.array(img)

wc = WordCloud(background_color='white', max_words=30, mask=back_mask)            # 바탕색, 단어 개수 등 설정.
wc.generate(a_long_sentence) 

plt.figure(figsize=(10,10))
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")                                    # 축을 꺼줌.
plt.show()
"""

