import numpy as np
import pandas as pd
import os

#제목,본문 저장된 위치
os.chdir(r"C:\Users\Gram\Desktop\네이버지식인카드불편사항\2. 네이버지식인 본문\5-2. 제목, 본문 저장")

#수정할 파일 이름
data = pd.read_excel("국민카드 신한카드_본문.xlsx")

#필요한 열 이름
title = data['title']
content = data['content']

#수정
for i in range(len(title)):
    if pd.isnull(content[i]):
        content[i]=title[i]

#수정본 이름
save_name='국민카드 신한카드_본문(완)'

#제목빼고 본문만 저장
content_df=pd.DataFrame(content)

#최종 저장
content_df.to_excel(save_name+".xlsx")