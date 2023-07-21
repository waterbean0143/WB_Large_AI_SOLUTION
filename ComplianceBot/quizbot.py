import streamlit as st
import pandas as pd

def load_data():
    data_url = "https://github.com/waterbean0143/WB_Large_AI_SOLUTION/raw/main/ComplianceBot/comp_quiz02.csv"
    data = pd.read_csv(data_url)
    return data

def main():
    data = load_data()

    st.title("Quiz App")
    st.write("문항을 풀어보세요.")

    total_questions = len(data)  # 전체 문항 수
    correct_count = 0  # 정답 개수
    wrong_questions = []  # 틀린 문항 번호

    for i, question in data.iterrows():
        st.write(f"문제 {i+1}/{total_questions}:")
        st.write("문항:", question["문항"])

        # O, X 버튼 생성
        user_answer = st.radio("정답을 선택하세요.", ("O", "X"))

        if user_answer == question["답안"]:
            st.write("정답입니다!")
            correct_count += 1
        else:
            st.write("틀렸습니다.")
            st.write("해설:", question["해설"])
            wrong_questions.append(i+65)  # 틀린 문항 번호 저장

        st.write("---")

    st.write("모든 문항을 푸셨습니다!")
    st.write("정답 개수:", correct_count)
    st.write("틀린 문항 번호:", wrong_questions)

if __name__ == "__main__":
    main()
