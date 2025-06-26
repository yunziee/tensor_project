# 함수 정의

from datetime import datetime

def calculate_age(birthdate):
    
    birth = datetime.strptime(birthdate, "%Y-%m-%d")
    today = datetime.today()
    age = today.year - birth.year
    # 아직 생일이 안 지났으면 1살 빼기
    if (today.month, today.day) < (birth.month, birth.day):
        age -= 1
    return age

def convert_currency(amount, from_currency, to_currency, rate):
    return round(amount * rate, 2)

def calculate_bmi(height, weight):
    # cm를 m로 변환
    height_m = height / 100 
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)