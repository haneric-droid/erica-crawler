"""
scheduler.py — 크롤러 정기 자동 실행 스크립트
"""
import schedule
import time
import subprocess
import os
from datetime import datetime

# run_all.py 파일의 절대 경로
SCRIPT_PATH = os.path.join(os.path.dirname(__file__), 'run_all.py')

def job():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"\n[{now}] 🤖 정기 크롤링 작업을 시작합니다...")
    
    try:
        # run_all.py를 실행
        subprocess.run(["python", SCRIPT_PATH], check=True)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ 크롤링 작업 성공적으로 완료됨.")
    except subprocess.CalledProcessError as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ 크롤링 작업 중 오류 발생: {e}")

# 스케줄 등록
# 1) 매일 오전 9시에 실행
schedule.every().day.at("09:00").do(job)
# 2) 매일 오후 3시에 실행
schedule.every().day.at("15:00").do(job)

# (테스트용) 주석을 풀면 프로그램을 켜자마자 1회 먼저 실행합니다.
# job()

print("=========================================")
print("🕒 공모전 자동 크롤링 스케줄러가 시작되었습니다.")
print("  - 실행 주기: 매일 09:00, 15:00")
print("  - 이 창을 켜두시면 자동으로 수집합니다.")
print("  - 종료하시려면 [Ctrl + C]를 누르세요.")
print("=========================================")

while True:
    schedule.run_pending()
    time.sleep(60) # 1분마다 스케줄 확인할 시간이 되었는지 체크
