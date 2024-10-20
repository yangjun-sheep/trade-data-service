# 下载标题及文件链接

import requests
import time
from datetime import datetime, date

from sqlmodel import Session

from app.core.db import engine
from app.crud import CRUDAnnouncement
from app.models import AnnouncementCreate
from app.enums import DataSourceEnum


def _fetch(sse_date: str, sse_date_end: str, page: int):
    # sse_date: 2024-10-18 00:00:00
    # sse_date_end: 2024-10-18 23:59:59
    url = "https://query.sse.com.cn/commonSoaQuery.do"
    params = {
        'isPagination': True,
        'pageHelp.pageSize': 25,
        'pageHelp.cacheSize': 1,
        'type': 'inParams',
        'sqlId': 'BS_ZQ_GGLL',
        'sseDate': sse_date,
        'sseDateEnd': sse_date_end,
        'securityCode': '',
        'title': '',
        'orgBulletinType': '',
        'bondType': 'CORPORATE_BOND_BULLETIN,COMPANY_BOND_BULLETIN',
        'order': 'sseDate|desc,securityCode|asc,bulletinId|asc',
        'pageHelp.pageNo': page,
        'pageHelp.beginPage': page,
        'pageHelp.endPage': page,
        '_': int(time.time() * 1000)
    }
    headers = {
        'Referer': 'https://www.sse.com.cn/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }
    response = requests.get(url, params=params, headers=headers)
    return response


def run(day: date | None = None):
    print(f"[sse]开始执行任务，时间：{datetime.now()}")
    session = Session(engine)
    crud_announcement = CRUDAnnouncement(session)
    if day is None:
        day = datetime.now().date()
    print(f'[sse] day: {day}')
    unique_keys = crud_announcement.get_unique_keys(day, DataSourceEnum.SSE.value)
    sse_date = datetime.combine(day, datetime.min.time()).strftime('%Y-%m-%d %H:%M:%S')
    sse_date_end = datetime.combine(day, datetime.max.time()).strftime('%Y-%m-%d %H:%M:%S')
    page = 1
    try:
        for page in range(1, 1000):
            response = _fetch(sse_date, sse_date_end, page)
            data = response.json()
            total_page = data['pageHelp']['pageCount']
            result = data['result']
            for item in result:
                unique_key = item['url']
                if unique_key in unique_keys:
                    break
                announcement_create = AnnouncementCreate(
                    code=item['securityCode'],
                    title=item['title'],
                    abbr=item['securityAbbr'],
                    url='https://static.sse.com.cn/' + item['url'],
                    type=item['bulletinType'],
                    publish_date=day,
                    source_key=unique_key,
                    source=DataSourceEnum.SSE.value
                )
                crud_announcement.create(announcement_create)

            if page >= total_page:
                break

            page += 1

    except Exception as e:
        print(e)
        # TODO 记录下来，重新执行，先不实现了

    print('[sse]任务执行完毕')
