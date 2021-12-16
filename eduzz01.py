from decouple import config
from eduzz import Eduzz
from pprint import pprint

credentials = dict(email=config('EDUZZ_EMAIL'),
                   publickey=config('EDUZZ_PUBLICKEY'),
                   apikey=config('EDUZZ_APIKEY'))

client = Eduzz(credentials)

g = client.get_sales_list('2021-11-01', '2021-12-15')

pprint(sum(1 for _ in g))


