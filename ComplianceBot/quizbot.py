import streamlit as st
import pandas as pd

def load_data():
    data_url = "https://github.com/waterbean0143/WB_Large_AI_SOLUTION/raw/main/ComplianceBot/comp_quiz02.csv"
    data = pd.read_csv(data_url)
    return data

def main():
    data = load_data()

    st.title("Quiz App")
    st.write("문항 번호를 입력하여 문제를 풀어보세요.")

    question_number = st.text_input("문항 번호를 입력하세요.")

    if question_number:
        question = data.loc[int(question_number)-65]  # 문항 번호에 해당하는 데이터 가져오기

        st.write("문제:", question["문항"])

        # O, X 버튼 생성
        user_answer = st.radio("정답을 선택하세요.", ("O", "X"), index=None)

        if user_answer is not None:
            if user_answer == question["답안"]:
                st.write("정답입니다!")
            else:
                st.write("틀렸습니다.")
                st.write("해설:", question["해설"])

if __name__ == "__main__":
    main()
