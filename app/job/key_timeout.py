from datetime import datetime
from typing import List, Dict

from app import create_app
from app.extensions import logger
from app.services.info import InfoService
from app.services.user import UserService
from app.utils.sms_tools import send_sms


def run() -> None:
    logger.info("run_key_timeout")
    data_list = get_list()
    for data in data_list:
        if send_sms(data['from_phone'], f"""
        {data['name']}
        {data['end_date']}
        {data['person']}
        {data['phone']}
        """.strip()):
            send_finish(data["id"])


def get_list() -> List[Dict]:
    try:
        with create_app().app_context():
            infos = InfoService.get_job()
            result = []
            for info in infos:
                info = info.to_dict()
                user = UserService.get_by_id(info['user_id']).to_dict()
                remind_time = user["remind_time"]
                if remind_time is None:
                    remind_time = "10"
                if remind_time != str(datetime.now().hour):
                    continue
                info = info | {"from_phone": user["phone"]}
                result.append(info)
        return result
    except Exception as e:
        logger.warning(str(e))
        return []


def send_finish(info_id: int) -> None:
    try:
        with create_app().app_context():
            InfoService.state_finish(info_id)
    except Exception as e:
        logger.warning(str(e))
