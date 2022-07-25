#### #### ###
import time
import pandas as pd
import tweepy as tw
from pymongo import MongoClient

list_acess = []
acess = {}
acess["consumer_key"] = ''
acess["consumer_secret"] = ''
acess["acessss_token"] = ''
acess["acessss_token_secret"] = ''
acess["bearer_token"] = ''
list_acess.append(acess)

acess = {}
acess["consumer_key"] = ''
acess["consumer_secret"] = ''
acess["acessss_token"] = ''
acess["acessss_token_secret"] = ''
acess["bearer_token"] = ''
list_acess.append(acess)


def conecta_mongo(usuario,senha):
    client = MongoClient("mongodb://{}:{}@mongodb:27017/db_nlp".format(usuario,senha))
    return client

def retorna_termos_validos(client):
    db = client["db_nlp"]
    collection = db["collection_termos"]
    lista_termos = []
    for x in collection.find({ "status": True}):
        lista_termos.append(x)
    return lista_termos

def conect_twitter(acess):
    consumer_key = acess["consumer_key"] 
    consumer_secret = acess["consumer_secret"]
    acessss_token = acess["acessss_token"]
    acessss_token_secret = acess["acessss_token_secret"]
    bearer_token = acess["bearer_token"]

    auth = tw.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(acessss_token,acessss_token_secret)
    api = tw.API(auth)
    return api

def busca_tweets(termo,api):
    search_query = termo + " -filter:retweets"
    cursor_tweets = tw.Cursor(api.search_tweets,
                tweet_mode='extended',
                q=search_query,
                ).items(500)

    tw_dict = {}
    tw_dict = tw_dict.fromkeys(['created_at', 'id', 'id_str', 'full_text', 'truncated', 'entities',
    'metadata', 'source', 'in_reply_to_status_id', 'in_reply_to_status_id_str',
    'in_reply_to_user_id', 'in_reply_to_user_id_str', 'in_reply_to_screen_name', 'user',
    'geo', 'coordinates', 'place', 'contributors', 'is_quote_status', 'retweet_count',
    'favorite_count','favorited', 'retweeted', 'lang'])

    json_tweets = []
    for tweet in cursor_tweets:
        json_tweets.append(tweet)
        for key in tw_dict.keys():
            try:
                tw_content = tweet._json[key]
                tw_dict[key].append(tw_content)
            except KeyError:
                tw_content = ""
                if(tw_dict[key] is None):
                    tw_dict[key] = [tw_content]
                else:
                    tw_dict[key].append(tw_content)
            except:
                tw_dict[key] = [tw_content]
    return json_tweets

def salva_json_on_mongo(json_tw,client,id_termo):    
    db = client["db_nlp"]
    for tweet in json_tw:
        tweet_add = tweet._json
        tweet_add["id_termo"] = id_termo
        try:
            filter = { 'id': tweet_add["id"], 'id_termo': id_termo }
            new_values = { "$set": tweet_add }
            db.collection_twittes.update_one(filter, new_values, upsert=True)
        except:
            a=1
def fecha_tudo(api,client):
    api.session.close()
    client.close()

def saveTweets():

    cliente_mongo = conecta_mongo("user_twitter_script","pass_twitter_script")
    termos_validos = retorna_termos_validos(cliente_mongo)
    tweetes = []

    for i in range(0,len(termos_validos)):
        api_twitter = conect_twitter(list_acess[i])
        tweetes.append(busca_tweets(termos_validos[i]["termo"],api_twitter))
        time.sleep(5)
        api_twitter.session.close()
        salva_json_on_mongo(tweetes[0],cliente_mongo,termos_validos[i]["termo"])
    fecha_tudo(api_twitter,cliente_mongo)
    return "saveTweets"


saveTweets()