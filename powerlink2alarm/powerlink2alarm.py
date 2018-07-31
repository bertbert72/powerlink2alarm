import requests
import uuid
import json
import xmltodict
from datetime import datetime


class Powerlink2(object):
    def __init__(self, hostname, user, password):
        self.__user = user
        self.__password = password
        self.__hostname = hostname

        self.__base_url = 'http://' + self.__hostname
        self.__cmd_autologout = self.__base_url + '/web/ajax/system.autologout.ajax.php'
        self.__cmd_arming = self.__base_url + '/web/ajax/security.main.status.ajax.php'
        self.__cmd_login = self.__base_url + '/web/ajax/login.login.ajax.php'
        self.__cmd_logout = self.__base_url + '/web/ajax/login.php?act=logout'
        self.__cmd_logs = self.__base_url + '/web/ajax/setup.log.ajax.php'
        self.__cmd_search = self.__base_url + '/web/ajax/home.search.ajax.php'
        self.__cmd_status = self.__base_url + '/web/ajax/alarm.chkstatus.ajax.php'

        self.__plink_token = uuid.uuid4().hex
        self.__plink_token='1234123412341234'
        self.__current_index = 0

        self.__logged_in = False

        self.__keyfobs = None
        self.__sensors = None

        #self.connect()

    def headers(self):
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept-language": "en-GB,en-US;q=0.8,en;q=0.6",
            "Cookie": "PowerLink=" + self.__plink_token,
        }
        return headers

    def connect(self):
        #self.login()
        status = self.status()
        print('Status Dict: {0}'.format(status))
        if status:
            if 'customStatus' not in status or status['customStatus'] != '[NOCNG]':
                print('Some status changes detected')
                print('Index: {0}'.format(status['index']))
            else:
                print('No status changes detected')
        self.logout()

    def Xlogin(self):
        # Check if logged in
        print('Time: {0}'.format(datetime.now()))
        payload = {
            "task": "get_auto_logout_params"
        }

        res = requests.post(self.__cmd_autologout, data=payload, headers=self.headers())
        # Includes workaround for invalid XML response from device
        if res and res.text and '[RELOGIN]' not in res.text:
            print('Response: {0}'.format(res.text))
            response = json.loads(res.text)
            print('Autologout: {0}'.format(response["auto_logout"]))
            self.__logged_in = True
        else:
            print('Login required')
            self.__logged_in = False
        
        print('Result: {0}'.format(res))
        print('Content: {0}'.format(res.content))

        if not self.__logged_in:
            # Login required
            print('Login required')
            payload = {
                "user": self.__user,
                "pass": self.__password,
            }
            res = requests.post(self.__cmd_login, data=payload, headers=self.headers())
            '[RELOGIN]' not in res.textprint('Token: {0}'.format(self.__plink_token))
            if res:
                print('Result: {0}'.format(res))
                print('Content: {0}'.format(res.content))
                if res.content.decode() == 'OK':
                    print('Login was successful')
                    self.__logged_in = True
                else:
                    print('Login not successful')
                #response = json.loads(res.text)
                #print('Response: {0}'.format(response))

    def login(self):
        # Login required
        print('Login required')
        payload = {
            "user": self.__user,
            "pass": self.__password,
        }
        res = self.post_request(self.__cmd_login, payload)
        if res and res.content.decode() == 'OK':
            print('Login was successful')
            self.__logged_in = True
        else:
            print('Login not successful')
            self.__logged_in = False

    def logout(self):
        # Doesn't appear to work
        payload = {
            "user": self.__user,
            "pass": self.__password,
        }
        res = requests.post(self.__cmd_logout, data=payload, headers=self.headers())
        print('Logout result: {0}'.format(res))

    def post_request(self, command, payload, depth = 0):
        res = requests.post(command, data=payload, headers=self.headers())
        if res and res.text and '[RELOGIN]' not in res.text:
            return res
        elif depth < 5:
            print('Retrying post {0}'.format(depth))
            self.login()
            return self.post_request(command, payload, depth + 1)
        else:
            return None

    def status(self):
        # Structure is:
        # reply > {index, cameras, configuration, alerts, alarms, qvFullPath, detectors, faileds}
        #   cameras > {name, picture_name, picture_path}
        #   configuration > {sensors*, system, keyfob*, siren, gsm}
        #     sensors > {name, index, type, location, chime, alarm, status}
        #     system > {name, not_ready, disarm, status, arm, memory, latchkey_enable, ip_mode, ip, subnet, gateway, dns1}
        #     keyfob > {name, index}
        #     siren > {name, index}
        #     gsm > {name, index}
        #   alerts > ?
        #   alarms > {alarm*}
        #     alarm > {module, index, text, picture_text, small_picture, large_picture}
        #   detectors > detector*
        #     detector > {zone, loc, type, status, isalarm}
        #   failedds > {failed*}
        #     failed > {type, status}

        print('Checking status')
        payload = {
            "curindex": self.__current_index, 
            "sesusername": self.__user, 
            "sesusermanager": "1"}
        #res = requests.post(self.__cmd_status, data=payload, headers=self.headers())
        res = self.post_request(self.__cmd_status, payload)
        if res:
            #print('Status: {0}'.format(res.text))
            response = xmltodict.parse(res.text)
            #print('Status Dict: {0}'.format(response))
            #print('Index: {0}'.format(response['reply']['index']))
            status = response['reply']
            if status:
                if 'customStatus' not in status or status['customStatus'] != '[NOCNG]':
                    if 'index' in status:
                        self.__current_index = status['index']
                    if 'camera' in status:
                        self.__cameras = status['cameras']
                    if 'configuration' in status:
                        configuration = status['configuration']
                        for device in configuration:
                            print('Device: {0}'.format(device))
                        if 'sensors' in configuration:
                            for sensor in configuration['sensors']:
                                sensor_info = {
                                    'name': sensor['name'],
                                    'type': sensor['type'],
                                    'location': sensor['location'],
                                    'alarm': None,
                                }
                                self.__sensors[sensor['index']] = sensor_info
                            print('Sensors: {0}', self.__sensors)
                    #        self.__sensors = configuration['sensors']
                    #    if 'system' in configuration:
                    #        self.__system = configuration['system']
                    #    if 'keyfob' in configuration:
                    #        self.__keyfobs = configuration['keyfob']
                    #    if 'siren'
                    #    if 'gsm'

                return status
        return None
 
