from flask import Blueprint

from app.services.info import InfoService
from app.utils.result import Result
from app.utils.security import login_required, UserTools

info_bp = Blueprint("info", __name__, url_prefix="/info")


@info_bp.route("/<int:info_id>", methods=["GET"])
@login_required
def get_info(info_id: int):
    info = InfoService.get_by_id(info_id)
    if info:
        return Result.success(info.to_dict())
    return Result.error()


@info_bp.route("/list", methods=["GET"])
@login_required
def get_infos():
    infos = InfoService.get_by_user_id(UserTools.get_current_user().get('id'))
    if infos:
        return Result.success([info.to_dict() for info in infos])
    return Result.success([])
