import uuid
import random
import sqlite3
import secrets
import asyncio
import aiohttp
from datetime import datetime
from toiney import errors
from toiney import constants
from toiney.core.models import device
from toiney.utils.regtoken import SignupUtil
import json
import logging

proxy = 'http://127.0.0.1:8888'

now = datetime.now()  # current time
currentTime = now.strftime('[%I:%M:%S]')

logging.basicConfig(level=logging.DEBUG,
                    format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='[%I:%M:%S]',
                    filename='logs/session.log',
                    filemode='w')

logger = logging.getLogger('session')


class ToineyAPI(object):

    def __init__(self, client=None, loop=None, user=None, pwd=None, cookies=None):
        self._login = True
        self.reg = True
        self._proxies = 'http://127.0.0.1:8888'
        # self._proxies = None
        self._user = user
        self._pwd = pwd
        self.database = sqlite3.connect("credentials.db")
        self._cookies = cookies
        self.loop = loop if loop is not None else asyncio.get_event_loop()
        self._log = True

    def _url(self, path):
        if path[0:2] == constants.API_V2:
            return 'https://secure.hi5.com/api/' + path
        elif path[0:2] == constants.API_V1:
            return 'https://secure.hi5.com/api/' + path
        else:
            return constants.API + path

    async def _request(self, method, url, data={}, headers=None, photo=None):
        if headers is None:
            headers = constants.HEADERS
        if photo is not None:
            boundary = str(uuid.uuid4())
            new_type = 'multipart/form-data; boundary=' + boundary
            constants.HEADERS['Content-Type'] = new_type
            data = aiohttp.FormData()
            data.add_field('upload_photo', open(photo, 'rb'), filename=photo)
        async with aiohttp.ClientSession(cookies=self._cookies) as session:
            async with session.request(method,
                                       self._url(url),
                                       headers=headers,
                                       data=data,
                                       proxy=self._proxies
                                       ) as response:
                try:
                    json_resp = await response.json()
                except Exception:
                    json_resp = json.dumps(await response.text())
                # take session value passed in json_resp and use it as cookie with key: s
                if self._login is True and url == '?method=tagged.login.login&application_id=user':
                    self._s = json_resp['result']['session']  # session cookie
                    self._cookies = response.cookies
                    # self._cookies = {'S': self._s}
                    self._login = False
                if self._log is True:
                    logger.debug(headers)
                    logger.debug(data)
                    logger.debug(json_resp)

                return json_resp

    async def _get(self, url, headers=None):
        return await self._request("get", url, headers=headers)

    async def _post(self, url, data=None, headers=None, photo=None):
        if data is None:
            data = {}
        if photo is None:
            return await self._request("post", url, data=data, headers=headers)
        elif photo is not None:
            return await self._request("post", url, data=data, headers=headers, photo=photo)

    async def location(self):
        # change headers for this request only
        headers = {
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.11.0',
            'Connection': 'Keep-Alive',
            'host': 'secure.hi5.com'
        }
        locations = await self._get('v2/locations/countries?feature=registration', headers)
        return locations['items']  # list of countries + country codes

    async def get_reg_token(self):  # TODO: might need to figure out a better way to implement this
        resp = await self._get("?method=tagged.reg.getRegToken&application_id=user")
        hash_token = SignupUtil().calculateRegHash(str(resp['result']['regToken']).encode())
        return hash_token

    async def reg_token(self):  # TODO: change this function
        # the function getRegToken returns a token that we then hash
        # using the SignupUtil class, but first, turn the token to bytes using .encode()
        hashToken = await self.get_reg_token()
        return await self._post('?method=tagged.mobile.registerDeviceToken&application_id=user', hashToken)

    async def un_reg_token(self):  # unregister device token func
        return await self._post("")  # TODO: change this

    async def appsflyer_id(self):
        # generate appsflyer_id using secrets module and padding
        sec = secrets.SystemRandom().getrandbits(62)
        print(sec)
        randNum = random.randint(0, 8)
        appsflyerId = str(constants.time_ms) + '-' + str(sec).ljust(19, str(randNum))
        # time_ms should equal time since package was installed, will implement database/similar for this
        return str(appsflyerId)

    async def register(self, firstName=None, lastName=None, gender=None, birthYear=None, birthMonth=None, birthDay=None,
                       ethnicity='caucasian', country='US', zipCode=None, email=None, password=None):
        # grab hashed token for regTokenHash field[!]
        hashToken = await self.get_reg_token()  # call getRegToken

        regUrl = "?method=tagged.reg.registerUser&application_id=user"
        if email is None:
            return None
        else:
            regData = {
                'firstName': firstName,
                'lastName': lastName,
                'gender': gender,  # F or M
                'birthYear': birthYear,
                'birthMonth': birthMonth,
                'birthDay': birthDay,
                'ethnicity': ethnicity,
                'country': country,
                'zipCode': zipCode,
                'email': email,
                'password': password,
                'regTokenHash': hashToken,
                'deviceId': device.android_id,
                'aaid': device.ad_id,
                'refId': '',  # leave blank, not required field
                'appsflyer_id': await self.appsflyer_id()
            }
            # return regData

        json_data = await self._post(regUrl, regData)
        return json_data

    async def kit_register(self):
        pass  # TODO: implement this

    async def login(self, data):
        login_json = await self._post("?method=tagged.login.login&application_id=user", data)
        return login_json

    async def photo_upload(self, data, photo=None, caption=None):
        if photo is not None:
            if caption is not None:
                return await self._post(
                    '?method=tagged.photo.upload&&caption=' + caption + '&photo_type=P&application_id=user',
                    data,
                    photo=photo)
            if caption is None:
                return await self._post(
                  "?method=tagged.photo.upload&photo_type=P&application_id=user", data, photo=photo)
        else:
            raise errors.ToineyError('photo_upload failed, data: {0}, photo: {1}'.format(data, photo))

    async def inbox(self, page=None):
        count = 20
        if page is None:
            return await self._get(
                "?method=tagged.im.getInbox&size=s&size2=m&count={0}&filter=all&isPhotoCommentSupported=true&application_id=user".format(
                    count))
        else:
            return await self._get(
                '?method=tagged.im.getInbox&size=s&size2=m&next=' + str(
                    page) + '&count={0}&filter=all&isPhotoCommentSupported=true&application_id=user'.format(
                    count))

    async def send_msg(self, data):
        return await self._post("?method=tagged.im.send&platform=android&application_id=user", data)

    async def send_photo(self, uid, data):
        return await self._post(
            "?method=tagged.im.sendPhotoFromUpload&uid={0}&application_id=user".format(uid), data)

    async def get_alerts(self):
        return await self._get("?method=tagged.user.getAlerts&mcall=true&reset_messages=true&application_id=user")

    async def get_convo(self, uid, count=None):
        if count is None:
            count = '25'
        return await self._get(
            "?method=tagged.im.getConversation&size=s&size2=m&uid={0}&count={1}&isPhotoCommentSupported=true&application_id=user".format(uid, count))

    async def mark_read(self, data):  # mark a msg as read
        return await self._post("?method=tagged.im.markRead&application_id=user", data)

    async def interested(self, uid, counter=None, streak=None):  # interested endpoint request
        if streak is None:
            streak = 0
        if counter is None:
            counter = 1

        interest = random.choices(['true', 'false'], [8.5, 0.7])
        return await self._get('?method=tagged.apps.meetme.interested&user_id=' + str(uid) + '&interest=' +
                               interest[0] + '&counter=' + str(counter) + '&streak=' + str(
            streak) + '&application_id=user')

    async def send_friend_request(self, uid):  # TODO: may be able to add multiple users simultaneously(?)
        return await self._get('?method=tagged.friends.sendRequest&user_ids=' + uid + '&application_id=user')

    async def location_id(self, keyword):
        """
        :param keyword: City name. (case sensitive)
        :return: Shuffles list of city id's and then returns a random choice.
        """
        # change this later to default to preset location id if keyword is None
        param_str = '?method=tagged.locations.location.autoComplete&keyword='+keyword+'' \
                                                                                      '&cc_iso=US&include_region=false'\
                                                                                      '&count=10&application_id=user'
        result = await self._get(param_str)
        cityId_list = []
        for city in result['result']['suggestions']:
            if city['city'] == keyword:
                cityId_list.append(city['locationId'])

        random.shuffle(cityId_list)
        return cityId_list[0]

    async def meetmeBrowse(self, location=None, offset=None):  # TODO: work on this
        if location is None:
            locations = ['Atlanta', 'Greensboro', 'Charlotte', 'Raleigh', 'Los Angeles', 'Santa Cruz', 'San Diego']
            random.shuffle(locations)
            location = await self.location_id(locations[0])

        min_age = '18'
        max_age = '65'
        url = '?method=tagged.search.query&returns_users=true&show=25&language=-1&location=&location_nd=&min_age='+min_age+'&num_results=24&country=US&jsonFilters={"ethnicity":{},"rel_status":{}}&location=&offset='+offset+'&rel_status=0&ethnicity=0&gender=M&newlocation_id='+location+'&distance=100&max_age='+max_age+'&application_id=user'
        return await self._get(url)

    async def batch(self):  # this runs every 900 seconds to update the app(?)
        return await self._get("?method=tagged.log.batch")


if __name__ == '__main__':
    toiney = ToineyAPI()

    loop = asyncio.get_event_loop()

    first = "jackson"
    last = "griffin"
    gender = "M"
    birthyear = "1998"
    birthmonth = "5"
    birthday = "5"
    ethnicity = "caucasian"
    country = "US"
    zipCode = "28070"
    email = "jackygriffin@hotmail.com"
    password = "boobies69"
    results = loop.run_until_complete(toiney.register(first,
                                                      last,
                                                      gender,
                                                      birthyear,
                                                      birthmonth,
                                                      birthday,
                                                      ethnicity,
                                                      country,
                                                      zipCode,
                                                      email,
                                                      password))
    print(results)

    # example usage of calculateRegHash func
    # hashToken = SignupUtil().calculateRegHash(toiney.getRegToken().encode())
    # print(hashToken) to see value returned
    # example usage of location func:
    # for country in toiney.location():
    #    print(country['countryCode']) to grab all country codes