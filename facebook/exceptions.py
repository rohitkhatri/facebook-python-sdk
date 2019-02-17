class FacebookException(Exception):
    status_code = None
    api_code = None
    message = None
    error_type = None
    response = None

    def __init__(self, code, response):
        self.status_code = code
        self.response = response

        if 'error' in response:
            self.error_type = response['error']['type']
            self.message = response['error']['message']
            self.api_code = response['error']['code']
