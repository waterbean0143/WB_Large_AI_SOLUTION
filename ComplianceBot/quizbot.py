import streamlit as st
import pandas as pd

def load_data():
    # CSV 파일을 로드합니다.
    data = pd.read_csv("comp_quiz.csv")
    return data

def main():
    # 데이터 로드
    data = load_data()

    # Streamlit 앱 구성
    st.title("Quiz App")
    st.write("문항 번호를 입력하여 문제를 풀어보세요.")

    # 시트 이름과 문항 번호 입력
    sheet_name = st.text_input("시트 이름을 입력하세요.")
    question_number = st.text_input("문항 번호를 입력하세요.")

    if sheet_name and question_number:
        # 문제 가져오기
        question = get_question(sheet_name, question_number, data)

        if not question.empty:
            st.write("문제:", question["문항"].values[0])

            # OX 버튼 생성
            user_answer = st.radio("정답을 선택하세요.", ("O", "X"))

            # 정답 확인
            if user_answer == question["답안"].values[0]:
                st.write("정답입니다!")
            else:
                st.write("틀렸습니다.")
                st.write("해설:", question["해설"].values[0])
        else:
            st.write("문항을 찾을 수 없습니다.")

if __name__ == "__main__":
    main()
