import streamlit as st
import pandas
import utils.ip

st.title('IP 정보 조회')
st.write("""
    * 입력한 IPv4 주소의 구체적인 지리정보를 조회하는 어플리케이션입니다. 
    * CSV 파일에는 `first IP, last IP, continent, country, state or province, city, latitute, longtitude` 형식으로 데이터가 저장되어 있습니다.
    * 데이터 파일의 사이즈가 220MB으로 크기 때문에, 파일에서 데이터를 로딩해오는데 상당히 오래 걸립니다. 어떻게 하면 데이터를 빠르게 불러오고 성능을 높일 수 있을지 생각해보세요.
    * 데이터 소스: [IP Geolocation by DB-IP](https://db-ip.com)
""")

@st.cache_data(ttl="7d", show_spinner=False)
def load_data():
    # csv_data = pandas.read_csv('data/ipv4-geo.csv') 
    # github 파일 크기 제한으로 원본 데이터를 3개로 분리시켰습니다.
    csv_data = pandas.concat([
        pandas.read_csv('data/ipv4-geo-1.csv'),
        pandas.read_csv('data/ipv4-geo-2.csv'),
        pandas.read_csv('data/ipv4-geo-3.csv'),    
    ], ignore_index=True, sort=True)
    csv_data['first'] = csv_data['first'].map(utils.ip.ip_to_num)
    csv_data['last'] = csv_data['last'].map(utils.ip.ip_to_num)
    return csv_data

with st.spinner('CSV 파일에서 데이터를 읽어오고 있습니다..'):
    csv_data = load_data()

user_input = st.text_input('IPv4 주소를 입력하세요')
if user_input:
    if utils.ip.is_valid(user_input) == False:
        st.warning('IPv4 주소 형식으로 입력하세요.')
    else:
        ip = utils.ip.ip_to_num(user_input)
        row = csv_data[(csv_data['first'] <= ip) & (ip <= csv_data['last'])]
        st.dataframe(
            row[['continent', 'country', 'state', 'city', 'latitude', 'longtitude']], 
            hide_index=True, 
            use_container_width=True)
        st.map(row, latitude='latitude', longitude='longtitude')


st.divider()
st.write("""
🚫 검색 코드를 아래와 같이 구현하면, 검색하려는 IP 주소에 따라 검색 속도가 매우 느려지는 문제가 발생합니다. 무엇이 원인인지 생각해보세요. 
그리고 pandas를 사용하지 않고 어떻게 검색 성능을 높일 수 있는지 생각해보세요.
""")
st.code("""
ip_search = st.text_input('ip address')
ip = utils.ip.ip_to_num(ip_search)
for idx,row in csv_data.iterrows():
    # IP 주소가 first와 last 범위에 포함되는지 확인
    if row['first'] <= ip and ip <= row['last']:
        st.write(row)
""")

