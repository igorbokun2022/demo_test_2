import streamlit as st
from telethon import TelegramClient, events


def telegram_parser(cl_mas_mes, send_message_func=None, loop=None):
    '''Телеграм парсер'''

    # Параметры из my.telegram.org
    # Параметры из my.telegram.or
    api_id = 16387030
    api_hash = '07bfab67941aa8ebe50f836e3b5c5704'
    # Сессия клиента teletho
    session = 'telemesmonitor'

    # Канал источник новостей @prime1
    channel_source = 'https://t.me/prime1'

    client = TelegramClient(session, api_id, api_hash)
    client.start()

    @client.on(events.NewMessage(chats=channel_source))
    async def handler(event):
        '''Забирает посты из телеграмм каналов и посылает их в наш канал'''

        if send_message_func is None:
            cl_mas_mes.append(event.raw)
            print(str(len(cl_mas_mes)+1))
            print(event.raw_text, '\n')
            st.text(str(len(cl_mas_mes)+1))
            st.text(event.raw_text)
        else:
            await send_message_func(f'@prime1\n{event.raw_text}')

    return client


if __name__ == "__main__":

    cl_mas_mes=[]    

    client = telegram_parser(cl_mas_mes)

    client.run_until_disconnected()