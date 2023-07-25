import streamlit as st
import pandas as pd

def load_data(file):
    data = pd.read_csv(file)
    return data

def noCopyPaste():
    # Custom CSS styles to disable text selection and copying
    custom_css = '''
    <style>
    body {
        user-select: none;
        -webkit-user-select: none;
        -moz-user-select: none;
    }
    </style>
    '''

    # Render the custom CSS styles
    st.markdown(custom_css, unsafe_allow_html=True)

def main():
    noCopyPaste()  # Call the noCopyPaste function to disable text selection and copying

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
        user_answers = [None] * total_questions  # 사용자 답변 리스트 초기화

        with st.form("quiz_form"):
            for i in range(total_questions):
                st.write(f"문제 {i+1}/{total_questions}:")
                st.write("문항:", data.loc[i, "문항"])
                user_answers[i] = st.radio("정답을 선택하세요.", options=["미선택", "O", "X"], key=f"answer_{i}")

            submitted = st.form_submit_button("제출")

        if submitted:
            st.write(f"총 {total_questions}문제 중")
            correct_count = 0
            incorrect_questions = []
            for i in range(total_questions):
                if user_answers[i] == "미선택":
                    incorrect_questions.append(i+1)
                elif user_answers[i] == data.loc[i, "답안"]:
                    correct_count += 1
                else:
                    incorrect_questions.append(i+1)

            if len(incorrect_questions) == 0:
                st.write("정답을 모두 맞추셨습니다!")
            else:
                st.write(f"[미선택]이 체크되어있는 문제 {', '.join(map(str, incorrect_questions))}번을 안풀었습니다.")

            if len(incorrect_questions) > 0:
                st.write("틀린 문제 및 해설:")
                for question_num in incorrect_questions:
                    st.write(f"문제 {question_num}:")
                    st.write("문항:", data.loc[question_num-1, "문항"])
                    st.write(f"[{question_num}번 해설]:", data.loc[question_num-1, "해설"])

if __name__ == "__main__":
    main()
