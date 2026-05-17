"""
eec.py — 한양대 ERICA 스타트업 라운지 공모전 크롤러
대상: https://eec.hanyang.ac.kr/front/ko/startup-lounge/notice
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from base_crawler import BaseCrawler

BASE_URL = "https://eec.hanyang.ac.kr"
LIST_URL = f"{BASE_URL}/front/ko/startup-lounge/notice"


class EecCrawler(BaseCrawler):
    NAME = "스타트업 라운지(eec)"

    def crawl(self) -> list[dict]:
        results = []
        soup = self.fetch(LIST_URL)
        if not soup:
            return results
        rows = soup.select(".notice-list li, .board-list li, table tbody tr")
        for row in rows:
            a_tag = row.select_one("a")
            if not a_tag:
                continue
            title = a_tag.get_text(strip=True)
            if not title:
                continue
            href = a_tag.get("href", "")
            if not href.startswith("http"):
                href = BASE_URL + href
            self.sleep()
            detail = self._get_detail(href)
            results.append({
                "title": title,
                "description": detail.get("description", ""),
                "source_url": href,
                "apply_url": href,
                "category": "스타트업 라운지",
                "targets": ["재학생"],
                "end_date": None,
            })
        return results

    def _get_detail(self, url: str) -> dict:
        soup = self.fetch(url)
        if not soup:
            return {}
        content = soup.select_one(".view-content, .board-view-content, article")
        description = content.get_text(" ", strip=True)[:1000] if content else ""
        return {"description": description}
