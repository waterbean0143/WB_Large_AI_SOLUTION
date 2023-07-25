import streamlit as st
import pandas as pd

def load_data(file):
    data = pd.read_csv(file)
    return data

def main():
    st.title("Quiz App")
    st.write("문항을 풀어보세요.")

    files = {
        "quiz02.csv": "https://github.com/waterbean0143/WB_Large_AI_SOLUTION/raw/main/ComplianceBot/quiz02.csv",
        "quiz03.csv": "https://github.com/waterbean0143/WB_Large_AI_SOLUTION/raw/main/ComplianceBot/quiz03.csv",
        "quiz04.csv": "https://github.com/waterbean0143/WB_Large_AI_SOLUTION/raw/main/ComplianceBot/quiz04.csv",
        "quiz05.csv": "https://github.com/waterbean0143/WB_Large_AI_SOLUTION/raw/main/ComplianceBot/quiz05.csv",
        "quiz06.csv": "https://github.com/waterbean0143/WB_Large_AI_SOLUTION/raw/main/ComplianceBot/quiz06.csv",
        "quiz07.csv": "https://github.com/waterbean0143/WB_Large_AI_SOLUTION/raw/main/ComplianceBot/quiz07.csv",
        "quiz08.csv": "https://github.com/waterbean0143/WB_Large_AI_SOLUTION/raw/main/ComplianceBot/quiz08.csv",
        "quiz09.csv": "https://github.com/waterbean0143/WB_Large_AI_SOLUTION/raw/main/ComplianceBot/quiz09.csv",
        "quiz12.csv": "https://github.com/waterbean0143/WB_Large_AI_SOLUTION/raw/main/ComplianceBot/quiz12.csv",
        "quiz14.csv": "https://github.com/waterbean0143/WB_Large_AI_SOLUTION/raw/main/ComplianceBot/quiz14.csv",
        "quiz16.csv": "https://github.com/waterbean0143/WB_Large_AI_SOLUTION/raw/main/ComplianceBot/quiz16.csv"
    }

    selected_file = st.selectbox("CSV 파일 선택", list(files.keys()))

    if selected_file:
        file_url = files[selected_file]
        data = load_data(file_url)

        total_questions = len(data)  # 전체 문항 수
        user_answers = [None] * total_questions  # 사용자 답변 리스트 초기화

        with st.form("quiz_form"):
            for i in range(total_questions):
                st.write(f"문제 {i+1}/{total_questions}:")
                st.write("문항:", data.loc[i, "문항"])
                user_answers[i] = st.radio("정답을 선택하세요.", options=["O", "X"], key=f"answer_{i}")

                # Create empty explanations for each question
                explanation = st.empty()

        # Display the explanation after the user clicks the "제출" (Submit) button
        if st.form_submit_button("제출"):
            st.write(f"총 {total_questions}문제 중")
            correct_count = 0
            incorrect_questions = []
            for i in range(total_questions):
                if user_answers[i] == data.loc[i, "답안"]:
                    correct_count += 1
                else:
                    incorrect_questions.append(i)

            st.write(f"{correct_count}문제 맞추셨습니다!")

            if incorrect_questions:
                st.write("틀린 문제:")
                for question_num in incorrect_questions:
                    st.write(f"문제 {question_num+1}:")
                    st.write("문항:", data.loc[question_num, "문항"])
                    explanation.text("틀린 이유: " + data.loc[question_num, "해설"])

if __name__ == "__main__":
    main()
