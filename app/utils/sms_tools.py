import base64
import hashlib
import json
import logging
import os

from dotenv import load_dotenv
from zeep import Client

logger = logging.getLogger("sms")
logger.setLevel(level=logging.INFO)


def send_sms(phone: str, text: str) -> bool:
    logger.info(f"send sms: {phone} and {text}")
    return send(phone, text)


def get_sha(input_str):
    sha1_hash = hashlib.sha1(input_str.encode()).digest()
    return base64.b64encode(sha1_hash).decode()


def send(phone: str, msg: str) -> bool:
    load_dotenv()
    sms_url = os.getenv("SMS_URL")
    sms_secret_key = os.getenv("SMS_SECRET_KEY")
    sms_operator = os.getenv("SMS_OPERATOR")
    if not sms_url or not sms_secret_key or not sms_operator:
        raise ValueError("没有设置短信接口")
    params_map = {}
    try:
        # 授权处理
        # 秘钥，必须
        params_map["secret_key"] = get_sha(sms_secret_key)
        # 对应的第三方系统名称（协议值），必须
        params_map["tp_name"] = "DeepSeekAPI"
        # 对应的模块名称（协议值），必须
        params_map["module_id"] = "sms"
        # 对应的平台系统名称（协议值），必须
        params_map["sys_id"] = "mp"
        # 对应的接口方法名称（协议值），必须
        params_map["interface_method"] = "sms"

        # 参数列表
        # 接收人信息,每个人员信息格式为： 名字|学工号|部门ID|部门名称|电话号码，人与人之间用"^@^"隔开
        params_map["person_info"] = f"||||{phone}"
        # 短信内容，必须
        params_map["sms_info"] = msg
        # 发送优先级（1：紧急通知；2：验证码；3：立即发送；4：发送），必须
        params_map["send_priority"] = "3"
        # 发送时间，String型，可为空，参数不可省略
        params_map["send_time"] = ""
        # 发送人UID，发送模板的时候不可为空，参数不可省略
        params_map["operator_id"] = ""
        # 发送人ID_NUMBER，需要发送回执的时候不可为空，其他可为空，参数不可省略
        params_map["operator_id_number"] = ""
        # 发送人姓名，可为空，参数不可省略
        params_map["operator_name"] = ""
        # 发送人部门ID，不可为空，参数不可省略，有关于短信的配额问题
        params_map["operator_unit_id"] = sms_operator
        # 发送人部门姓名，可为空，参数不可省略
        params_map["operator_unit_name"] = ""
        # 发送模板选择，不发送模板值为"0"，参数不可省略
        params_map["templet_id"] = "0"
        # 发送回执选择，不发送模板值为"0"，参数不可省略
        params_map["receipt_id"] = "0"
        # 发送人签名，根据模板而定，选择的模板有"发送人签名"标签的需要写值，其他为空，参数不可省略
        params_map["person_send"] = ""
        # 发送平台码，必须
        params_map["send_sys_id"] = "1"
        # 发送平台名称，必须
        params_map["send_sys_name"] = "第三方平台"
        # 发送使用的浏览器，可为空，参数不可省略
        params_map["user_browser"] = ""

        json_str = json.dumps(params_map)
        client = Client(sms_url)
        result = client.service.saveSmsInfo(json_str)

        return json.loads(result).get('result')

    except Exception:
        import traceback
        traceback.print_exc()
        return False
