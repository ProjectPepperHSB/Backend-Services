import requests

__version__ = "v1.0.0"
__author__ = "Benjamin Thomas Schwertfeger"
__copyright__   = "Benjamin Thomas Schwertfeger"
__email__ = "development@b-schwertfeger.de"
__status__ = "Production"

class Client(object):
    '''
        Stores the API Key and can be used to query data from the mySQL Database by sending 
        requests to the Express-Web-Application of the Pepper Project.

        ------ P A R A M E T E R S ------
        :param API_KEY: str | required
            The key to access the restricted api endpoints

        :param sandbox: bool | optional
            Use localhost webapp or the production Mandatory

        ------ E X A M P L E ------

        > client = Client(API_KEY="n6C?q*QuDA", sandbox=True)
        > client.sql_query("select * from pepper_did_not_understand_table limi 1")
        [{
            'data_id': 1,
            'identifier': '7ce287b890cd497c9c2ae05c1dd2ae20',
            'phrase': 'q76lx76ydl0l93qu2o',
            'ts': '2022-01-11T12:34:50.000Z'
        }]

    '''

    VERSION = "v0.0.1"
    API_VERSION = "v1"

    BASE_URL = "https://informatik.hs-bremerhaven.de/docker-hbv-kms-http"
    SANDBOX_URL = "http://localhost:3000/docker-hbv-kms-http"

    timeout = 10

    def __init__(self, API_KEY: str, sandbox: bool=False, verbose: int=0):
        self.API_KEY = API_KEY
        if not sandbox:
            self.url = self.BASE_URL
        else:
            self.url = self.SANDBOX_URL

        if verbose == 0:
            print(self.test_connection())
        
    
    def test_connection(self):
        payload = {
            "subject": "test"
        }
        return self._request("POST", params=payload, uri="/api/v1")

    def sql_query(self, query: str):
        return self._send_sql_query(query)

    def _send_sql_query(self, query: str):
        payload = {
            "subject": "sql_query",
            "query_str": f"{query};"
        }

        return self._request("POST", params=payload, uri="/api/v1")

    def _request(self, method: str, params: dict={}, uri: str='', headers: dict={}):
        uri_path = uri
        data_json = ''
        if method in ["GET", "DELETE"]:
            if params:
                strl = []
                for key in sorted(params):
                    strl.append("{}={}".format(key, params[key]))
                data_json += '&'.join(strl)
                uri += f"?{data_json}"
        else:
            if params:
                params["auth_key"] = self.API_KEY
                data_json = params 
       
        headers["User-Agent"] = "hbv-kms-pepper-team"
        url = f"{self.url}{uri}"

        if method in ["GET", "DELETE"]:
            response_data = requests.request(method, url, headers=headers, timeout=self.timeout)
        else:
            response_data = requests.request(method, url, headers=headers, data=data_json, timeout=self.timeout)

        return self.check_response_data(response_data)

    @staticmethod
    def check_response_data(response_data):
        if response_data.status_code == 200:
            try:
                data = response_data.json()
            except ValueError:
                raise Exception(response_data.content)
            else:
                return data
        else:
            raise Exception("{}-{}".format(response_data.status_code, response_data.text))
