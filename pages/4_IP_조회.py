import streamlit as st
import pandas
import utils.ip

st.title('IP 국가 조회')
st.write("""
    * IPv4 주소가 어느 국가에 할당되어 있는지 조회하는 웹 어플리케이션입니다.
    * 데이터는 `First IP, Last IP, Country` 형식으로 CSV 파일에 저장되어 있습니다. 
    * 검색하려는 IP주소가 `First` 와 `Last` 범위에 포함된다면, 해당하는 국가코드를 출력합니다.
    * 문자열 데이터는 범위를 확인할 수 없으므로, IP 주소를 숫자 데이터로 변환하는 것이 필요합니다.
    * IPv4 주소는 4바이트(즉 16진수 8자리)로 구성되므로, 아래와 같이 정수형 데이터로 변환이 가능합니다.     
        ```
        IP 주소 => 16진수 => 10진수
        '0.0.0.1' => 0x00000001 => 1
        '1.1.1.1' => 0x01010101 => 16843009
        '1.1.1.255' => 0x010101FF => 16843263
        '255.255.255.255' => 0xFFFFFFFF => 4294967295
        ```
    * 데이터 소스: [IP Geolocation by DB-IP](https://db-ip.com)
""")

@st.cache_data
def load_data():
    csv = pandas.read_csv('data/ipv4-country.csv')
    csv['first'] = csv['first'].map(utils.ip.ip_to_num)
    csv['last'] = csv['last'].map(utils.ip.ip_to_num)
    return csv
    """     
    dataframe['column'].map(function) 
    # 위 코드는 'column'의 각 데이터에 대해 function 함수를 수행합니다. 아래 코드와 동일합니다.
    for i in dataframe['column']:
        function(i) 
    """

user_input = st.text_input('IPv4 주소를 입력하세요')
csv = load_data()
if user_input:
    if utils.ip.is_valid(user_input):
        ip = utils.ip.ip_to_num(user_input)
        country = csv[(csv['first'] <= ip) & (ip <= csv['last'])]
        st.success(country['country'].values[0])
    else:
        st.warning('유효한 IPv4 주소를 입력하세요.')

