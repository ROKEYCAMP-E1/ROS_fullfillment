import json

# 파일 경로
DATA_FILE = "src/Fullfillment/Fullfillment/UI/utils/user_data.json"


# 사용자 데이터 로드 함수
def load_user_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# 사용자 데이터 저장 함수
def save_user_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)