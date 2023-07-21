import streamlit as st
import pandas as pd

def load_data(file):
    data = pd.read_csv(file)
    return data

def main():
    st.title("Quiz App")
    st.write("문항을 풀어보세요.")

    file = st.file_uploader("CSV 파일 선택", type=["csv"])

    if file is not None:
        data = load_data(file)

        total_questions = len(data)  # 전체 문항 수
        user_answers = [None] * total_questions  # 사용자 답변 리스트 초기화

        with st.form("quiz_form"):
            for i in range(total_questions):
                st.write(f"문제 {i+1}/{total_questions}:")
                st.write("문항:", data.loc[i, "문항"])
                user_answers[i] = st.radio("정답을 선택하세요.", options=["O", "X"], key=f"answer_{i}")

            submitted = st.form_submit_button("제출")

        if submitted:
            st.write(f"총 {total_questions}문제 중")
            correct_count = 0
            for i in range(total_questions):
                if user_answers[i] == data.loc[i, "답안"]:
                    correct_count += 1
                else:
                    st.write(f"문제 {i+1} 틀렸습니다.")
                    st.write("해설:", data.loc[i, "해설"])

            st.write(f"{correct_count}문제 맞추셨습니다!")

if __name__ == "__main__":
    main()
