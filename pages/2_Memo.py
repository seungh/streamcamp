import streamlit as st
import os
from datetime import datetime

st.title('Memo')

memo_list = ['새로운메모'] + os.listdir('memo/')
fn = st.selectbox('메모를 선택하세요.', memo_list)

content = ''
if fn != '새로운메모':
    with open(f'memo/{fn}', 'r', encoding='utf-8') as f:
        content = f.read()
else:
    fn = datetime.now().strftime('%Y_%m_%d__%H_%M_%S') + '.txt'

txt = st.text_area('메모를 작성하세요.', value=content)

left, right = st.columns(2)
with left:
    button = st.button('저장하기', use_container_width=True)
with right:
    down_button = st.download_button('다운로드', data=txt, file_name=fn, use_container_width=True)

if button:
    try:
        with open(f'memo/{fn}', 'w', encoding='utf-8') as f:
            f.write(txt)
            st.success('메모가 저장되었습니다.')    
    except Exception as e:
        st.error('저장에 실패했습니다.', e)
