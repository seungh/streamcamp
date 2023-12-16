import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# introduction
st.title('경기도 편의점 데이터 분석')
st.write("""
    * Streamlit은 데이터 시각화를 위한 파이썬 패키지로, 분석 결과를 웹으로 쉽게 배포할 수 있도록 도와줍니다.
    * 기본으로 제공하는 라이브러리를 이용해서 간단한 차트와 그래프를 그릴 수 있고, Matplotlib 이나 Plotly 등 기존에 존재하는 강력한 분석도구를 이용할 수도 있습니다.
    * 스트림릿을 이용해서 경기도 편의점 현황 데이터를 분석해봅시다.
    * 데이터소스: [경기도 데이터 분석포털](https://data.gg.go.kr/portal/data/service/selectServicePage.do?infId=CPMB3F3D1SDTN6V7LTWE13467194&infSeq=1&loc=)
""")

# Data loading is a time-consuming task. You can import performance by using cache. Read the link below for more information.
# https://docs.streamlit.io/library/advanced-features/caching
data = pd.read_csv('data/data.csv', encoding='cp949')
data = data.drop(['다중이용업소여부', '총시설규모(㎡)', '위생업종명', '위생업태명', '소재지지번주소'], axis=1) # Remove unnecessary columns using drop() method.
data['인허가일자'] = pd.to_datetime(data['인허가일자'], format='mixed')
data['폐업일자'] = pd.to_datetime(data['폐업일자'], format='mixed')

# print data frame
st.subheader('RAW DATA')
st.dataframe(data)

# draw bar graph
st.subheader('도시별 편의점 수')
stores_city = data.value_counts('시군명')
st.bar_chart(stores_city)

# draw map scatter
st.subheader('편의점 분포')
st.map(data.dropna(), latitude='WGS84위도', longitude='WGS84경도', size=1) # dropna() method removes missing values.

c1,c2 = st.columns(2)

# analyze store closure
with c1:
    st.subheader('영업상태')
    closure_stats = data.value_counts('영업상태명')

    fig = px.pie(values=closure_stats.values, names=closure_stats.index, hole=0.3, width=300)
    st.plotly_chart(fig, names='엽업현황', title='엽업현황', use_container_width=True)

# analyze brand statistics
with c2:
    st.subheader('브랜드')
    # Brand information is not included in the raw data. Therefore, we need to look for brand info in the '사업자명' column.
    brand_info = {
        'CU': ['씨유', 'CU'],
        'GS25': ['지에스', 'GS'],
        '세븐일레븐': ['세븐', 'seven'],
        '미니스톱': ['미니'],
        '이마트24': ['이마트', 'emart'],
    }
    brand_stats = {}
    for i in brand_info:
        conditions = data['사업장명'].str.contains('|'.join(brand_info[i]))
        cnt = data['사업장명'][conditions].count()
        brand_stats[i] = cnt
    brand_stats['기타'] = data['사업장명'].count() - sum(brand_stats.values())

    fig = px.pie(values=brand_stats.values(), names=brand_stats.keys(), hole=0.3, width=300)
    st.plotly_chart(fig, names='브랜드현황', title='브랜드현황', use_container_width=True)


# open/closure statistic
st.subheader('개업/폐업 추이')

# filter raw data by selected brands
selected_brands = st.multiselect("Display only selected brands", brand_info.keys())
search_keywords = []
for i in selected_brands:
    search_keywords += brand_info[i]
conditions = data['사업장명'].str.contains('|'.join(search_keywords))
filtered_data = data.loc[conditions]

# draw chart of open/close statistics
data_by_year = pd.DataFrame()
data_by_year['인허가 수'] = filtered_data['인허가일자'].dt.year.value_counts()
data_by_year['폐업 수'] = filtered_data['폐업일자'].dt.year.value_counts()
data_by_year.index.name = '년도'
data_by_year.index = data_by_year.index.astype("str")
data_by_year = data_by_year.fillna(0)
st.area_chart(data_by_year)

