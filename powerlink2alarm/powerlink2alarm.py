import requests

class Powerlink2(object):
    def __init__(self, hostname, user, password):
        self.__user = user
        self.__password = password
        self.__hostname = hostname

        self.__base_url = 'http://' + self.__hostname
        self.__cmd_login = self.__base_url + '/web/ajax/login.login.ajax.php'
        self.__cmd_autologout = self.__base_url + '/web/ajax/system.autologout.ajax.php'

        self.__plink_token = None

        self.connect()

    def connect(self):
        self.login()
        print('Login ok')


    def login(self):
        payload = {
            "task": "get_auto_logout_params"
        }

        res = requests.post(self.__cmd_autologout, data=payload, headers=self.headers())
        if res:
            print('Result: {0}'.format(res))

    def headers(self):
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept-language": "en-GB,en-US;q=0.8,en;q=0.6",
            "Cookie": "PowerLink=" + self.__plink_token
        }
        return headers
