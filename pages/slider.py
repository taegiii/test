import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase 서비스 계정 키 파일 경로
cred = credentials.Certificate('secret_key.json')

# Firebase 초기화 (이미 초기화된 경우 건너뛰기)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Firestore 클라이언트 초기화
db = firestore.client()

# Firestore에 사용자 데이터 추가
def add_user_to_firestore(user_data):
    try:
        doc_ref = db.collection('users').document(user_data['username'])
        doc_ref.set(user_data)
        st.success('회원가입이 완료되었습니다!')
    except Exception as e:
        st.error(f'Error: {e}')

# Firestore에서 사용자 데이터 확인
def verify_user(username, password):
    try:
        doc_ref = db.collection('users').document(username)
        doc = doc_ref.get()
        if doc.exists:
            user_data = doc.to_dict()
            if user_data['password'] == password:
                return True
        return False
    except Exception as e:
        st.error(f'Error: {e}')
        return False

# Streamlit 앱
st.title("회원관리 시스템")

# 탭 설정
tabs = st.tabs(["회원가입", "로그인"])

# 회원가입 양식
with tabs[0]:
    with st.form(key='signup_form'):
        username = st.text_input("사용자 이름", max_chars=20)
        email = st.text_input("이메일")
        password = st.text_input("비밀번호", type="password")
        confirm_password = st.text_input("비밀번호 확인", type="password")
        
        submit_button = st.form_submit_button(label='회원가입')

        if submit_button:
            if password != confirm_password:
                st.error("비밀번호가 일치하지 않습니다.")
            else:
                user_data = {
                    'username': username,
                    'email': email,
                    'password': password
                }
                add_user_to_firestore(user_data)

# 로그인 양식
with tabs[1]:
    with st.form(key='login_form'):
        username = st.text_input("사용자 이름")
        password = st.text_input("비밀번호", type="password")
        
        login_button = st.form_submit_button(label='로그인')

        if login_button:
            if verify_user(username, password):
                st.success('로그인 성공!')
            else:
                st.error('로그인 실패. 사용자 이름 또는 비밀번호를 확인하세요.')
