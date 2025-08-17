from datetime import date
from typing import Optional

from flask_sqlalchemy.pagination import Pagination

from app.extensions import db
from app.models.info import Info


class InfoService:
    @staticmethod
    def get_by_id(info_id: int) -> Optional[Info]:
        info = Info.query.get(info_id)
        if not info:
            return None
        return info

    @staticmethod
    def get_pagination_by_user_id(user_id: int, page: int, per_page: int) -> Optional[Pagination]:
        return Info.query.paginate(page=page, per_page=per_page, error_out=False)

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
    def update(info_id: int, name: Optional[str], start_date: Optional[date], end_date: Optional[date],
               person: Optional[int], phone: Optional[int]) -> Optional[Info]:
        info = Info.query.get(info_id)
        if not info:
            return None
        if name:
            info.name = name
        if start_date:
            info.start_date = start_date
        if end_date:
            info.end_date = end_date
        if person:
            info.person = person
        if phone:
            info.phone = phone
        db.session.commit()
        db.session.refresh(info)
        if info:
            return info
        return None

    @staticmethod
    def delete_info(info_id: int) -> bool:
        db_info = Info.query.get(info_id)
        if db_info:
            db.session.delete(db_info)
            db.session.commit()
            return True
        return False
