import streamlit as st
import os
from datetime import datetime

st.title('메모장')
st.write("""
    * 메모를 작성하고 저장할 수 있는 웹 어플리케이션입니다. 
    * 저장한 메모를 텍스트 파일로 다운로드 받거나 삭제할 수 있습니다. 
    * [스트림릿 클라우드](https://share.streamlit.io)를 이용해서 간단하게 배포할 수 있습니다.
    * 스트림릿 클라우드에서 앱을 reboot하면 파일로 저장한 메모가 모두 삭제됩니다. 왜 그럴까요?
""")

# memo 폴더에서 파일목록을 읽어옵니다.
memo_list = ['새로운 메모'] + os.listdir('memo/')
fn = st.selectbox('메모를 선택하세요.', memo_list)

content = ''
if fn != '새로운 메모':
    # 선택한 메모 내용을 불러옵니다. 
    with open(f'memo/{fn}', 'r', encoding='utf-8') as f:
        content = f.read()

new_content = st.text_area('메모를 입력하세요', content, height=300)
button_label = "메모 작성"
if content != '':
    button_label = "메모 수정"
save_button = st.button(button_label, use_container_width=True)

if content != '':
    # 불러온 메모가 있는 경우, 다운로드 버튼과 삭제 버튼을 표시합니다.
    down_button = st.download_button(label='메모 다운로드', file_name=fn, data=content, use_container_width=True)
    delete_button = st.button('메모 삭제', use_container_width=True)
    if delete_button:
        try:
            os.remove(f'memo/{fn}')
            st.success('메모가 삭제되었습니다.')
        except:
            st.error('메모삭제에 실패했습니다.')

if save_button:
    # save_button을 클릭했을때 동작
    if fn == '새로운 메모':
        # 날짜와 시간을 바탕으로 새로운 메모 파일의 이름을 생성합니다.
        fn = datetime.now().strftime('%Y_%m_%d__%H_%M_%S') + '.txt'

    try:
        with open(f'memo/{fn}', 'w', encoding='utf-8') as f:
            f.write(new_content)
            st.success('저장되었습니다.')
    except:
        st.error('메모저장에 실패했습니다.')

