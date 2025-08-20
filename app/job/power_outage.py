import logging
from datetime import datetime

from app import create_app
from app.services.setting import SettingService
from app.services.notice import NoticeService
from app.utils.sms_tools import send_sms
from app.utils.web_tools import get_web_notice

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def run() -> None:
    with create_app().app_context():
        get_list()
        send()


def get_list() -> None:
    notice_list = get_web_notice()
    notice_list.reverse()
    if notice_list:
        for notice in notice_list:
            NoticeService.create(notice["title"], notice["date"])


def send() -> None:
    notice_time = SettingService.get_value_by_key("notice_time")
    notice_phone = SettingService.get_value_by_key("notice_phone")
    if notice_time and notice_phone and str(datetime.now().hour) == notice_time:
        notices = NoticeService.get_job()
        items = [item.to_dict() for item in notices]
        for item in items:
            if send_sms(notice_phone, f"""
            {item["title"]}
            {item["release_date"]}
            """.strip()):
                NoticeService.state_finish(item.get("id"))
