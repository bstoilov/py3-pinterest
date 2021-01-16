import json
import time
from urllib.parse import urlencode, quote_plus


class RequestBuilder:
    def __init__(self):
        pass

    def buildPost(self, options, source_url='/', context=None):
        return self.url_encode({
            'source_url': source_url,
            'data': json.dumps({
                'options': options,
                "context": context
            }),
            '_': '%s' % int(time.time() * 1000)
        })

    def buildGet(self, url, options, source_url='/', context=None):
        data = self.url_encode({
            'source_url': source_url,
            'data': json.dumps({
                'options': options,
                "context": context
            }),
            '_': '%s' % int(time.time() * 1000)
        })

        url = '{}?{}'.format(url, data)
        return url

    def url_encode(self, query):
        if isinstance(query, str):
            query = quote_plus(query)
        else:
            query = urlencode(query)
        query = query.replace('+', '%20')
        return query
