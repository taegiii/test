import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json
# Firebase 서비스 계정 키 파일 경로

key_dict = json.loads(st.secrets["textkey"])

cred = credentials.Certificate(key_dict)  # 서비스 계정 키 파일 경로 설정
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Firestore 클라이언트 초기화
db = firestore.client()

# 퀴즈 정답
correct_answers = {
    'answer1': "KCL",
    'answer2': "KVL",
    'answer3': "sheet off",
    'answer4': "3"
}

# 유저의 점수 계산
def calculate_score(answers):
    score = 0
    for key in correct_answers:
        if answers.get(key) == correct_answers[key]:
            score += 25
    return score

# Firestore에 데이터 저장
def save_user_data(user_data):
    try:
        doc_ref = db.collection('quiz_results').document(user_data['username'])
        doc_ref.set(user_data)
        st.success('결과가 저장되었습니다!')
    except Exception as e:
        st.error(f'Error: {e}')

# 퀴즈 페이지
st.title("퀴즈 페이지")

# 사용자 이름 입력
username = st.text_input("이름을 입력하세요")

# 문제 1
st.write("Q1. 한 점에서 모든 전류의 합이 0이 되야 하는 법칙의 이름은?(25점)")
answer1 = st.radio("보기 중 답을 고르시오.", ["KVL", "KCL", "V=IR", "열평형 법칙", "슈뢰딩거의 파동방정식"], key='first')

# 문제 2
st.write("Q2. 한 점에서 모든 전압의 합이 0이 되야 하는 법칙의 이름은?(25점)")
answer2 = st.radio("보기 중 답을 고르시오.", ["KVL", "KCL", "V=IR", "열평형 법칙", "슈뢰딩거의 파동방정식"], key='second')

# 문제 3
st.write("Q3. Si로 이루어진 웨이퍼에 산화막이 있으면 물이 묻는걸 water sheet이라 한다, 그럼 산화막을 벗기는 현상을 머라하는가?(25점)")
answer3 = st.radio("보기 중 답을 고르시오.", ['water off', 'sheet off', 'sheet on', 'water on', 'wafer off'], key='third')

# 문제 4
st.write("Q4.")
st.image("문제2.png")
st.write("(25점)")
answer4 = st.radio("보기 중 답을 고르시오", ["1", "2", "3", "4"], key="four")

if st.button("제출"):
    if username:
        user_answers = {
            'answer1': answer1,
            'answer2': answer2,
            'answer3': answer3,
            'answer4': answer4
        }
        score = calculate_score(user_answers)
        user_data = {
            'username': username,
            'answers': user_answers,
            'score': score
        }
        save_user_data(user_data)
        st.write(f"{username}님의 점수는 {score}점 입니다.")
    else:
        st.error("이름을 입력하세요.")
