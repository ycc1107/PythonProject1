import argparse
import json
import pprint
import sys
import urllib
import urllib2

import oauth2


API_HOST = 'api.yelp.com'
DEFAULT_TERM = 'Japanese'
DEFAULT_LOCATION = 'New York, NY'
SEARCH_LIMIT = 1000
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'

# OAuth credential placeholders that must be filled in by users.
CONSUMER_KEY = 'ASmqU0iU9N58dnQAakja7w'
CONSUMER_SECRET = 'iCLcU-Ce2mlHsbc4vHC4esOb9C8'
TOKEN = 'VkVLi0mvpaLw4E7MM-7Kq-SrGWqfQyM7'
TOKEN_SECRET = 'nKuYi3tmmx7vz5dWGoS_vMC7P1k'

def request(host, path, url_params=None):
    url_params = url_params or {}
    url = 'http://{0}{1}?'.format(host, path)

    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request(method="GET", url=url, parameters=url_params)

    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
        }
    )
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()

    print 'Querying {0} ...'.format(url)

    conn = urllib2.urlopen(signed_url, None)
    try:
        response = json.loads(conn.read())
    finally:
        conn.close()

    return response

def search(term, location):

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, url_params=url_params)

def get_business(business_id):

    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path)

def query_api(term, location):

    response = search(term, location)

    businesses = response.get('businesses')

    if not businesses:
        print 'No businesses for {0} in {1} found.'.format(term, location)
        return

    business_id = businesses[0]['id']

    print '{0} businesses found, querying business info for the top result "{1}" ...'.format(
        len(businesses),
        business_id
    )

    response = get_business(business_id)
    getFourStarRating(response)

def getFourStarRating(response):
    result = []
    x = response

    for res in response:
        if res["rating"] >= 4:
            temp = " ".join(res["name"],res["rating"],res["review_count"],res["url"])
            result.append(temp)
    with open("text.txt","wb") as f:
        f.write(result)



def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM, type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location', default=DEFAULT_LOCATION, type=str, help='Search location (default: %(default)s)')

    input_values = parser.parse_args()

    try:
        query_api(input_values.term, input_values.location)
    except urllib2.HTTPError as error:
        sys.exit('Encountered HTTP error {0}. Abort program.'.format(error.code))



if __name__ == '__main__':
    main()
