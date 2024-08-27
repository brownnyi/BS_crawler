import requests
from bs4 import BeautifulSoup

i = 0

url = 'https://www.inven.co.kr/search/maple/article/%ED%97%88%EB%93%A4/1'
resp = requests.get(url)
soup = BeautifulSoup(resp.content, 'html.parser')

print(soup)

--------------------------------------------
results = []

for i in range(1, 50):
    url = 'https://www.inven.co.kr/search/maple/article/%ED%97%88%EB%93%A4/' + str(i) 
#스크랩을 원하는 사이트 링크를 확인하고 페이지의 변경 방식이 어떻게 변하는지 보고 바꿀 것
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')


    for item in soup.find_all('li', class_='item'):
    # target="_blank"가 있는 <a> 태그의 href 값 추출
        link_tag = item.find('a', target='_blank')
        if link_tag:
            link = link_tag['href']
        # <p class="caption">의 내용 추출
            caption_tag = item.find('p', class_='caption')
            caption = caption_tag.text if caption_tag else ''
            results.append(caption)

-----------------------------------------------
#나온 contents 들을 통해 wordcloud로 시각화
import re
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk

# 불용어 리스트 불러오기
nltk.download('stopwords')
from nltk.corpus import stopwords

# 불필요한 기호와 숫자 제거하고 소문자로 변환
cleaned_text = ' '.join(results).lower()
cleaned_text = re.sub(r'[^\w\s]', '', cleaned_text)  # 구두점 제거
cleaned_text = re.sub(r'\d+', '', cleaned_text)  # 숫자 제거

# 단어 리스트로 변환
word_list = cleaned_text.split()

# 불용어 제거
# 간단한 한국어 불용어 리스트
stop_words = set([
    '이', '그', '저', '에서', '의', '가', '을', '를', '에', '은', '는', '와', '과', '도', '으로', '하다'
, '허들', '허들이','허들을','허들은','수','너무','더','좀','많이','너무','결국','차','다','허들도','근데','있는','진짜','그냥','이제'])

filtered_words = [word for word in word_list if word not in stop_words]


# 단어 빈도 계산
word_freq = Counter(filtered_words)

# 가장 많이 등장한 상위 10개 단어 추출
common_words = word_freq.most_common(10)

# 1. 워드클라우드 시각화
wordcloud = WordCloud(font_path='NEXONLv1GothicRegular.ttf', width=800, height=400, background_color='white').generate_from_frequencies(word_freq)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

# 2. 막대 그래프 시각화
words, counts = zip(*common_words)
plt.bar(words, counts)
plt.xlabel('Words')
plt.ylabel('Frequency')
plt.title('Top 10 Most Frequent Words')
plt.xticks(rotation=45)
plt.show()
