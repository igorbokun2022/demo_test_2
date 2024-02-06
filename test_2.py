import streamlit as st
import PIL as pil

import httpx
import asyncio
import feedparser
from collections import deque 

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


if __name__ == "__main__":

    flagLocal=False

    if flagLocal==True: path='F:/_Data Sience/Веб_приложения/Streamlit/demo_test_2/'
    else:               path=''

    cl_mas_data=[]

    st.set_page_config(layout="wide")
    st.header('Демо. Веб-приложение на питоне. Визуальный интеллектуальный анализ новостей')
    img=pil.Image.open(path+'photo.jpg')
    st.sidebar.image(img, width=250)
    

    # Очередь из уже опубликованных постов, чтобы их не дублировать
    posted_q = deque(maxlen=30)

    # 50 первых символов от текста новости - это ключ для проверки повторений
    n_test_chars = 50

    httpx_client = httpx.AsyncClient()
    
    for i in range(1,2):
        asyncio.run(rss_parser(httpx_client, posted_q, n_test_chars))