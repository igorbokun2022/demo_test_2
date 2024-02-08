from telethon import TelegramClient, events
import streamlit as st
import asyncio

def telegram_parser(send_message_func=None, loop=None):
    '''Телеграм парсер'''

    # Параметры из my.telegram.org
    api_id = 16387030
    api_hash = '07bfab67941aa8ebe50f836e3b5c5704'
    session='telemesmonitor'
    #channel_href ='t.me/rian_ru'   
    # Канал источник новостей @prime1
    channel_source = 'https://t.me/prime1'
    cl_mas_data=[]
   
    client = TelegramClient(session, api_id, api_hash, loop=loop)
    client.start()

    @client.on(events.NewMessage(chats=channel_source))
    async def handler(event):
        '''Забирает посты из телеграмм каналов и посылает их в наш канал'''

        if send_message_func is None:
            cl_mas_data.append(event.raw_text)
            print(str(len(cl_mas_data)))
            st.info(str(len(cl_mas_data)))
            print(event.raw_text, '\n')
            st.text(event.raw_text) 
        else:
            await send_message_func(f'@prime1\n{event.raw_text}')

    return client


if __name__ == "__main__":

    client = telegram_parser(send_message_func=None, loop=None) 
    client.run_until_disconnected()
    
    
    
   