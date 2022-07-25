import re
import nltk
import json

import pandas as pd
import tweepy as tw
from pymongo import errors
from datetime import datetime
from pymongo import MongoClient
import string

from textblob import TextBlob
from googletrans import Translator
from nltk.tokenize import TweetTokenizer
tk = TweetTokenizer()
from unidecode import unidecode
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer

from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer, TfidfVectorizer

import pickle
  
with open(r"data/model.pkl", "rb") as input_file:
    model = pickle.load( input_file)
    
with open(r"data/bow_article.pkl", "rb") as input_file:
    bow_article = pickle.load( input_file)
    
nltk.download('rslp')
spc = spacy.load("pt_core_news_md")
nltk.download('stopwords')
nltk.download('punkt')
stop_words = spacy.lang.pt.stop_words.STOP_WORDS
stemmer = nltk.stem.RSLPStemmer()
stopwor_inst = nltk.corpus.stopwords.words('portuguese')


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

def clean_dados(list_tweets,client,model,bow_article):
    db = client["db_nlp"]
    df_tweets = pd.DataFrame()
    df_tweets_metions = pd.DataFrame()
    df_tweets_hastag = pd.DataFrame()
    for tweet in list_tweets:

        # tweet = json.dumps(tweet)
        #tweet = json.loads(tweet)
        tw = {}

        tw["id_tweet"] = tweet["id"]
        tw["created_at"] = datetime.strftime(datetime.strptime(tweet["created_at"],'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')
        tw["text"] = tweet["full_text"]
        tw["text_cleaned"] =  transform_lemma(limpezaDeString(tweet["full_text"]))
        tw["size_text"] = tweet["display_text_range"][1]
        tw["id_user"] = tweet["user"]["id"]
        tw["id_termo"] = tweet["id_termo"]
                               
        X_padding = bow_article.transform([transform_lemma(limpezaDeString(tweet["full_text"]))])
        transformer = TfidfTransformer()
        X_padding_tf_idf = transformer.fit_transform(X_padding)
        tw["sentiment_predicted"] = str(model.predict(X_padding_tf_idf)[0])
        print(tw)
        try:
            filter = { 'id_tweet': tw["id_tweet"], 'id_termo': tw["id_termo"] }
            new_values = { "$set": tw }
            db.collection_clean_twittes_text.update_one(filter, new_values, upsert=True)
        except Exception as e:
            print("An exception occurred ::", e)


def salva_json_on_mongo(json_tw,client):    
    db = client["db_nlp"]
    for tweet in json_tw:
        try:
            db.collection_clean_twittes.insert_one(tweet._json)
        except:
            print("erro")
            

def clean_text(texto):
    '''
    Função para converter todas as letras para sua forma minúscula, selecionar apenas as letras,
    remover stopwords e lematizar o texto. 
    '''

    def remove_tweet_ruido(tweets_text):
        clean_text = re.sub(r'RT+', '', tweets_text) 
        clean_text = re.sub(r'@\S+', '', clean_text)  
        clean_text = re.sub(r'http\S+', '', clean_text) 
        clean_text = clean_text.replace("\n", " ")
        return clean_text

    ### Transforme as letras para minúscula ###
    minusculas = texto.lower()
    texto = remove_tweet_ruido(minusculas)
    ### Selecione apenas as letras do texto ##
    letras = re.findall(r'\b[A-zÀ-úü]+\b', texto)
    return letras


def fecha_tudo(client):
    client.close()
    
    
    
def limpezaDeString(texto):
    # Letras minúsculas
    texto = texto.lower()
    texto = re.sub(r" +", ' ', texto)
    # \n
    texto = re.sub(r"(\\n)+", "",texto);
    texto = re.sub(r"(\n)+", "",texto);

    # Use tokenize method
    geek = tk.tokenize(texto)
    sentence = []
    for word in geek:
        if  ('“' not in word)  & ('”' not in word) & ('…' not in word) & ("#" not in word) & ("@" not in word ) & ("htt" not in word ) & ( word[0] not in  string.punctuation) & (".com" not in word) & (".br" not in word) & (not word[0].isnumeric()):
            if re.match(r"[a-zA-Z]", word):
                sentence.append(unidecode(word))
            else:
                sentence.append((word))
    sentenca = ' '.join(sentence)

    palavras_sem_stopwords = [palavra for palavra in sentenca.split() if palavra not in stopwor_inst]
    palavras_sem_stopwords = ' '.join(palavras_sem_stopwords)
    # Espaços em branco
    palavras_sem_ponto = re.sub(r"\.", ' ', palavras_sem_stopwords)
    palavras_sem_espaco_duplo = re.sub(r" +", ' ', palavras_sem_ponto)
    palavras_sem_sem_k = re.sub(r"kkk", ':]', palavras_sem_espaco_duplo)
    palavras_sem_sem_k = re.sub(r":]k", ':]', palavras_sem_sem_k)
    palavras_sem_sem_k = re.sub(r":]k", ':]', palavras_sem_sem_k)
    palavras_sem_sem_a = re.sub(r"aaa", 'a', palavras_sem_sem_k)
    palavras_sem_sem_a = re.sub(r"aaa", 'a', palavras_sem_sem_a)
    palavras_sem_sem_r = re.sub(r"rrr", 'r', palavras_sem_sem_a)
    palavras_sem_sem_r = re.sub(r"rrr", 'r', palavras_sem_sem_r)
    palavras_sem_sem_i = re.sub(r"ii", 'i', palavras_sem_sem_r)
    palavras_sem_sem_i = re.sub(r"ii", 'i', palavras_sem_sem_i)
    palavras_sem_sem_h = re.sub(r"hh", 'h', palavras_sem_sem_i)
    palavras_sem_sem_h = re.sub(r"hh", 'h', palavras_sem_sem_h)
    palavras_sem_sem_o = re.sub(r"ooo", 'o', palavras_sem_sem_h)
    palavras_sem_sem_o = re.sub(r"oo", 'o', palavras_sem_sem_o)
    palavras_sem_sem_e = re.sub(r"eee", 'e', palavras_sem_sem_o)
    palavras_sem_sem_e = re.sub(r"ee", 'e', palavras_sem_sem_e)
    
    return palavras_sem_sem_e

def transform_lemma(sentence):
    lista_lemma = []

    for palavra in spc(sentence):
        if palavra.pos_ in ["ADJ","NOUN","VERB","ADV","DET","PROPN"]:
            lista_lemma.append(palavra.lemma_)
    return ' '.join(lista_lemma)


def cleanData():

    cliente_mongo = conecta_mongo("user_twitter_script","pass_twitter_script")
    lista_tweeter = retorna_termos_validos(cliente_mongo)
    clean_dados(lista_tweeter,cliente_mongo,model,bow_article)
    fecha_tudo(cliente_mongo)
    return "Funcionou até aqui"

cleanData()