import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import csv
import openai

openai.api_key="use-your-api-key"

def read_csv(file_path):
    data = []
    with open(file_path, "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # 첫 번째 행(헤더)은 건너뜁니다.
        for row in reader:
            subject = row[0]  # 제목은 A열에 해당합니다.
            body = row[1]  # 본문은 B열에 해당합니다.
            link = row[2]  # 링크는 C열에 해당합니다.

            # 메일 본문 형식으로 정리합니다.
            data.append(f"<h2>{subject}</h2><p>{body}</p><p><a href='{link}'>링크 바로가기</a></p>")

    return "\n".join(data)  # 리스트에 있는 데이터를 줄바꿈으로 연결하여 문자열로 반환

def gpt_summarize(text):
    # system instruction = "assistant는 user의 입력을 bullet point로 3줄 요약된다."
    system_instruction = "assistant는 user의 입력을 30자로 요약해준다."

    messages = [{"role": "system", "content": system_instruction},{"role":"user","content":text}]

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    result = response['choices'][0]['message']['content']
    return result

def send_email(subject, body, to_email, attachment_path):
    # 보내는 사람 이메일 계정 정보
    from_email = "sbbae123@naver.com"  # 발송자 이메일 주소
    password = "sbbaehebron77"  # 발송자 이메일 계정 비밀번호

    # 이메일 설정
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = ", ".join(to_email)  # 수신자 이메일 주소들을 콤마로 구분하여 문자열로 변환
    msg["Subject"] = subject

    # 이메일 본문 추가 (HTML 형식)
    body_part = MIMEText(body, "html")
    msg.attach(body_part)

    # 첨부 파일 추가
    with open(attachment_path, "rb") as file:
        part = MIMEApplication(file.read(), Name="attachment")
        part["Content-Disposition"] = f"attachment; filename={attachment_path}"
        msg.attach(part)

    # SMTP 서버 연결
    smtp_server = "smtp.naver.com"
    smtp_port = 587
    try:
        smtp_conn = smtplib.SMTP(smtp_server, smtp_port)
        smtp_conn.starttls()  # TLS 보안 연결
        # 로그인
        smtp_conn.login(from_email, password)

        # 이메일 발송
        smtp_conn.sendmail(from_email, to_email, msg.as_string())

        print("이메일이 성공적으로 발송되었습니다.")
    except smtplib.SMTPException as e:
        print("이메일 발송 중 오류가 발생했습니다:", e)
    finally:
        # SMTP 연결 종료
        smtp_conn.quit()

if __name__ == "__main__":
    subject = "[파이뉴스] 트렌드 3줄 요약 공유"
    file_path = "/Users/dowankim/Downloads/ai-news.csv"  # CSV 파일 경로 입력
    attachment_path = "/Users/dowankim/Downloads/tooning.zip"  # 첨부 파일 경로 입력

    # CSV 파일 읽기
    body = read_csv(file_path)

    # 텍스트 요약
    summarized_body = gpt_summarize(body)

    to_email_list = ["waterbean.bae@kt.com"]  # 여러 명의 수신자 이메일 주소들을 리스트로 저장

    for to_email in to_email_list:
        send_email(subject, summarized_body, [to_email], attachment_path)  # 수신자 이메일 주소를 리스트로 변환하여 함수 호출
