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

        incorrect_questions = []
        explanations = []

        with st.form("quiz_form"):
            for i in range(total_questions):
                st.write(f"문제 {i+1}/{total_questions}:")
                st.write("문항:", data.loc[i, "문항"])
                user_answers[i] = st.radio("정답을 선택하세요.", options=["O", "X"], key=f"answer_{i}")

                if user_answers[i] != data.loc[i, "답안"]:
                    incorrect_questions.append(f"문제 {i+1}")
                    explanations.append(data.loc[i, "해설"])

            submitted = st.form_submit_button("제출")  # Move submit button inside the form context

        # Display the explanation after the user clicks the "제출" (Submit) button
        if submitted:
            with st.sidebar:  # Add content to the right sidebar
                if incorrect_questions:
                    st.header("틀린 문제:")
                    st.write("\n".join(incorrect_questions))

                    st.header("해설:")
                    st.write("\n".join(explanations))
                else:
                    st.write("모든 문제를 정답으로 맞추셨습니다!")

if __name__ == "__main__":
    main()
