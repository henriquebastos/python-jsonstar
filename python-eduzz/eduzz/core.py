import requests
from eduzz.serializers import JSONDecoder
from urlobject import URLObject

URL = URLObject('https://api2.eduzz.com/')


class Eduzz:
    def __init__(self, credentials):
        self.credentials = credentials

    def get_sales_list(self, start_date, end_date):
        next_page = 1
        token = None
        token_valid_until = None

        params = {'start_date': start_date, 'end_date': end_date}
        params['page'] = next_page

        response = requests.get(URL.add_path('/sale/get_sale_list'), params=params, auth=self.credentials)
        response.raise_for_status()
        json = response.json(cls=JSONDecoder)

        data = json['data']
        paginator = json['paginator']
        profile = json['profile']
        token = profile['token']
        token_valid_until = profile['token_valid_until']

        yield from data
        #
        # next_page = paginator['page'] + 1
        # params['page'] = next_page
        #
        # response = requests.get(URL.add_path('/sale/get_sale_list'), headers=headers, params=params)
        #
        # json = response.json(cls=JSONDecoder)
        #
        # data = json['data']
        # paginator = json['paginator']
        # profile = json['profile']
        # token = profile['token']
        # token_valid_until = profile['token_valid_until']
        # headers['token'] = token
        #
        # yield from data

