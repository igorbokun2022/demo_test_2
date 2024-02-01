import streamlit as st
import PIL as pil

import httpx
import asyncio
import feedparser
from collections import deque
import threading

flagLocal=False

if flagLocal==True: path='F:/_Data Sience/Веб_приложения/Streamlit/demo_test_2/'
else:               path=''

cl_mas_data=[]

st.set_page_config(layout="wide")
st.header('Демо. Веб-приложение на питоне')
img=pil.Image.open(path+'photo.jpg')
st.sidebar.image(img, width=250)

async def rss_parser(httpx_client, posted_q,
                     n_test_chars, send_message_func=None):
    '''Парсер rss ленты'''

    rss_link = 'https://rssexport.rbc.ru/rbcnews/news/20/full.rss'
    maxcntmes=20
    flagCycle=True
 
    loop=asyncio.new_event_loop()   
 
    while flagCycle:
        try:
            response = await httpx_client.get(rss_link)
        except:
            await asyncio.sleep(10)
            continue
                    
        feed = feedparser.parse(response.text)

        for entry in feed.entries[::-1]:
             
            st.text(entry)               
              
            if len(cl_mas_data)>=maxcntmes:
                #print("STOP!")
                flagCycle=False
                exit
                
            summary = entry['summary']
            title = entry['title']
            news_text = f'{title}\n{summary}'
            head = news_text[:n_test_chars].strip()

            if head in posted_q: continue
           
            if send_message_func is None:
                print(str(len(cl_mas_data)+1))
                print(news_text, '\n')
                cl_mas_data.append(news_text)
            else:
                await send_message_func(f'rbc.ru\n{news_text}')
            
            posted_q.appendleft(head)    
                                      
        await asyncio.sleep(5)
    
    return cl_mas_data   
       
def go():
    print(" *** START GO *** ")
    cl_mas_data=asyncio.run(rss_parser(httpx_client, posted_q, n_test_chars))
    print("*** STOP GO *** ")
    return cl_mas_data 

#*************************************************************************************

but_start=st.sidebar.button("Начать чтение новостей")
if but_start:
    # Очередь из уже опубликованных постов, чтобы их не дублировать
    posted_q = deque(maxlen=20)
    # 50 первых символов от текста новости - это ключ для проверки повторени
    n_test_chars = 50
    httpx_client = httpx.AsyncClient()
    #threading.Thread(target=go).start()
    cl_mas_data=asyncio.run(rss_parser(httpx_client, posted_q, n_test_chars))
   
    print("****************************************")

    for i in range(0,len(cl_mas_data)):
        print(str(i+1))
        print(cl_mas_data[i])
        st.text(str(i+1))
        st.text(cl_mas_data[i])