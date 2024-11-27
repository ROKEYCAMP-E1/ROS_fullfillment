import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re

def is_valid_email(email):
    """이메일 주소가 유효한지 확인"""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def send_email(receiver_email, subject, message):
    """이메일 전송 함수"""
    sender_email = "kim3he@naver.com"
    sender_password = "Rlagml5125248!"  # 네이버 비밀번호

    # 이메일 주소 유효성 검증
    if not is_valid_email(receiver_email):
        print(f"잘못된 이메일 주소: {receiver_email}")
        return

    try:
        # 이메일 메시지 생성
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # SMTP 서버 설정 및 이메일 전송
        with smtplib.SMTP('smtp.naver.com', 587) as server:
            server.starttls()  # TLS 암호화 시작
            server.login(sender_email, sender_password)  # SMTP 서버 로그인
            server.sendmail(sender_email, receiver_email, msg.as_string())  # 이메일 전송
            print("이메일이 성공적으로 발송되었습니다!")
    except smtplib.SMTPAuthenticationError:
        print("SMTP 인증 오류: 이메일 계정 및 비밀번호를 확인하세요.")
    except smtplib.SMTPRecipientsRefused:
        print("수신자 이메일 주소가 거부되었습니다.")
    except smtplib.SMTPException as e:
        print(f"SMTP 관련 오류 발생: {e}")
    except Exception as e:
        print(f"이메일 발송 중 알 수 없는 오류 발생: {e}")