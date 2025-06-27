import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import time

# streamlit 앱이 브라우저의 전체 너비를 사용
st.set_page_config(layout="wide")

# .env 파일에서 OPENAI API KEY 불러오기
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)

import base64

# 이미지 첨부를 위한 base64 문자열 변환 함수
def img_to_base64(img_path):
    with open(img_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# 사용자/봇 프로필 이미지 변환
user_img_b64 = img_to_base64("datas/ganadi_user.png")
bot_img_b64 = img_to_base64("datas/ganadi_bot.png")

# 카카오톡 느낌의 CSS..
st.markdown("""
<style>
.stApp {
    background: #dbe6e4;
}
.chat-container {
    width: 100%;     
    max-width: 750px; 
    margin: 0 auto; 
    padding: 0 8px; 
}
.bubble-row {
    display: flex;
    align-items: flex-end;
    margin-bottom: 10px;
}
.bubble-avatar {
    width: 44px;
    height: 44px;
    border-radius: 50%%;
    margin: 2px 10px 2px 2px;
    object-fit: cover;
    box-shadow: 0 1px 8px #bbcfde30;
}
.bubble-user {
    background: #fff578;
    color: #222;
    border-radius: 15px 15px 3px 15px;
    padding: 13px 18px;
    font-size: 1.0em;
    display: inline-block;
    max-width: 600px; 
    margin-left: auto;
    margin-right: 3px;
    box-shadow: 2px 2px 7px #efe8b6b0;
    word-break: break-word;
    white-space: pre-line;
    text-align: left;
}
.bubble-bot {
    background: #fff;
    color: #222;
    border-radius: 15px 15px 15px 3px;
    padding: 13px 18px;
    font-size: 1.0em;
    display: inline-block;
    max-width: 600px; 
    margin-right: auto;
    margin-left: 3px;
    box-shadow: 2px 2px 7px #bbcfde80;
    word-break: break-word;
    white-space: pre-line;
    text-align: left;
}
.user-row {
    justify-content: flex-end;
}
.bot-row {
    justify-content: flex-start;
}
.nickname {
    font-size: 0.93em;
    color: #49787a;
    font-weight: bold;
    margin-left: 10px;
    margin-bottom: 3px;
}
</style>
""", unsafe_allow_html=True)

# 상단에 봇 프로필 이미지와 타이틀 표시
cols = st.columns([1, 7])
with cols[0]:
    st.image("datas/ganadi_bot.png", width=100)
with cols[1]:
    st.markdown("<h3>Chat Ganadi</h3>", unsafe_allow_html=True)

st.divider()

# 세션 상태에 모델명 및 메시지 리스트가 없으면 초기화
if 'openai_model' not in st.session_state:
    st.session_state.openai_model = 'gpt-4.1'

if 'messages' not in st.session_state:
    st.session_state.messages = []

# 말풍선 렌더링 함수
def render_msg(msg, is_user):
    # 사용자 true/false에 따라 스타일 적용
    if is_user:
        # # 사용자 메시지: 오른쪽 정렬, 노란색 버블, 사용자 아바타
        st.markdown(f"""
        <div class="bubble-row user-row">
            <div class="bubble-user">{msg["content"]}</div>
            <img class="bubble-avatar" src="data:image/png;base64,{user_img_b64}" />
        </div>
        """, unsafe_allow_html=True)
    else:
        # 봇 메시지: 왼쪽 정렬, 흰색 버블, 봇 아바타, 닉네임
        st.markdown(f"""
        <div class="bubble-row bot-row">
            <img class="bubble-avatar" src="data:image/png;base64,{bot_img_b64}" />
            <div>
               <div class="nickname">가나디</div>
               <div class="bubble-bot">{msg["content"]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# 타자 효과로 출력(bubble 내 타이핑)
def typing_bubble(content, is_user, delay=0.015):
    bubble_area = st.empty()
    text_shown = ""
    for c in content:
        text_shown += c
        if is_user:
            bubble_area.markdown(f"""
            <div class="bubble-row user-row">
                <div class="bubble-user">{text_shown}</div>
                <img class="bubble-avatar" src="data:image/png;base64,{user_img_b64}" />
            </div>
            """, unsafe_allow_html=True)
        else:
            bubble_area.markdown(f"""
            <div class="bubble-row bot-row">
                <img class="bubble-avatar" src="data:image/png;base64,{bot_img_b64}" />
                <div>
                    <div class="nickname">가나디</div>
                    <div class="bubble-bot">{text_shown}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        time.sleep(delay) # 여기서 타자 효과

# 채팅 입력창 및 메시지 처리
if prompt:= st.chat_input("가나디에게 물어보기"):
    # 먼저 이전 메시지들 + 사용자 입력 보여 주기
    for msg in st.session_state.messages:
        render_msg(msg, is_user=(msg["role"]=="user"))
    render_msg({"role": "user", "content": prompt}, is_user=True)

    system_prompt = (
        "너의 이름은 '가나디'야. 사용자가 '가나디'라고 부르면 너를 부르는 거야."
        """
        챗봇 설정: 너는 가나디라는 귀엽고 어리숙한 강아지 캐릭터 챗봇이다. 
        가나디는 질문에 올바르고 정확한 답을 하며, 지식이나 정보는 틀리지 않는다. 
        다만 답변을 할 때마다 바보 같고 억울하며 어리숙한 느낌을 풍기며, 
        가끔 말 끝에는 "멍...", "킁킁...", "그치만..." 같은 말을 붙이거나 억울한 기색을 보인다. 
        사람을 착하고 순수하게 돕는다.
    """
    )

    # 전체 메시지 리스트 생성 (시스템 프롬프트 + 이전 대화 + 이번 입력)
    messages = [{"role": "system", "content": system_prompt}]
    messages += [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages]
    messages.append({"role": "user", "content": prompt})

    # gpt 답변 구하기
    with st.spinner("가나디가 생각 중..."):
        stream = client.chat.completions.create(
            model=st.session_state.openai_model,
            messages=messages,
            stream=True
        )
        response_text = ""
        for chunk in stream:
            token = chunk.choices[0].delta.content or ""
            response_text += token

        # 답변 한 글자씩 타자 효과 출력
        typing_bubble(response_text, is_user=False)

        # 대화창을 위해 최종적으로 세션에 메시지 저장
        st.session_state.messages.append({"role":"user", "content":prompt})
        st.session_state.messages.append({"role":"assistant", "content":response_text})

else:
    # 프롬프트가 없을 때(=대기상태) 기존 메시지 모두 렌더링
    for msg in st.session_state.messages:
        render_msg(msg, is_user=(msg["role"]=="user"))
