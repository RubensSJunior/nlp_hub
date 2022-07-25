import pandas as pd
import tweepy as tw
from datetime import datetime
from pymongo import MongoClient
from pymongo import errors
import json

def conecta_mongo(usuario,senha):
    client = MongoClient("mongodb://{}:{}@mongodb:27017/db_nlp".format(usuario,senha))
    return client

def retorna_termos_validos(client):
    db = client["db_nlp"]
    collection = db["collection_twittes"]
    list_tweets = []
    for x in collection.find():
            list_tweets.append(x)
    return list_tweets
def clean_dados(list_tweets,client):
    db = client["db_nlp"]
    df_tweets = pd.DataFrame()
    df_tweets_metions = pd.DataFrame()
    df_tweets_hastag = pd.DataFrame()
    for tweet in list_tweets:
        tw = {}
        tw["id_tweet"] = tweet["id"]
        tw["created_at"] = datetime.strftime(datetime.strptime(tweet["created_at"],'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')
        tw["text"] = tweet["full_text"]
        tw["size_text"] = tweet["display_text_range"][1]
        tw["id_user"] = tweet["user"]["id"]
        tw["id_termo"] = tweet["id_termo"]
        try:
            filter = { 'id_tweet': tw["id_tweet"], 'id_termo': tw["id_termo"] }
            new_values = { "$set": tw }
            db.collection_clean_twittes_text.update_one(filter, new_values, upsert=True)
        except Exception as e:
            print("An exception occurred ::", e)


        for mention in tweet["entities"]["user_mentions"]:
            mt = {}
            mt["id_tweet"] = tw["id_tweet"]
            mt["id_user_mention"] = mention["id"]
            mt["id_user_mentioned"] = tw["id_user"]
            mt["id_termo"] = tweet["id_termo"]
            try:
                filter = { 'id_tweet': mt["id_tweet"], 'id_termo': mt["id_termo"] }
                new_values = { "$set": mt }
                db.collection_clean_twittes_metion.update_one(filter, new_values, upsert=True)
                
                
            except Exception as e:
                print("An exception occurred ::", e)

        for hashtag in tweet["entities"]["hashtags"]:
            ht = {}
            ht["id_tweet"] = tweet["id"]
            ht["hashtag"] = hashtag["text"]
            ht["id_termo"] = tweet["id_termo"]
            try:
                filter = { 'id_tweet': ht["id_tweet"], 'id_termo': ht["id_termo"] }
                new_values = { "$set": ht }
                db.collection_clean_twittes_hashtag.update_one(filter, new_values, upsert=True)
            except Exception as e:
                print("An exception occurred ::", e)

def salva_json_on_mongo(json_tw,client):    
    db = client["db_nlp"]
    for tweet in json_tw:
        try:
            db.collection_clean_twittes.insert_one(tweet._json)
        except:
            print("la")

def fecha_tudo(client):
    client.close()
    
    
    
cliente_mongo = conecta_mongo("user_twitter_script","pass_twitter_script")
lista_tweeter = retorna_termos_validos(cliente_mongo)
clean_dados(lista_tweeter,cliente_mongo)


fecha_tudo(cliente_mongo)