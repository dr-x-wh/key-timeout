from flask import Flask

from app.extensions import db
from app.models.setting import Setting
from app.services.setting import SettingService


def init_data(app: Flask) -> None:
    with app.app_context():
        notice_phone = Setting.query.filter_by(name="notice_phone").first()
        if not notice_phone:
            new_notice_phone = Setting()
            new_notice_phone.name = "notice_phone"
            db.session.add(new_notice_phone)

        notice_time = Setting.query.filter_by(name="notice_time").first()
        if not notice_time:
            new_notice_time = Setting()
            new_notice_time.name = "notice_time"
            db.session.add(new_notice_time)

        db.session.commit()
