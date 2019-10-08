import json,re,time,datetime
from requests_oauthlib import OAuth1Session #OAuthのライブラリの読み込み
from util import close_connection
from util import create_connection
# from config import *

# CK, CS, AT, ATSは同ディレクトリ内でconfig.pyで設定しておく
twitter = OAuth1Session(CK, CS, AT, ATS) #認証処理

SEARCH_URL = "https://api.twitter.com/1.1/search/tweets.json" #タイムライン取得エンドポイント

def save(timelines, recent_tweet_id, diagnosis):
    for line in timelines['statuses']:
            if line['id_str'] == recent_tweet_id:
                print(diagnosis + ' は最新状態です：　' + recent_tweet_id)
                return False

            print(re.findall(r'端的に表すと「(.+?)」です。(.+)で例えると(.+?)。', line['text']))
            
            fa = re.findall(r'端的に表すと「(.+?)」です。(.+)で例えると「(.+?)」。', line['text'])
            if not fa:
                continue
            else:
                con = create_connection()
                last_id = None
                with con.cursor() as cursor:
                    cursor.execute("INSERT IGNORE INTO post (tweet_id, created_at, message, species, sample,diagnosis) VALUES (%s,%s,%s,%s,%s,%s)", (line['id_str'], datetime.datetime.strptime(line['created_at'],'%a %b %d %H:%M:%S +0000 %Y'), fa[0][0], fa[0][1], fa[0][2], diagnosis))
                    last_id = cursor.lastrowid
                close_connection(con)

                if last_id:
                    features = re.search(r'特性：(.+)', line['text'])
                    if features:
                        fs = features[1].replace('…', '').split('，')
                        con = create_connection()
                        with con.cursor() as cursor:
                            for fn in fs:
                                print(last_id, fn)
                                cursor.execute("INSERT INTO post_meta (post_id, name) VALUES (%s, %s)", (last_id, fn))
                        close_connection(con)

def search(params, recent_tweet_id, diagnosis):
    res = twitter.get(SEARCH_URL + params)
    if res.status_code == 200: #正常通信出来た場合
        timelines = json.loads(res.text) #レスポンスからタイムラインリストを取得

        if save(timelines, recent_tweet_id, diagnosis) == False:
            return
        
        time.sleep(5)
        if not timelines['search_metadata'].get('next_results'):
            print(timelines['search_metadata'])
        else:
            params = timelines['search_metadata']['next_results']
            search(params, recent_tweet_id, diagnosis)

    else: #正常通信出来なかった場合
        print("Failed: %d" % res.status_code)

def select_recent_tweet_id(diagnosis):
    con = create_connection()
    recent_tweet_id = -1

    with con.cursor() as cursor:
        cursor.execute("SELECT tweet_id FROM post WHERE diagnosis = %s ORDER BY created_at DESC LIMIT 1", diagnosis)
        recent_tweet_id = cursor.fetchone()

        if recent_tweet_id:
            recent_tweet_id = recent_tweet_id['tweet_id']
    close_connection(con)

    return recent_tweet_id

def run_diagnosis(query):
    params = "?q=" + query + "&lang=ja&result_type=mixed&count=10&include_entities=false"

    diagnosis = query[:-7]
    search(
        params=params,
        recent_tweet_id=select_recent_tweet_id(diagnosis),
        diagnosis=diagnosis
    )

if __name__ == "__main__":
    run_diagnosis("性格免許証 -恋愛")
    run_diagnosis("恋愛免許証 -性格")