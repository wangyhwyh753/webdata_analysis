import urllib.request
import urllib.parse
import json
import time

DEFAULT_SERVICE_URL = 'https://service.aibee.cn/santa/single'
DEFAULT_AUTH = 'Basic c2FudGE6OWVEejNBck1CSEpGNDZyYQ=='


def alert(title, content, phone=None, email=None):
    try:
        headers = {'Authorization': DEFAULT_AUTH}
        url = DEFAULT_SERVICE_URL

        if email is None:
            send_user_list = [
                {'target': 'sms', 'value': phone}
            ]
        elif phone is None:
            send_user_list = [
                {'target': 'mail', 'value': email}
            ]
        else:
            send_user_list = [
                {'target': 'sms', 'value': phone},
                {'target': 'mail', 'value': email}
            ]

        package = {
            "title": title,
            "content": content,
            "users": send_user_list
        }
        request = urllib.request.Request(url=url, data=json.dumps(package).encode('utf-8'), headers=headers)
        response = urllib.request.urlopen(request).read().decode('utf-8')
        print('santa response {}'.format(response))

    except Exception as e:
        print('alarm error: %s' % str(e))


def send_alarm(content_str, subject_str, users_phone_email_list):
    if not users_phone_email_list:
        pass
    else:
        for users_phone_email in users_phone_email_list:
            [user_iphone, user_email] = users_phone_email.split(":")
            alert(subject_str, content_str, user_iphone, user_email)
            time.sleep(3)
