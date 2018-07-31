#!/usr/bin/env python3
import time
#from visonic import alarm
from powerlink2alarm import powerlink2alarm

hostname  = '192.168.0.200'
user = 'admin'
password = 'rosie0500'

test = powerlink2alarm.Powerlink2(hostname, user, password)

res = test.status()
print('Res1: {0}'.format(res))
res = test.status()
print('Res2: {0}'.format(res))
time.sleep(3)
print('And again: {0}'.format(time.time()))
res = test.status()
print('Res3: {0}'.format(res))
print('To: {0}'.format(time.time()))
#user_code = '1234'
#user_id   = '2d978962-daa6-4e18-a5e5-b4a99100bd3b'
#panel_id  = '123456'
#partition = 'P1'
#
#api = alarm.API(hostname, user_code, user_id, panel_id, partition)
#
#res = api.login()
#
#if api.is_logged_in():
#    print('Logged in')
#else:
#    print('Not logged in')
#
#print(api.get_status())
