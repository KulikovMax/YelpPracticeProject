import time
import json
import requests
from parsel import Selector

urls = [
    'https://www.yelp.com/biz/the-pig-washington-2',
    'https://www.yelp.com/biz/gypsy-kitchen-washington',
    'https://www.yelp.com/biz/pupatella-washington',
    'https://www.yelp.com/biz/cvi-che-105-miami'
]

# proxy = '158.46.169.252:443'
# proxies = {
#     'http': 'http://'+proxy,
#     'https': 'https://'+proxy
# }


def create_address_dict(sel):
    address_country = 'US'
    address_text = sel.xpath('//address/p/span/text()').get()
    address_zip = address_text[-5:]
    address_text = address_text[:-6]
    address_state = ''
    if address_country == 'US':
        address_state = address_text[-2:]
    address_city = address_text
    return {
        "country": address_country,
        "state": address_state,
        "zip": address_zip,
        "city": address_city
    }


def create_contact_dict(sel):
    contacts_phone = sel.xpath('//section/div/div[2]/div/div/p[2]/text()').get()
    contact_domain = sel.xpath('//section/div/div/div/div/p[2]/a/text()').get()
    contact_url = f'http://{contact_domain}'
    return {
        'phone': contacts_phone,
        'website': {
            'domain': contact_domain,
            'url': contact_url
        }
    }


def create_data_json(link):
    response = requests.get(link)
    response_text = response.text
    selector = Selector(text=response_text)

    title = selector.xpath(".//h1/text()").get()
    categories = selector.xpath(
            '//yelp-react-root/div/div[2]/div/div/div/div/span[3]/span/a/text()'
        ).getall()

    data_dict = dict()
    data_dict["url"] = link
    data_dict["title"] = title
    data_dict["categories"] = categories

    data_dict['address'] = create_address_dict(selector)
    data_dict['contact'] = create_contact_dict(selector)

    with open(f'{title}.json', 'w') as w_file:
        json.dump(data_dict, w_file, indent=2)

    return data_dict


# for url in urls:
#     create_data_json(url)
#     time.sleep(20)
