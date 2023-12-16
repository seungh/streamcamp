import streamlit as st

spam_list = []

# 스팸목록이 저장된 파일로부터 데이터를 불러옵니다. 
with open('data/spam_list.txt') as f:
    lines = f.readlines()
    for tel in lines:
        spam_list.append(tel.strip())

st.title('스팸조회')
st.write("""
    * 입력한 값이 스팸리스트에 포함되어 있는지 확인하는 웹 어플리케이션입니다. 
    * 검색유형에 따라 입력 값이 유효한 형식인지 확인하는 코드를 직접 작성해보세요. 
    * 스팸 리스트를 어떻게 업데이트 할 수 있을지 생각해보세요.
""")

left, right = st.columns([0.3, 0.7]) # 좌우 칼럼을 3대7 비율로 나눕니다. 

with left:
    search_type = st.selectbox("검색유형을 선택하세요", ('전화번호', '이메일주소', 'IP 주소'))
with right:
    user_input = st.text_input(f'{search_type}를 입력하세요.')


if user_input:
    search = user_input
    if search_type == '전화번호':
        # 1577-0000 형식으로 입력한 전화번호에서 하이픈과 좌우공백을 제거합니다.
        search = user_input.replace('-', '').strip()

    if search in spam_list:
        st.error(f'{user_input} : 입력하신 {search_type}가 스팸목록에 등록되어 있습니다.')
    else:
        st.success(f'{user_input} : 입력하신 {search_type}는 스팸목록에 등록되어 있지 않습니다.')
        st.balloons()

# 체크박스를 클릭하면 스팸목록에 저장된 데이터를 확인합니다. 
data_view = st.checkbox('전체 스팸목록 보기')
if data_view:
    st.dataframe(spam_list, width=800)

