import streamlit as st
import pandas as pd

def load_data(file):
    data = pd.read_csv(file)
    return data

def main():
    st.title("Quiz App")
    st.write("문항을 풀어보세요.")

    files = {
        "2. 청탁금지법": "quiz02.csv",
        "3. 힘/성희롱": "quiz03.csv",
        "4. 회계세무": "quiz04.csv",
        "5. 담합예방": "quiz05.csv",
        "6. 제3위험평가": "quiz06.csv",
        "7. 안전보건": "quiz07.csv",
        "8. 부당특약": "quiz08.csv",
        "9. 재원집행(대가지급)": "quiz09.csv",
        "12. 기술자료 탈취": "quiz12.csv",
        "14. 위장도급": "quiz14.csv",
        "16. 제안센터 정보보안": "quiz16.csv"
    }

    selected_text = st.selectbox("문항을 선택하세요.", list(files.keys()))

    if selected_text:
        selected_file = files[selected_text]
        file_url = f"https://github.com/waterbean0143/WB_Large_AI_SOLUTION/raw/main/ComplianceBot/{selected_file}"
        data = load_data(file_url)

        total_questions = len(data)  # 전체 문항 수
        user_answers = [None] * total_questions  # 사용자 답변 리스트 초기화

        with st.form("quiz_form"):
            for i in range(total_questions):
                st.write(f"문제 {i+1}/{total_questions}:")
                st.write("문항:", data.loc[i, "문항"])
                user_answers[i] = st.radio("정답을 선택하세요.", options=["O", "X"], key=f"answer_{i}")

                # Display incorrect answers only after the form is submitted
                if st.form_submit_button("제출"):
                    if user_answers[i] != data.loc[i, "답안"]:
                        st.write("해설:", data.loc[i, "해설"])

        # After the form is submitted, show the result and incorrect questions.
        st.write(f"총 {total_questions}문제 중")
        correct_count = 0
        incorrect_questions = []
        for i in range(total_questions):
            if user_answers[i] == data.loc[i, "답안"]:
                correct_count += 1
            else:
                incorrect_questions.append(i+1)

        st.write(f"{correct_count}문제 맞추셨습니다!")

        if len(incorrect_questions) > 0:
            st.write("틀린 문제:")
            for question_num in incorrect_questions:
                st.write(f"문제 {question_num}:", data.loc[question_num-1, "문항"])
                st.write("해설:", data.loc[question_num-1, "해설"])

if __name__ == "__main__":
    main()
