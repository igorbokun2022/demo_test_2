import streamlit as st
import PIL as pil

import httpx
import asyncio
import feedparser
from collections import deque 

import pandas as pd
from pymorphy2 import MorphAnalyzer
from gensim import models, corpora
import numpy as np
import matplotlib as mplt
import nltk 
nltk.download('stopwords')
from nltk.corpus import stopwords
nltk.download('punkt')


class Prepare(object):    
    
    def __init__(self, mas, del_words, minf, maxf):
        #self.stemmer=stemmer 
        self.ru_stopwords = stopwords
        self.morph = morph 
        self.patterns = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
         
        self.mas=mas
        self.del_words=del_words
        self.minf=minf
        self.maxf=maxf
                        
    def prepareWord(self, old_word):
        new_word=old_word
        if not isinstance(old_word,str): return(" ") 
        #new_word=re.sub(self.patterns, ' ', new_word) 
        #new_word=new_word.translate(new_word,self.patterns)
        new_word=new_word.lower()
        #new_word=stemmer.stem(new_word)
        #new_word=Porter.stem(u(new_word))
        
        if new_word not in self.ru_stopwords and new_word not in self.del_words:  
            if len(new_word)>3:
                if 'NOUN' in morph.tag(new_word)[0]:
                    #print("("+old_word+") = "+new_word)
                    #print("*****************")             
                    return morph.parse(new_word)[0].normal_form            
        return " "     
    
#**********************************************************    

    def histogramm(self, all_mes_words):
    
        st.info("2. Началось формирование гистограммы обратных частот слов в сообщениях") 
         
        my_dictionary = corpora.Dictionary(all_mes_words)
        bow_corpus =[my_dictionary.doc2bow(mes, allow_update = True) for mes in all_mes_words]
   
        #print(bow_corpus)
        #print("*************************************")
        word_weight =[]
        for doc in bow_corpus:
            for id, freq in doc:
                word_weight.append([my_dictionary[id], freq])
        #print(word_weight)
        #print("*************************************")
        tfIdf = models.TfidfModel(bow_corpus, smartirs ='ntc')

        weight_tfidf =[]
        for doc in tfIdf[bow_corpus]:
            for id, freq in doc:
                weight_tfidf.append([my_dictionary[id], np.around(freq, decimals=3)]) 

        sort_weight_tfidf=sorted(weight_tfidf,key=lambda freq: freq[1]) 

        wrd=[]
        val=[]
        new_del_words=[]
        for i in range(len(sort_weight_tfidf)):
            curval=float(sort_weight_tfidf[i][1])
            if curval>=self.minf and curval<self.maxf: 
                #print(str(i))
                #print(sort_weight_tfidf[i]) 
                wrd.append(sort_weight_tfidf[i][0])
                val.append(float(sort_weight_tfidf[i][1]))
            else:
                new_del_words.append(sort_weight_tfidf[i][0])
        #print("*************************************")

        fig, ax = mplt.pyplot.subplots(figsize =(10, 7)) 
        ax.hist(val, bins = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        canvas = mplt.pyplot.get_current_fig_manager().canvas
        canvas.draw()
        buf = pil.Image.frombytes('RGB', canvas.get_width_height(), canvas.tostring_rgb())
            
        return new_del_words, fig, buf

#**********************************************************
        
    def prepare_all(self):
        st.info("1. Началось создание корпуса слов")
        all_mes_words=[]
        all_sent_words=[]
        all_words=[]
        print("*************************************") 
        for line in self.mas:  
            if len(line)<10: continue
            cur_mes_words=[]
            for sent in nltk.sent_tokenize(line): 
                cur_sent_words=[]
                for word in nltk.word_tokenize(sent):
                    word=self.prepareWord(word)  
                    if word!=" ":
                        cur_sent_words.append(word)
                        all_words.append(word)
                        cur_sent_words.append(word)
                        cur_mes_words.append(word)
                all_sent_words.append(cur_sent_words)        
            all_mes_words.append(cur_mes_words)    

        new_del_words, fig, buf=self.histogramm(all_mes_words)
        return all_mes_words, all_sent_words, all_words, new_del_words, fig, buf
    
    
#**********************************************************

def start_corpus(mas_data, minf, maxf):    
    #start_corpus(file, minf, maxf):   
    #df = pd.read_excel('postnews1.xlsx')
    #df.columns=['A']
    #mas_data = list(df['A'])
            
    prep = Prepare(mas_data, delw, minf, maxf)
    all_mes_words, all_sent_words, all_words, curdelw, fig, buf = prep.prepare_all()
    cur_del_words=curdelw
    corpus=all_mes_words
    
    list_posts=[]
    list_posts.append(" *****   Информация о корпусе слов     *****")
    list_posts.append("Всего преддложений = "+str(len(all_sent_words)))
    list_posts.append("Всего слов = "+str(len(all_words)))
    list_posts.append("Всего удалено слов = "+str(len(curdelw)))
    list_posts.append("Всего осталось слов = "+str(len(all_words)-len(curdelw)))
                 
    return buf, fig, list_posts, all_mes_words, all_sent_words


async def rss_parser(httpx_client, posted_q,
                     n_test_chars, send_message_func=None):
    '''Парсер rss ленты'''

    max_cnt_mes=100 
    cl_mas_mes=[]
    rss_link = 'https://rssexport.rbc.ru/rbcnews/news/20/full.rss'

    while True:
        try:
            response = await httpx_client.get(rss_link)
        except:
            await asyncio.sleep(10)
            continue

        feed = feedparser.parse(response.text)

        for entry in feed.entries[::-1]:
            summary = entry['summary']
            title = entry['title']

            news_text = f'{title}\n{summary}'

            head = news_text[:n_test_chars].strip()

            if head in posted_q:
                continue

            if send_message_func is None:
                cl_mas_mes.append(news_text)
                print(str(len(cl_mas_mes)))
                print(news_text, '\n')
                st.text(str(len(cl_mas_mes)))
                st.text(news_text)
            else:
                await send_message_func(f'rbc.ru\n{news_text}')

            posted_q.appendleft(head)

        await asyncio.sleep(5)
    
    return(cl_mas_mes)    


if __name__ == "__main__":

    flagLocal=False

    if flagLocal==True: path='F:/_Data Sience/Веб_приложения/Streamlit/demo_test_2/'
    else:               path=''

    cl_mas_data=[]
    minf=0.1
    maxf=1.0
    delw=[]
    cur_del_words=[]
    corpus=[]
    all_mes_words=[]

    # получен  запросом - await client.start(phone=phone, code_callback=code_callback)
    max_posts=1000

    #stemmer=nltk.stem.SnowballStemmer(language="russian")
    stopwords = stopwords.words('russian') 
    morph = MorphAnalyzer() 

    st.set_page_config(layout="wide")
    st.header('Демо. Веб-приложение на питоне. Визуальный интеллектуальный анализ новостей')
    img=pil.Image.open(path+'photo.jpg')
    st.sidebar.image(img, width=250)
    

    # Очередь из уже опубликованных постов, чтобы их не дублировать
    posted_q = deque(maxlen=30)

    # 50 первых символов от текста новости - это ключ для проверки повторений
    n_test_chars = 50

    httpx_client = httpx.AsyncClient()
    
    cl_mas_data=asyncio.run(rss_parser(httpx_client, posted_q, n_test_chars))
    
    minf=1
    maxf=1
    
    buf, fig, listp, allmes, sent_words =start_corpus(cl_mas_data, minf, maxf)
    st.info("3. Корпус создан. Вывод гистограммы")
    st.image(buf,60)
    
    