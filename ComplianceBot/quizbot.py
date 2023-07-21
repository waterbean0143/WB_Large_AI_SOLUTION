import streamlit as st
import pandas as pd

def load_data():
    data_url = "https://github.com/waterbean0143/WB_Large_AI_SOLUTION/raw/main/ComplianceBot/comp_quiz02.csv"
    data = pd.read_csv(data_url)
    return data

def main():
    data = load_data()
    total_questions = len(data)  # 전체 문항 수

    st.title("Quiz App")
    st.write("문항을 풀어보세요.")

    question_number = st.empty()  # 문항 번호 표시할 빈 컨테이너
    question_text = st.empty()  # 문항 텍스트 표시할 빈 컨테이너
    user_answer = st.empty()  # 사용자 정답 선택할 빈 컨테이너
    feedback_message = st.empty()  # 정답 여부 피드백 표시할 빈 컨테이너

    current_question = 0  # 현재 문항 인덱스

    while current_question < total_questions:
        question_number.write(f"문제 {current_question+1}/{total_questions}:")
        question_text.write("문항:", data.loc[current_question, "문항"])

        if user_answer.button("제출"):  # 제출 버튼 누르면 정답 체크
            if user_answer.radio("정답을 선택하세요.", ("O", "X")) == data.loc[current_question, "답안"]:
                feedback_message.write("정답입니다!")
            else:
                feedback_message.write("틀렸습니다.")
                st.write("해설:", data.loc[current_question, "해설"])

            current_question += 1  # 다음 문항으로 이동

            # 다음 문항으로 이동하기 위한 버튼
            if current_question < total_questions:
                if st.button("다음 문제"):
                    question_number.empty()
                    question_text.empty()
                    user_answer.empty()
                    feedback_message.empty()
            else:
                st.write("모든 문항을 푸셨습니다!")

if __name__ == "__main__":
    main()
