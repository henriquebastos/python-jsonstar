import requests
from urlobject import URLObject
from eduzz.serializers import JSONDecoder

URL = URLObject('https://api2.eduzz.com/')

from requests import Session



class Credentials:
    def __init__(self, email, pubkey, apikey):
        self.email = email
        self.pubkey = pubkey
        self.apikey = apikey
        self._token = None
        self._valid_until = None

    def token(self):
        if self._token and self._valid_until > datetime.now():
            return self._token

        self._token, self._valid_until = self.renew(self.email, self.pubkey, self.apikey)

    @staticmethod
    def renew(email, pubkey, apikey):
        resource = URL.add_path('/credential/generate_token')
        payload = dict(email=email, publickey=pubkey, apikey=apikey)
        r = requests.post(url=resource, params=payload)
        return r['data']['token'], r['data']['valid_until']


class Eduzz:
    def __init__(self, credentials):
        self.credentials = credentials

    def get_sales_list(self, start_date, end_date):
        def renew_token(credentials):
            resource = URL.add_path('/credential/generate_token')
            payload = self.credentials
            response = requests.post(url=resource, params=payload)
            return response.json(cls=JSONDecoder)

        next_page = 1
        token = None
        token_valid_until = None

        headers = {}

        if 'token' not in headers:
            json = renew_token(self.credentials)
            token = json['data']['token']
            token_valid_until =json['data']['token_valid_until']
            headers['token'] = token

        params = {'start_date': start_date, 'end_date': end_date}
        params['page'] = next_page

        response = requests.get(URL.add_path('/sale/get_sale_list'), headers=headers, params=params)

        if response.status_code == 401:
            json = renew_token(self.credentials)
            token = json['data']['token']
            token_valid_until = json['data']['valid_until']
            headers['token'] = token

            response = requests.get(URL.add_path('/sale/get_sale_list'), headers=headers, params=params)

        json = response.json(cls=JSONDecoder)

        data = json['data']
        paginator = json['paginator']
        profile = json['profile']
        token = profile['token']
        token_valid_until = profile['token_valid_until']
        headers['token'] = token

        yield from data

        next_page = paginator['page'] + 1
        params['page'] = next_page

        response = requests.get(URL.add_path('/sale/get_sale_list'), headers=headers, params=params)

        if response.status_code == 401:
            json = renew_token(self.credentials)
            token = json['data']['token']
            token_valid_until = json['data']['valid_until']
            headers['token'] = token

            response = requests.get(URL.add_path('/sale/get_sale_list'), headers=headers, params=params)

        json = response.json(cls=JSONDecoder)

        data = json['data']
        paginator = json['paginator']
        profile = json['profile']
        token = profile['token']
        token_valid_until = profile['token_valid_until']
        headers['token'] = token
        
        yield from data






def get_token(email, publickey, apikey):
    resource = URL.add_path('/credential/generate_token')
    payload = dict(email=email, publickey=publickey, apikey=apikey)

    r = requests.post(url=resource, params=payload)
    data = r.json(cls=JSONDecoder)
    return data





# class Endpoints:
#     url = URLObject('https://api2.eduzz.com/')
#
#     @classmethod
#     def token(cls):
#         return cls.url.add_path('credential/generate_token')
#
#     @classmethod
#     def sale__get_sale_list(cls, params):
#         qparams = ('start_date', 'end_date', 'page')
#         url = cls.url.add_path('sale/get_sale_list')
#         return url.add_query_params(**params)
#
# #
# def eduzz_token(email, pubkey, apikey):
#
#     URL = 'https://api2.eduzz.com/credential/generate_token'
#     auth = {'email': email, 'pubkey': pubkey, 'apikey': apikey}
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
#     }
#     r = requests.post(URL, data=auth, headers=headers)
#     j = r.json()
#     return {'token': j['data']['token']}
#
#
# def eduzz_get_sale_list(start_date, end_date, token):
#     page = 1
#     while True:
#         URL = f'https://api2.eduzz.com/sale/get_sale_list?start_date={start_date}&end_date={end_date}&page={page}'
#         r = requests.get(URL, headers=token)
#         assert r.status_code == 200
#
#         j = r.json()
#         assert j['success']
#         data = j['data']
#         token = {'token': j['profile']['token']}
#         paginator = j['paginator']
#
#         yield from data
#
#         page += 1
#
#         if paginator['page'] >= paginator['totalPages']:
#             break
#
#
# def eduzz_sales(start_date, end_date):
#     token = eduzz_token(config('EDUZZ_EMAIL'), config('EDUZZ_PUBLICKEY'), config('EDUZZ_APIKEY'))
#     return eduzz_get_sale_list(start_date, end_date, token)
#
#
#
# # def eduzz_get_sale_report():
# #     start_date = '2019-01-01'
# #     end_date = datetime.now().date()
# #     eduzz_api_sales_payload = eduzz_sales(start_date, end_date)
# #     # print(sales)
# #
# #     # Captura cabecalho da planilha e insere na lista
# #     for sale in eduzz_api_sales_payload:
# #         header_list = []
# #         for item in sale:
# #             header_list.append(item)
# #
# #         pprint(header_list)
# #         break
#
#
# def tests():
#     pass
#     # eduzz_get_sale_report()
#
# if __name__ == '__main__':
#     tests()