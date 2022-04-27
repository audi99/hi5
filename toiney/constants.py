import time
import logging

from toiney.core.models import device
from toiney.errors import ToineyError

logger = logging.getLogger(__name__)

# current_milli_time = lambda: int(round(time.time() * 1000))
current_milli_time = lambda: int(time.time())
time_ms = current_milli_time()

API = 'https://secure.hi5.com/api/'
API_V1 = 'v1'
API_V2 = 'v2'

SHA256_SCHEMA = 'IASjHLT83A/wJOvIFOE1rEAXkSRz5zULlEduFxgpsgwH'

HEADERS = {
    'Accept-Encoding': 'gzip',
    'User-Agent': device.Device().useragent(),
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Connection': 'Keep-Alive',
    'Host': 'secure.hi5.com'
}

KEY_ACTION = "action"
KEY_CLIENT_ID = "client_id"
KEY_CLIENT_VERSION = "client_version"
KEY_FIELD_PREFILLED = "field_prefilled"
KEY_REG_SESSION_ID = "reg_session_id"
KEY_REG_VERSION = "reg_version"
KEY_USER_AGENT = "user_agent"
SHA = "IASjHLT83A/wJOvIFOE1rEAXkSRz5zULlEduFxgpsgwH"
TOPIC = "registration_flow"
# TODO: turn the above variables into a proper registration builder


def batch(topic, reg_type):  # TODO: might change how this works for registration: email_form_submit(?)
    if reg_type == 'email':
        reg_type = 'signup_others_email_click'
    elif reg_type == 'phone':
        reg_type = 'signup_phone_number_click'
    try:
        data = {
            "source__agent": device.Device().useragent(),
            "registration_flow__action": reg_type,
            "source__timestamp": time_ms,
            "user_agent": device.Device().useragent(),
            "registration_flow__client_version": device.app_version,
            "registration_flow__reg_version": "1",
            "registration_flow__client_id": device.android_id,
            "registration_flow__platform": "Android",
            "metadata": 'true',
            "schema_sha256": SHA256_SCHEMA,
            "topic": topic
        }

        return data

    except ToineyError as e:
        logger.debug(e)

