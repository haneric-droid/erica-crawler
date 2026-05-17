"""
db.py — Supabase 연결 및 공모전 데이터 저장 공통 모듈
"""
import os
from dotenv import load_dotenv
from supabase import create_client, Client
import re

def extract_end_date(text: str) -> str | None:
    if not text:
        return None
    # 2024.05.20, 24-05-20, 2024년 5월 20일 등의 패턴 추출
    pattern = r'(202\d|\d{2})[-./년]\s*(1[0-2]|0?[1-9])[-./월]\s*(3[01]|[12][0-9]|0?[1-9])'
    matches = re.findall(pattern, text)
    if matches:
        # 보통 본문 맨 마지막에 나오는 날짜가 마감일일 확률이 높음
        y, m, d = matches[-1]
        if len(y) == 2:
            y = "20" + y
        return f"{y}-{int(m):02d}-{int(d):02d}"
    return None
from datetime import datetime, timezone

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise EnvironmentError("❌ .env 파일에 SUPABASE_URL 과 SUPABASE_KEY 를 설정해주세요.")

_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_client() -> Client:
    return _client


def upsert_contest(item: dict) -> bool:
    """
    공모전 1건을 DB에 저장.
    source_url 이 이미 존재하면 건너뜀 (중복 방지).
    반환값: True = 새로 삽입됨 / False = 이미 존재 or 오류
    """
    source_url = item.get("source_url", "").strip()
    if not source_url:
        print(f"  [경고] source_url 없음, 건너뜀: {item.get('title')}")
        return False

    try:
        # 중복 체크
        existing = (
            _client.table("contests")
            .select("id")
            .eq("source_url", source_url)
            .execute()
        )
        if existing.data:
            print(f"  [중복] 이미 존재: {item.get('title')[:40]}")
            return False

        # 필수 기본값 보정
        now = datetime.now(timezone.utc).isoformat()
        description = (item.get("description") or "").strip()[:2000]
        end_date = item.get("end_date")
        
        # 날짜 추출기 사용 (명시적 날짜가 없을 경우 본문에서 탐색)
        if not end_date:
            end_date = extract_end_date(description)
            
        # 그래도 못 찾았다면, DB 제약조건(not-null) 위반을 막기 위해 기본값(오늘부터 7일 뒤) 부여
        if not end_date:
            from datetime import timedelta
            end_date = (datetime.now(timezone.utc) + timedelta(days=7)).strftime("%Y-%m-%d")
            
        row = {
            "title":       item.get("title", "").strip()[:200],
            "description": description,
            "source_url":  source_url,
            "apply_url":   (item.get("apply_url") or source_url).strip(),
            "poster_url":  item.get("poster_url"),
            "category":    item.get("category", "교내 공모전"),
            "targets":     item.get("targets", ["재학생"]),
            "start_date":  item.get("start_date"),
            "end_date":    end_date,
            "status":      "draft",
            "created_at":  now,
            "updated_at":  now,
        }

        _client.table("contests").insert(row).execute()
        print(f"  [성공] 저장 완료: {row['title'][:50]}")
        return True

    except Exception as e:
        print(f"  [에러] DB 오류 ({item.get('title', '')[:30]}): {e}")
        return False


def log_crawl_run(source: str, collected: int, inserted: int, error: str = None):
    """크롤링 실행 이력을 crawl_runs 테이블에 저장"""
    try:
        _client.table("crawl_runs").insert({
            "source":    source,
            "collected": collected,
            "inserted":  inserted,
            "error":     error,
            "ran_at":    datetime.now(timezone.utc).isoformat(),
        }).execute()
    except Exception as e:
        print(f"  [경고] crawl_runs 로그 실패 (테이블 없을 수 있음): {e}")
