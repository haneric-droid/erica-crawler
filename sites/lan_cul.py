"""
lan_cul.py — 한양대 언어문화교육원 공모전 크롤러
대상: https://lan-cul.hanyang.ac.kr/bbs/board.php?tbl=bbs71&findWord=%EA%B3%B5%EB%AA%A8%EC%A0%84
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from base_crawler import BaseCrawler

BASE_URL = "https://lan-cul.hanyang.ac.kr"
LIST_URL = (
    f"{BASE_URL}/bbs/board.php?tbl=bbs71"
    "&findWord=%EA%B3%B5%EB%AA%A8%EC%A0%84"
)


class LanCulCrawler(BaseCrawler):
    NAME = "언어문화교육원(lan_cul)"

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
                "category": "언어문화교육원",
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
