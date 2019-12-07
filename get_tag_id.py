import os
import binascii
import nfc
import time
import json
import requests

URL = os.environ.get('SLACK_WEBHOOK_URL', None)
if not URL:
    print('No SLACK_WEBHOOK_URL.')
    exit()

# ユーザのSuica id
USERS_SUICA_ID = os.environ.get('USERS_SUICA_ID', None)
if not USERS_SUICA_ID:
    print('No USERS_SUICA_ID.')
    exit()
users_suica_id = USERS_SUICA_ID.split(',')
print(users_suica_id)

# Suica待ち受けの1サイクル秒
TIME_CYCLE = 1.0
# Suica待ち受けの反応インターバル秒
TIME_INTERVAL = 0.2
# タッチされてから次の待ち受けを開始するまで無効化する秒
TIME_WAIT = 3


def main():
    # NFC接続リクエストのための準備
    # 212F(FeliCa)で設定
    target_req_suica = nfc.clf.RemoteTarget("212F")
    target_req_nanaco = nfc.clf.RemoteTarget("212F")
    # 0003(Suica)
    target_req_suica.sensf_req = bytearray.fromhex("0000030000")
    # 04c7(nanaco)
    target_req_nanaco.sensf_req = bytearray.fromhex("0004c70000")

    print('Reader waiting...')
    while True:
        clf = nfc.ContactlessFrontend('usb')

        # Suica待ち受け開始
        # clf.sense( [リモートターゲット], [検索回数], [検索の間隔] )
        target = clf.sense(target_req_suica, target_req_nanaco, iterations=int(TIME_CYCLE//TIME_INTERVAL)+1 , interval=TIME_INTERVAL)

        if target:
            tag = nfc.tag.activate(clf, target)
            print(tag)
            print(type(tag))

            #IDmを取り出す
            idm = str(binascii.hexlify(tag.idm), 'utf-8')
            print('Suica detected. idm = {}'.format(idm))

            if idm in users_suica_id:
                print('OK! K')
                push_slack(True, 'K')
            else:
                print('Kさん以外のSuicaです')
                push_slack(False)

            print('Sleep {} seconds'.format(TIME_WAIT))
            time.sleep(TIME_WAIT)
            print('Suica waiting...')

        clf.close()


def push_slack(result, username=None):
    if username:
        text = '{}さんのSuicaを認証しました。'.format(username)
    else:
        text = '知らない人のSuicaを読みました。'
    post_json = {
        'text': text,
        'username': 'RC-S380'
    }
    requests.post(URL, data=json.dumps(post_json))


if __name__ == "__main__":
    print('Start reader')
    main()