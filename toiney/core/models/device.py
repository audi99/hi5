from decimal import Decimal

import uuid

import random
import string
import secrets

from toiney.utils.pyimei import ImeiSupport


def randhex(size=8):
    thisHex = secrets.token_hex(size)
    return thisHex


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# region Globals pt. 1
app_version = '9.5.0'  # subject to change
java_vm_version = "2.1.0"
ro_product_provider = "LGE"
ro_product_brand = "google"
ro_product_name = "bullhead"
ro_product_model = "Nexus 5X"
ro_product_board = "bullhead"
ro_product_instructions = "armeabi-v7a:armeabi"
ro_build_id = "OPM4.171019.016.A1"
ro_build_version_incremental = "4720815"
ro_build_version_release = "8.1.0"
ro_build_version_sdk = "27"
locale = "en_US"
offset = "-240"
device_id = str(uuid.uuid4())
imei = ImeiSupport.generateNew()
serial = str(randhex())
density = Decimal(2.625)
dimensions = "1080, 1920"  # TODO: Change this(?)
ad_id = str(uuid.uuid4())  # Visual Basic: Guid.NewGuid.ToString, Python: str(uuid.uuid4())
android_id = "Thi5" + str(randhex())  # has to have Thi5 prefixed
android_uuid = str(uuid.uuid4())
operator = "Verizon"
mcc = '311'  # Mobile country code
mnc = '480'  # Mobile network code
total_memory = 201326592
used_memory = random.randrange(100000000, total_memory)
#endregion


class Device:
    # region Globals pt. 2
    global app_version
    global java_vm_version

    global ro_product_provider
    global ro_product_brand
    global ro_product_name
    global ro_product_model
    global ro_product_board
    global ro_product_instructions

    global ro_build_id
    global ro_build_version_incremental
    global ro_build_version_release
    global ro_build_version_sdk

    global locale
    global offset

    global device_id

    global density
    global dimensions

    global imei
    global serial

    global ad_id
    global android_id
    global android_uuid

    global operator
    global mcc
    global mnc

    global total_memory
    global used_memory
    #endregion.

    def __init__(self):

        # region Members
        self.app_version = app_version
        self.java_vm_version = java_vm_version
        self.ro_product_provider = ro_product_provider
        self.ro_product_brand = ro_product_brand
        self.ro_product_name = ro_product_name
        self.ro_product_model = ro_product_model
        self.ro_product_board = ro_product_board
        self.ro_product_instructions = ro_product_instructions

        self.ro_build_id = ro_build_id
        self.ro_build_version_incremental = ro_build_version_incremental
        self.ro_build_version_release = ro_build_version_release
        self.ro_build_version_sdk = ro_build_version_sdk

        self.locale = locale
        self.offset = offset

        self.device_id = device_id

        self.density = density
        self.dimensions = dimensions

        self.imei = imei
        self.serial = serial

        self.ad_id = ad_id
        self.android_id = android_id
        self.android_uuid = android_uuid

        self.operator = operator
        self.mcc = mcc
        self.mnc = mnc

        self.total_memory = total_memory
        self.used_memory = used_memory
        #endregion

    def device_json(self):
        json_dict = {
            'java_vm_version': self.java_vm_version,
            'ro_product_provider': self.ro_product_provider,
            'ro_product_brand': self.ro_product_brand,
            'ro_product_name': self.ro_product_name,
            'ro_product_model': self.ro_product_model,
            'ro_product_board': self.ro_product_board,
            'ro_product_instructions': self.ro_product_instructions,
            'ro_build_id': self.ro_build_id,
            'ro_build_version_incremental': self.ro_build_version_incremental,
            'ro_build_version_release': self.ro_build_version_release,
            'ro_build_version_sdk': self.ro_build_version_sdk,
            'locale': self.locale,
            'offset': self.offset,
            'device_id': self.device_id,
            'imei': self.imei,
            'serial': self.serial,
            'density': self.density,
            'dimensions': self.dimensions,
            'ad_id': self.ad_id,  # Visual Basic: Guid.NewGuid.ToString, Python: str(uuid.uuid4())
            'android_id': self.android_id,
            'android_uuid': self.android_uuid,
            'operator': self.operator,
            'mcc': self.mcc,  # Mobile country code
            'mnc': self.mnc,  # Mobile network code
            'total_memory': self.total_memory,
            'used_memory': self.used_memory

        }

        return json_dict

    def useragent(self):
        # hi5 uses custom user agent
        return "hi5/{0} ({1}; Android {2}; {3} Build/{4}:{5}/MMB29M/G900PVPS3CQD1:user/release-keys)".format(app_version, ro_product_model, ro_build_version_release, ro_product_model, ro_build_id, ro_build_version_release)

        # if otherwise, we'd use:
        # return "Dalvik/{0} (Linux; U; Android {1}; {2} Build/{3})".format(java_vm_version, ro_build_version_release, ro_product_model, ro_build_id)

    def useragent_browser(self):
        return "Mozilla/5.0 (Linux; Android {0}; {1} Build/{2}) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.98 Mobile Safari/537.36".format(ro_build_version_release, ro_product_model, ro_build_id)

    def ro_build_fingerprint(self):
        return str.join('/', (ro_product_brand, ro_product_name, str.join(":", (ro_product_name, ro_build_version_release)), ro_build_id, str.join(":", (ro_build_version_incremental, "user")), "release-keys"))


if __name__ == '__main__':
    device = Device()
    print(id_generator())
