from datetime import date
from typing import Optional, List

from flask import current_app
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
    def get_pagination_by_user_id(query) -> Optional[Pagination]:
        page = query.get('page', 1, type=int)
        per_page = query.get('per_page', 10, type=int)
        desc = query.get('desc', 'true').lower() == 'true'
        order_by = query.get('order_by', 'id')

        qQuery = Info.query

        if name := query.get('name'):
            qQuery = qQuery.filter(Info.name.like(f'%{name}%'))

        if person := query.get('person'):
            qQuery = qQuery.filter(Info.person.like(f'%{person}%'))

        if phone := query.get('phone'):
            qQuery = qQuery.filter(Info.phone.like(f'%{phone}%'))

        if start_date := query.getlist("start_date[]"):
            start_date_0 = date.fromisoformat(start_date[0])
            start_date_1 = date.fromisoformat(start_date[1])
            qQuery = qQuery.filter(Info.start_date.between(start_date_0, start_date_1))

        if end_date := query.getlist("end_date[]"):
            end_date_0 = date.fromisoformat(end_date[0])
            end_date_1 = date.fromisoformat(end_date[1])
            qQuery = qQuery.filter(Info.end_date.between(end_date_0, end_date_1))

        order_field = getattr(Info, order_by)
        if desc:
            order_field = order_field.desc()
        qQuery = qQuery.order_by(order_field)

        return qQuery.paginate(page=page, per_page=per_page, error_out=False)

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
    def update(info_id: int, name: Optional[str], date_range: Optional[List],
               person: Optional[int], phone: Optional[int]) -> Optional[Info]:
        info = Info.query.get(info_id)
        if not info:
            return None
        if name:
            info.name = name
        try:
            if date_range:
                info.start_date = date.fromisoformat(date_range[0])
                info.end_date = date.fromisoformat(date_range[1])
        except ValueError as e:
            current_app.logger.warning(str(e))
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
