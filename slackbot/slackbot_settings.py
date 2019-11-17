import os

# botアカウントのトークンを指定
API_TOKEN = os.environ.get('SLACK_API_TOKEN', None)
if not API_TOKEN:
    print('No API_TOKEN.')
    exit()

# このbot宛のメッセージで、どの応答にも当てはまらない場合の応答文字列
DEFAULT_REPLY = '😪'

# プラグインスクリプトを置いてあるサブディレクトリ名のリスト
PLUGINS = ['plugins']