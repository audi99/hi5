from decimal import Decimal
import os
import json


class Configuration(object):
    def __init__(self):  # TODO: this
        self.loads = 0
        self.viewEventLog = True
        self.viewStatusBar = True
        self.autoScrollEvents = True
        self.shuffle_data = True
        self.save_coordinates_on_close = True
        self.timeout = Decimal(60)  # seconds
        self.retries = 3
        self.dumpErrorLogs = True
        self.mask_connections = True
        self.refresh_proxies_interval = 300  # 5 minutes
        self.proxy_single = True
        self.login_min = 1
        self.login_max = 3
        self.delete_invalid = True
        self.upload_min = 3
        self.upload_max = 5
        self.location_min = 3
        self.location_max = 5
        self.allow_register = True
        self.register_none_available = True
        self.registration_quota = 10  # amount of accounts to register per session
        self.refresh_proxies = True
        self.register_min = 1
        self.register_max = 3
        self.registration_photo = True
        self.allow_confirmation = True
        self.check_inbox_rest_min = 300  # seconds
        self.check_inbox_rest_max = 600
        self.check_inbox_delay_min = 3  # seconds
        self.check_inbox_delay_max = 6
        self.check_inbox_quota_min = 5
        self.check_inbox_quota_max = 10
        self.photosets_path = None  # TODO: this
        self.photoset_single = True
        self.workers = 10
        self.operation_min = 10000
        self.operation_max = 15000
        self.rest_min = 60
        self.rest_max = 120
        self.allow_set_profile = True
        self.profile_min = 5000
        self.profile_max = 7500
        self.existing_profile_details = True
        self.skip_details_quota = 1440
        self.skip_photo_quota = 1440
        self.profile_photo_quota = 1
        self.profile_location = True
        self.skip_location_quota = 60
        self.only_complete_profiles = True
        self.allow_scrape = True
        self.search_min = 3000
        self.search_max = 3000
        self.scrape_page_quota = 0  # 0 for infinite
        self.scrape_quota = 1
        self.scraping_rest_min = 5
        self.scraping_rest_max = 10
        self.allow_send_friend_requests = True
        self.outgoing_friend_request_min = 3000
        self.outgoing_friend_request_max = 5000
        self.outgoing_friend_request_quota_min = 50
        self.outgoing_friend_request_quota_max = 75
        self.outgoing_friend_request_rest_min = 30
        self.outgoing_friend_request_rest_max = 60
        self.allow_icebreaker = True
        self.icebreaker_min = 5000
        self.icebreaker_max = 10000
        self.accept_rest_min = 30
        self.accept_rest_max = 60
        self.allow_responding = True
        self.respond_scrape_min = 30000
        self.respond_scrape_max = 60000
        self.respond_abort = 5
        self.respond_min = 3000
        self.respond_max = 5000
        self.respond_quota_min = 50
        self.respond_quota_max = 100
        self.respond_rest_min = 30
        self.respond_rest_max = 60
        self.respond_male = True
        self.respond_female = True
        self.respond_flow = str({})
        self.respond_scrape_page_min = 2000
        self.respond_scrape_page_max = 2000
        self.refreshVariables = True
        self.variableRefreshInterval = 10

    def load(self):
        path = os.path.join('Main.folderData', "settings.dat")  # TODO: change this
        with open(path, 'r') as reader:
            file_contents = reader.readlines()
        return json.loads(self)(file_contents)




