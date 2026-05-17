"""
base_crawler.py — 모든 크롤러가 상속받는 기본 클래스
"""
import time
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ko-KR,ko;q=0.9",
}


class BaseCrawler:
    """크롤러 공통 기능: HTTP 요청, HTML 파싱, 딜레이"""

    NAME = "base"          # 사이트 식별 이름 (로그용)
    DELAY = 1.5            # 요청 사이 딜레이(초) — 서버 부하 방지

    def fetch(self, url: str, encoding: str = None) -> BeautifulSoup | None:
        """URL에서 HTML을 가져와 BeautifulSoup 객체로 반환"""
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            resp.raise_for_status()
            if encoding:
                resp.encoding = encoding
            return BeautifulSoup(resp.text, "lxml")
        except requests.RequestException as e:
            print(f"  [오류] 요청 실패 ({url}): {e}")
            return None

    def crawl(self) -> list[dict]:
        """각 사이트별로 override 해야 하는 메서드. 공모전 dict 리스트를 반환."""
        raise NotImplementedError

    def sleep(self):
        time.sleep(self.DELAY)

    def run(self) -> list[dict]:
        print(f"\n[START] [{self.NAME}] 크롤링 시작...")
        results = self.crawl()
        print(f"   → {len(results)}건 수집 완료")
        return results
