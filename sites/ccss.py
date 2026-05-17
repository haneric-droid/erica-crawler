"""
ccss.py — 한양대 소프트웨어융합대학 공모전 크롤러
대상: https://ccss.hanyang.ac.kr/bbs/board.php?tbl=bbs61&findType=title&findWord=%EA%B3%B5%EB%AA%A8%EC%A0%84
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from base_crawler import BaseCrawler

BASE_URL = "https://ccss.hanyang.ac.kr"
LIST_URL = (
    f"{BASE_URL}/bbs/board.php?tbl=bbs61"
    "&findType=title&findWord=%EA%B3%B5%EB%AA%A8%EC%A0%84"
)


class CcssCrawler(BaseCrawler):
    NAME = "소프트웨어융합대학(ccss)"

    def crawl(self) -> list[dict]:
        results = []
        soup = self.fetch(LIST_URL, encoding="utf-8")
        if not soup:
            return results
        rows = soup.select("table tbody tr")
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
                "category": "소프트웨어융합대학",
                "targets": ["재학생"],
                "end_date": None,
            })
        return results

    def _get_detail(self, url: str) -> dict:
        soup = self.fetch(url, encoding="utf-8")
        if not soup:
            return {}
        content = soup.select_one("#content, .view-content, article")
        description = content.get_text(" ", strip=True)[:1000] if content else ""
        return {"description": description}
