"""
run_all.py — 모든 정적 크롤러를 순차 실행하고 Supabase에 저장
"""
import os
import sys
from pathlib import Path

# 프로젝트 루트 (crawlers 폴더 기준)
ROOT = Path(__file__).parent
sys.path.append(str(ROOT))

from db import upsert_contest, log_crawl_run

# 각 크롤러 임포트
from sites.idesign import IdesignCrawler
from sites.ibus import IbusCrawler
from sites.global_center import GlobalCenterCrawler
from sites.icpbl import IcpblCrawler
from sites.eec import EecCrawler
from sites.computing import ComputingCrawler
from sites.ccss import CcssCrawler
from sites.lan_cul import LanCulCrawler

CRAWLERS = [
    IdesignCrawler(),
    IbusCrawler(),
    GlobalCenterCrawler(),
    IcpblCrawler(),
    EecCrawler(),
    ComputingCrawler(),
    CcssCrawler(),
    LanCulCrawler(),
]

def main():
    total_collected = 0
    total_inserted = 0
    for crawler in CRAWLERS:
        items = crawler.run()
        total_collected += len(items)
        for item in items:
            if upsert_contest(item):
                total_inserted += 1
    log_crawl_run(
        source="static_phase",
        collected=total_collected,
        inserted=total_inserted,
    )
    print(f"\n[완료] 전체 수집 {total_collected}건, 신규 삽입 {total_inserted}건 완료")

if __name__ == "__main__":
    main()
