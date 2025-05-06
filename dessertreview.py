import pandas as pd
import re
from konlpy.tag import Okt
from collections import Counter

# 1. 데이터 불러오기
df = pd.read_excel("./크롤링/kurly_data/attije_rollcake_all_reviews.xlsx")
df = df.drop_duplicates(subset='후기내용').dropna(subset=['후기내용']).copy()

# 2. 형태소 분석기
okt = Okt()

# 3. 명사만 추출
# 한글(가-힣) 과 공백(\s) 만 남기고 나머지 특수문자, 숫자, 영어 등은 모두 제거
def extract_nouns(text):
    text = re.sub(r'[^가-힣\s]', '', str(text))
    return [n for n in okt.nouns(text) if len(n) > 1]

# 4. 주요 품사(Verb, Adjective, Adverb) 추출
def extract_selected_pos(text, allowed=['Verb', 'Adjective', 'Adverb']):
    text = re.sub(r'[^가-힣\s]', '', str(text))
    tagged = okt.pos(text, stem=True)           ## 형태소 분석해서 단어와 품사를 뽑는다. 그리고 원형으로 복원(stem=True).
    return [word for word, tag in tagged if tag in allowed and len(word) > 1]

# 5. 전체 리뷰에 대해 처리
all_nouns = []
all_selected_pos = []

for review in df['후기내용']:
    all_nouns.extend(extract_nouns(review))
    all_selected_pos.extend(extract_selected_pos(review))

# 6. 상위 100개 빈도 출력
noun_counts = Counter(all_nouns).most_common(100)
selected_pos_counts = Counter(all_selected_pos).most_common(100)

# 결과 출력
print("📌 자주 등장한 명사 Top 100:")
for i, (word, count) in enumerate(noun_counts, 1):
    print(f"{i}. {word} ({count}회)")

print("\n📌 자주 등장한 동사/형용사/부사 Top 100:")
for i, (word, count) in enumerate(selected_pos_counts, 1):
    print(f"{i}. {word} ({count}회)")
