import streamlit as st

answer_index = ['KCL', 'KVL', 'sheet off', '3']
st.session_state.score = 0

for i in range(len(answer_index)):
    if st.session_state[f'answer{i+1}'] == answer_index[i] :
        st.write(f"{i+1}번 문제 정답입니다.")
        st.session_state.score += 25
    else :
        st.write(f"{i+1}번 문제 틀렸습니다.")

st.write(f"총 점수는 {st.session_state.score}/100 입니다.")