"""
icpbl.py — 한양대 IC-PBL 센터 새소식 크롤러
대상: http://icpbl.hanyang.ac.kr/?act=board&bbs_code=board-notice
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from base_crawler import BaseCrawler
import re

BASE_URL = "http://icpbl.hanyang.ac.kr"
LIST_URL = f"{BASE_URL}/?act=board&bbs_code=board-notice"
KEYWORDS = ["공모전", "contest", "competition", "대회", "경진"]


def _is_contest(text: str) -> bool:
    return any(kw in text for kw in KEYWORDS)


class IcpblCrawler(BaseCrawler):
    NAME = "IC-PBL 센터"

    def crawl(self) -> list[dict]:
        results = []
        soup = self.fetch(LIST_URL, encoding="utf-8")
        if not soup:
            return results

        rows = soup.select("table tbody tr, .board-list li, ul li")
        for row in rows:
            a_tag = row.select_one("td a, .title a, a[href*='view']")
            if not a_tag:
                continue
            title = a_tag.get_text(strip=True)
            if not title:
                continue
            # 공모전 관련 키워드 필터링
            if not _is_contest(title):
                continue

            href = a_tag.get("href", "")
            if not href.startswith("http"):
                href = BASE_URL + "/" + href.lstrip("/")

            self.sleep()
            detail = self._get_detail(href)
            results.append({
                "title":       title,
                "description": detail.get("description", ""),
                "source_url":  href,
                "apply_url":   href,
                "category":    "ICPBL",
                "targets":     ["재학생"],
                "end_date":    None,
            })

        return results

    def _get_detail(self, url: str) -> dict:
        soup = self.fetch(url, encoding="utf-8")
        if not soup:
            return {}
        content = soup.select_one(".board-content, .view-body, .content, article")
        description = content.get_text(" ", strip=True)[:1000] if content else ""
        return {"description": description}
