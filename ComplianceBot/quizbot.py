import streamlit as st
import pandas as pd

def load_data(file):
    data = pd.read_csv(file)
    return data

def main():
    st.title("Quiz App")
    st.write("문항을 풀어보세요.")

    files = {
        "2. 청탁금지법": "https://github.com/waterbean0143/WB_Large_AI_SOLUTION/raw/main/ComplianceBot/quiz02.csv",
        "3. 힘/성희롱": "https://github.com/waterbean0143/WB_Large_AI_SOLUTION/raw/main/ComplianceBot/quiz03.csv",
        "4. 회계세무": "https://github.com/waterbean0143/WB_Large_AI_SOLUTION/raw/main/ComplianceBot/quiz04.csv",
        "5. 담합예방": "https://github.com/waterbean0143/WB_Large_AI_SOLUTION/raw/main/ComplianceBot/quiz05.csv",
        "6. 제3위험평가": "https://github.com/waterbean0143/WB_Large_AI_SOLUTION/raw/main/ComplianceBot/quiz06.csv",
        "7. 안전보건": "https://github.com/waterbean0143/WB_Large_AI_SOLUTION/raw/main/ComplianceBot/quiz07.csv",
        "8. 부당특약": "https://github.com/waterbean0143/WB_Large_AI_SOLUTION/raw/main/ComplianceBot/quiz08.csv",
        "9. 재원집행(대가지급)": "https://github.com/waterbean0143/WB_Large_AI_SOLUTION/raw/main/ComplianceBot/quiz09.csv",
        "12. 기술자료 탈취": "https://github.com/waterbean0143/WB_Large_AI_SOLUTION/raw/main/ComplianceBot/quiz12.csv",
        "14. 위장도급": "https://github.com/waterbean0143/WB_Large_AI_SOLUTION/raw/main/ComplianceBot/quiz14.csv",
        "16. 제안센터 정보보안": "https://github.com/waterbean0143/WB_Large_AI_SOLUTION/raw/main/ComplianceBot/quiz16.csv"
    }

    selected_file = st.selectbox("퀴즈 선택", list(files.keys()))

    if selected_file:
        file_url = files[selected_file]
        data = load_data(file_url)

        total_questions = len(data)  # 전체 문항 수
        user_answers = ["미선택"] * total_questions  # 사용자 답변 리스트 초기화
        unanswered_questions = []  # List to store question numbers with "[미선택]" option checked

        incorrect_questions = []
        explanations = []

        with st.form("quiz_form"):
            for i in range(total_questions):
                st.write(f"문제 {i+1}/{total_questions}:")
                st.write("문항:", data.loc[i, "문항"])
                user_answers[i] = st.radio("정답을 선택하세요.", options=["미선택", "O", "X"], key=f"answer_{i}")
                st.write("")  # Add an empty line for spacing

                if user_answers[i] == "미선택":
                    unanswered_questions.append(i+1)
                elif user_answers[i] != data.loc[i, "답안"]:
                    incorrect_questions.append(i+1)
                    explanations.append(data.loc[i, "해설"])

            submitted = st.form_submit_button("제출")  # Move submit button inside the form context

        # Display the explanation after the user clicks the "제출" (Submit) button
        if submitted:
            with st.sidebar:  # Add content to the right sidebar
                if incorrect_questions:
                    st.header("틀린 문제:")
                    st.write(", ".join([f"문제 {q}번" for q in incorrect_questions]))

                    st.header("해설:")
                    for i, explanation in enumerate(explanations):
                        st.write(f"[{incorrect_questions[i]}번 해설] : {explanation}")

                if unanswered_questions:
                    st.warning("[미선택] 항목을 체크한 문제:")
                    st.write(", ".join([f"문제 {q}번" for q in unanswered_questions]))

                if not incorrect_questions and not unanswered_questions:
                    st.write("모든 문제를 정답으로 맞추셨습니다!")

if __name__ == "__main__":
    main()
