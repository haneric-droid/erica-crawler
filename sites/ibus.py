"""
ibus.py — 한양대 ERICA 경상대학 공모전 크롤러
대상: https://ibus.hanyang.ac.kr/front/community/notice?keyword=공모전
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from base_crawler import BaseCrawler

BASE_URL = "https://ibus.hanyang.ac.kr"
LIST_URL = (
    f"{BASE_URL}/front/community/notice"
    "?BoardArticleSearch%5Bkeyword%5D=%EA%B3%B5%EB%AA%A8%EC%A0%84"
)


class IbusCrawler(BaseCrawler):
    NAME = "경상대학(ibus)"

    def crawl(self) -> list[dict]:
        results = []
        soup = self.fetch(LIST_URL)
        if not soup:
            return results

        # 게시판 목록 링크 수집
        items = soup.select("table tbody tr, ul.board-list li, .board_list li")
        if not items:
            items = soup.select("tr")

        for row in items:
            a_tag = row.select_one("a[href*='notice'], td.subject a, .title a, a")
            if not a_tag:
                continue
            title = a_tag.get_text(strip=True)
            if not title or len(title) < 3:
                continue

            href = a_tag.get("href", "")
            if not href or href == "#":
                continue
            if not href.startswith("http"):
                href = BASE_URL + href

            self.sleep()
            detail = self._get_detail(href)
            results.append({
                "title":       title,
                "description": detail.get("description", ""),
                "source_url":  href,
                "apply_url":   href,
                "category":    "교내 공모전",
                "targets":     ["재학생"],
                "end_date":    None,
            })

        return results

    def _get_detail(self, url: str) -> dict:
        soup = self.fetch(url)
        if not soup:
            return {}
        content = soup.select_one(".view-content, .board-view-content, .content, article")
        description = content.get_text(" ", strip=True)[:1000] if content else ""
        return {"description": description}
