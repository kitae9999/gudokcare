import firebase_admin
from firebase_admin import credentials

# Firebase 서비스 계정 키 파일 경로
cred = credentials.Certificate("gudokcare/src/gudokcare-firebase-adminsdk-kfnxs-9ef63c472e.json")

# Firebase Admin 초기화
firebase_admin.initialize_app(cred)