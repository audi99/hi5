from toiney import api
from toiney import errors
from toiney.logs.func_wrappers_etc import log_dbg, wait_alt, log_func
from toiney.core.models.device import Device
from toiney.core.utils.uint_random import Random

from threading import Timer
import random
import json
import sqlite3
import spintax
import asyncio


def output_json(data):
    json_data = json.dumps(data)
    return json.loads(json_data)


class Session(object):
    # @log_dbg
    def __init__(self, functions=None, user=None):
        self.functions = functions
        self.user = user
        self._cookies = None
        self._api = api.ToineyAPI(cookies=self._cookies)
        self.logger = log_func
        self._email = None
        self._device = Device
        self.Random = Random()

        self.timer = Timer  # TODO: not sure if this will do what i need

        self.database = sqlite3.connect("credentials.db")

    @log_dbg
    async def login(self, i):  # TODO: redo this to make it where you call this function with an email
        sql_q = "SELECT email FROM user WHERE email LIKE '%@yahoo.com%' OR email LIKE '%@hotmail.com%' OR email LIKE" \
                "'%@gmail.com%' OR email LIKE '%@outlook.com%'"
        cur = self.database.cursor()

        emails = cur.execute(sql_q).fetchall()
        if emails[i][0] is None:
            raise errors.ToineyError('No user was found with email: ' + emails[i][0] + ' in database!')

        row = cur.execute("SELECT * FROM user where email LIKE '%{0}%'".format(emails[i][0])).fetchone()

        self.logger().debug("Logging into account '{0}'!".format(emails[i][0]))
        call_func = await self._api.login(data={'email': emails[i][0],
                                                'password': row[1],
                                                'deviceId': row[2],
                                                'aaid': row[3]})

        if call_func['stat'] != 'fail':
            self.logger().debug("Successfully logged into account '{0}'!".format(emails[i][0]))
            print(call_func)
            self._email = emails[i][0]

    @log_dbg
    async def register(self, delay=None):
        """
        :param delay: add random delay here based on GUI option
        :return: registration results
        """
        cur = self.database.cursor()
        cur.execute("SELECT first_name, last_name, password, birthday, gender from registration")
        results = cur.fetchall()
        for users in results:
            asyncio.sleep(delay)  # TODO: add delay here
            birthday = users[3].split('-')
            birth_rand = self.Random.birth_date(int(birthday[0]), int(birthday[1]))
            data = {'firstName': users[0],
                    'lastName': users[1],
                    'gender': users[4],
                    'birthYear': str(birth_rand[0]),
                    'birthMonth': str(birth_rand[1]),
                    'birthDay': str(birth_rand[2]),
                    'ethnicity': 'caucasian',
                    'country': 'US',
                    'zipCode': '',  # TODO: add zipcode(s)
                    'email': '',  # TODO: add email(s)
                    'password': users[2]
                    }
            print(data)
            # await aiohttp request to register endpoint here
            # then parse json result

    @log_dbg
    async def location(self):
        return await self._api.location()

    @log_dbg
    async def upload_photo(self, files):
        return await self._api.photo_upload(files)

    @log_dbg
    async def icebreaker(self, var=None):
        users = await self.inbox(unread=True)
        n = 0
        for user in users:
            uid = str(user['uid'])
            cur = self.database.cursor()
            try:
                cur.execute("SELECT user_id from conversations where user_id={0}".format(uid))
                if cur.fetchone() is not None:
                    self.logger().debug("Already msged user {0}, skipping...".format(uid))
                    continue
            except Exception:
                pass
            # before we execute, let's do a 1 in 20 chance of rand_num being our chosen integer, if it is,
            # then sleep between 1-3 minutes,
            # we also will reset the integer n, once n hits 50 users messaged, then sleep between 2-3 minutes.
            rand_num = random.randint(0, 20)
            if rand_num == 6:
                self.logger().debug("'rand_num' variable hit, sleeping for {0}s!".format(str(random.randint(60, 180))))
            if n > 0:
                self.logger().debug("Sleeping before sending next message...")
            elif n == 0:
                self.logger().debug("Sleeping before sending message...")
            elif n == 50:
                n = 0
                self.logger().debug(
                    "50 users messaged this loop, resetting integer n and then sleeping for {0}s!".format(
                        str(await wait_alt(30, 90))))
            n += 1
            await wait_alt(30, 90)  # sleep
            await self.mark_read(user)
            await wait_alt(3, 10)  # random wait after marking the msg as read to make us look more real
            if var is None:
                msgs = ['hey!! how are you?', 'hi, how are you?? :)', 'hey, what\'s up?']
                random.shuffle(msgs)
                msg = msgs[0].strip('\n')
            else:
                msg = spintax.spin(var)  # make spintax variable and call function with it(var)
            # uid = msgUser
            body = {
                'uid': str(uid),
                'message': str(msg),
                'type': '1',
                'priority': '0'
            }
            self.logger().debug("HTML body being sent in request: {0}".format(body))

            attempt_msg = "Attempting to send response message to user '[{0}]' from account '{1}'!"
            self.logger().debug(attempt_msg.format(str(uid), self._email))
            post_msg = await self._api.send_msg(body)
            if post_msg['stat'] == 'ok':
                success_msg = "Successfully sent response message to user '[{0}]' from account '{1}'"
                self.logger().debug(success_msg.format(str(uid), self._email))
                cur.execute("INSERT into conversations(user_id) VALUES ({0})".format(uid))
                self.database.commit()

    @log_dbg
    async def inbox(self, unread=True, count=None):  # TODO: may need to redo this
        user_list = []
        user_dict = {}
        page = None
        x = 0
        while True:
            await wait_alt(2, 5)
            if unread is True:  # if function is called with True, then scrape only unread messages(!)
                inbox = await self._api.inbox(page=page)
                data = output_json(inbox)  # we can check if next=None, otherwise it will return null
                for item in data['result']['items']:
                    if item['unread'] > 0:
                        if item['gender'] == 'M':
                            if item['uid'] is not None:
                                x += 1
                                user_dict['uid'] = item['uid']
                                user_dict['unread_count'] = item['unread']
                                user_list.append(user_dict)
                                user_dict = {}
                        else:  # if gender is not male, then pass(avoid all female accounts)
                            pass
                next_page = output_json(data['result']['next'])
                self.logger().debug(next_page)
                items = data['result']['items']
                if 2 > len(items):
                    if x < 21:  # if only one page total of users in account inbox
                        next_page = 1
                    elif x >= 21:
                        next_page = page
                    success_msg = "Successfully retrieved '{0}' incoming messages from individual users " \
                                  "on account '{2}'!"  # TODO: format email into this variable
                    self.logger().debug(success_msg.format(x, next_page, self._email))
                    # avoiding duplicates(!) #
                    seen = set()
                    new_l = []
                    for d in user_list:
                        t = tuple(sorted(d.items()))
                        if t not in seen:
                            seen.add(t)
                            new_l.append(d)
                    return new_l
                else:  # else if json key 'next' is not None(null) value
                    page = next_page
                    pass
            elif unread is False:  # scrape all messages in our inbox
                inbox = await self._api.inbox(page=page)
                data = output_json(inbox)  # we can check if next=None, otherwise it will return null
                for item in data['result']['items']:
                    if item['uid'] is not None:
                        x += 1
                        user_list.append(item['uid'])
                next_page = data['result']['next']
                if next_page is None:
                    if x < 21:  # if only one page total of users messaged account
                        next_page = 1
                    elif x >= 21:
                        next_page = page
                    success_msg = "Successfully retrieved '{0}' incoming messages from individual users open conversations " \
                                  "on account '{2}'!"
                    self.logger().debug(success_msg.format(x, next_page))
                    # avoiding duplicates(!) #
                    seen = set()
                    new_l = []
                    for d in user_list:
                        print(user_list)
                        t = tuple(sorted(d.items()))
                        if t not in seen:
                            seen.add(t)
                            new_l.append(d)

                    return new_l
                else:  # else if json key 'next' is not None(null) value
                    self.logger().debug("Retrieving more users...")
                    page = next_page
                    pass

    @log_dbg
    async def mark_read(self, data):  # ideally execute this function after a msg is sent(?)
        if data is not None:
            return await self._api.mark_read(data)
        else:
            pass

    async def get_alerts(self):
        return await self._api.get_alerts()

    @log_dbg
    async def interested(self):
        uids = await self.inbox(unread=True)
        counter = 1
        streak = 0
        for uid in uids:
            try:
                await wait_alt(5, 10)
                uid = str(uid['uid'])
                interest = await self._api.interested(uid, counter=counter, streak=streak)
                counter = interest['result']['counter']
                streak = interest['result']['streak']
            except KeyError as e:
                raise errors.ToineyError(
                    'The maximum number of YES votes per day has been reached. Play again tomorrow!')

    @log_dbg
    async def send_friend_request(self, uid=None):
        if uid is None:
            return None
        return await self._api.send_friend_request(str(uid))

    @log_dbg
    async def batch(self):
        pass  # TODO: change this self._api.batch()

    @log_dbg
    async def run_batch(self):
        self.timer(900000, self.batch).start()

    async def search_query(self, count=None):
        if count is None:
            count = 1
        offset = 24  # the number it starts at, if in loop, we want this to increase by 24 each cycle.
        # keep offset var outside of loop
        temp_list = []
        for i in range(0, count):
            users = await self._api.meetmeBrowse(offset=str(offset))
            offset += 24
            for user in users['results']:
                temp_list.append(user['userId'])

        random.shuffle(temp_list)
        return temp_list

    @log_dbg
    async def fetch(self, login_int):  # TODO: testing, maybe delete later(?)
        await self.login(login_int)
        await wait_alt(3, 9)
        # await self.interested()
        # await self.icebreaker()
        while True:
            uids = await self.search_query()
            for uid in uids:
                await wait_alt(5, 11)
                await self.icebreaker()
                await wait_alt(10, 20)
                await self.send_friend_request(uid=uid)

    async def run_func(self, func_key, *args, **kwargs):
            func_name = self.functions.get(func_key)
            if func_name and hasattr(self, func_name):
                return await getattr(self, func_name)(*args, **kwargs)
            else:
                return await None


def main(login=False, list_of_tasks=None, loop=None):
    loop = loop if loop else asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    fun_dict = {}
    a = Session(fun_dict)
    # fun_dict = {0: '_request'}
    if login is True:
        login_tasks = ['login']  # one account to be logged in for now
        login_ = []
        fun_dict[0] = login_tasks[0]
        login_.append(a.run_func(0, 0))
        print(login_)
        loop.run_until_complete(asyncio.gather(*login_))
        fun_dict = {}
    else:
        pass
    task_list = list_of_tasks

    keys = range(len(task_list))
    for i in keys:
        fun_dict[i] = task_list[i]
        task_list.append(a.run_func(i, i))  # i, i = integer(function), args

    interest_run = loop.run_until_complete(asyncio.gather(*task_list))
    results_list = []
    for results in interest_run:
        results_list.append(results)

    print(results_list)
    return results_list


if __name__ == '__main__':  # for testing purposes mostly
    loop = asyncio.new_event_loop()
    sess = Session()
    foo = loop.run_until_complete(sess.fetch(2))
