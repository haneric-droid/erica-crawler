"""
idesign.py — 한양대 ERICA 디자인대학 공모전 크롤러
대상: http://idesign.hanyang.ac.kr/bbs/board.php?bo_table=notice&sca=공모전
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from base_crawler import BaseCrawler

BASE_URL = "http://idesign.hanyang.ac.kr"
LIST_URL = f"{BASE_URL}/bbs/board.php?bo_table=notice&sca=%EA%B3%B5%EB%AA%A8%EC%A0%84"


class IdesignCrawler(BaseCrawler):
    NAME = "디자인대학(idesign)"

    def crawl(self) -> list[dict]:
        results = []
        soup = self.fetch(LIST_URL, encoding="utf-8")
        if not soup:
            return results

        rows = soup.select("div#game_board ul.bo_list li, table.bd_list tbody tr")
        # gnuboard 스타일 게시판
        articles = soup.select("div#bo_list .tbl_head01 tbody tr, ul#bo_list_ul li, .list_body tr")
        if not articles:
            articles = soup.select("tr")

        for row in articles:
            a_tag = row.select_one("td.td_subject a, .bo_tit a, a[href*='wr_id']")
            if not a_tag:
                continue
            title = a_tag.get_text(strip=True)
            if not title or title in ("제목", ""):
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
                "category":    "교내 공모전",
                "targets":     ["재학생"],
                "end_date":    detail.get("end_date"),
            })

        return results

    def _get_detail(self, url: str) -> dict:
        soup = self.fetch(url, encoding="utf-8")
        if not soup:
            return {}
        content_div = soup.select_one("div#bo_v_con, div.bo_v_body, div.view_content")
        description = content_div.get_text(" ", strip=True)[:1000] if content_div else ""
        return {"description": description}
