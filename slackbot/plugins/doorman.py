import os
import re
import json
import requests
from slackbot.bot import respond_to, listen_to


URL = os.environ.get('SLACK_WEBHOOK_URL', None)
if not URL:
    print('No SLACK_WEBHOOK_URL.')
    exit()

# 「カギ開けて」「解錠して」等に反応するようにします
@listen_to('(鍵|カギ)+.*(開|あけ|空け)+')
@listen_to('(解錠)+')
@listen_to('(open)+.*(door)+', re.IGNORECASE)
@respond_to('(鍵|カギ)+.*(開|あけ|空け)+')
@respond_to('(解錠)+')
@respond_to('(open)+.*(door)+', re.IGNORECASE)
def openKeyOrder(message, *something):
    user = message.body.get('user')
    if not user:
        return

    # if カギが閉まっていたら :
    message.reply('わかりました。解錠します。')

    userid = message.channel._client.users[user]['name']
    print(userid + 'さんの命令でカギを開けます')

    post_json = {
        'text': '施錠されました。',
        'username': 'door',
        'link_names': 1
    }
    requests.post(URL, data=json.dumps(post_json))


# 「鍵閉めて」「施錠」等の場合はこちら
@listen_to('(鍵|カギ)+.*(閉|しめ|締め)+')
@listen_to('(施錠)+')
@listen_to('(close|lock)+.*(door)+', re.IGNORECASE)
@respond_to('(鍵|カギ)+.*(閉|しめ|締め)+')
@respond_to('(施錠)+')
@respond_to('(close|lock)+.*(door)+', re.IGNORECASE)
def closeKeyOrder(message, *something):
    user = message.body.get('user')
    if not user:
        return

    message.reply('わかりました。施錠します。')

    userid = message.channel._client.users[user]['name']
    print(userid + 'さんの命令でカギを閉めます。')


# 未許可なFeLiCaを許可ユーザとして追加する命令
@listen_to('(許可|追加)+')
@respond_to('(許可|追加)+')
def addUserOrder(message, *something):
    # 「」で囲まれている場合はユーザ名付きで許可する。
    m = re.search('「.*」', message.body['text'])
    if m:
        hit = m.group(0)
        username = hit[1:][:-1]
        message.reply('わかりました。直近のインスタントユーザを「{}」として追加します。有効期限は10分間です。'.format(username))
    else:
        username = 'John Doe'
        message.reply('わかりました。直近のインスタントユーザを追加します。有効期限は10分間です。')

    # 該当のFeLiCaを許可ユーザに追加する処理… userAddHandler(username, userid)