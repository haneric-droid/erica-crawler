"""
global_center.py — 한양대 ERICA 국제처 공모전 크롤러
대상: https://global.hanyang.ac.kr/bbs/board.php?bo_table=s4_1&stx=공모전
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from base_crawler import BaseCrawler

BASE_URL = "https://global.hanyang.ac.kr"
LIST_URL = (
    f"{BASE_URL}/bbs/board.php?bo_table=s4_1"
    "&sop=and&sfl=wr_subject%7C%7Cwr_content&stx=%EA%B3%B5%EB%AA%A8%EC%A0%84"
)


class GlobalCenterCrawler(BaseCrawler):
    NAME = "국제처(global)"

    def crawl(self) -> list[dict]:
        results = []
        soup = self.fetch(LIST_URL, encoding="utf-8")
        if not soup:
            return results

        # gnuboard 스타일
        rows = soup.select(".tbl_head01 tbody tr, table tbody tr")
        for row in rows:
            a_tag = row.select_one("td.td_subject a, .bo_tit a")
            if not a_tag:
                continue
            title = a_tag.get_text(strip=True)
            if not title:
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
                "category":    "대외활동",
                "targets":     ["재학생"],
                "end_date":    None,
            })

        return results

    def _get_detail(self, url: str) -> dict:
        soup = self.fetch(url, encoding="utf-8")
        if not soup:
            return {}
        content = soup.select_one("#bo_v_con, .bo_v_body")
        description = content.get_text(" ", strip=True)[:1000] if content else ""
        return {"description": description}
