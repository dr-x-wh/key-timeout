from datetime import date
from typing import Optional, List

from app.extensions import db
from app.models.info import Info


class InfoService:
    @staticmethod
    def get_by_id(info_id: int) -> Optional[Info]:
        info = Info.query.get(info_id)
        if info:
            return info
        return None

    @staticmethod
    def get_by_user_id(user_id: int) -> Optional[List[Info]]:
        infos = Info.query.filter_by(user_id=user_id).all()
        if infos:
            return infos
        return None

    @staticmethod
    def create(user_id: int, name: str, start_date: date, end_date: date, person: Optional[int],
               phone: Optional[int]) -> Optional[Info]:
        info = Info()
        info.user_id = user_id
        info.name = name
        info.start_date = start_date
        info.end_date = end_date
        if person:
            info.person = person
        if phone:
            info.phone = phone
        db.session.add(info)
        db.session.commit()
        db.session.refresh(info)
        if info:
            return info
        return None

    @staticmethod
    def delete_user(info_id: int) -> bool:
        db_info = Info.query.get(info_id)
        if db_info:
            db.session.delete(db_info)
            db.session.commit()
            return True
        return False
