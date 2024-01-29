import streamlit as st
from multiapp import MultiApp
import PIL as pil
import requests
from bs3 import BeautifulSoup
import xlwt

flagLocal=False
if flagLocal==True: path='F:/_Data Sience/Веб_приложения/Streamlit/demo_test_2/'
else:               path=''

st.set_page_config(layout="wide")
st.header('Демо. Веб-приложение на питоне')
img=pil.Image.open(path+'photo.jpg')
st.sidebar.image(img, width=250)

def prog1():
    # создание книги Excel 
    wb = xlwt.Workbook()
    # создание страницы Excel
    ws = wb.add_sheet('Data')

    # установка шрифта и стиля для записи в Excel
    font0 = xlwt.Font()
    font0.name = 'Times New Roman'
    font0.colour_index = 0
    style0 = xlwt.XFStyle()
    style0.font = font0
    style0.alignment.horizontal='center'
    style0.alignment.vertical='center'

    # определение ссылки на страницу сайта
    url_page = 'https://stat.cooperation.uz/procurement/corporate'
    # запрос всего текста этой страницы сайта на HTML
    response = requests.get(url_page)
    text_url = BeautifulSoup(response.text, 'lxml')
    # получение текста всех строк всех таблиц (одной!) на этой странице (между тегами <tr>)

    rows_text = text_url.find_all("tr")


    # установка индекса строки
    i=0    
    # цикл по всем строкам, найденным на данной странице 
    for r in rows_text:
        # выбор текста текущий строки
        row_text = r.find_all("td")
        # запись каждого поля текущей строки в текстовом формате (в т.ч. чисел) в список
        row_data = [field_text.text for field_text in row_text]
        st.text(str(row_data))
        print(row_data) # вывод текущей строки на экран питон
        # запись каждого поля текущей строки из списка в буфер записи Excel 
        for j in range(0,len(row_data)):
            ws.write(i, j, row_data[j], style0)
        i=i+1    
      
    wb.save(path+'parsing_data.xls') # сохранение записанных данных в файл Excel
    
    return

def prog2():
    return
def prog3():
    return
def myhelp():
    return
    
app = MultiApp()
app.add_app("prog1", prog1)
app.add_app("prog2", prog2)
app.add_app("prog3", prog3)
app.add_app("myhelp", myhelp)
app.run()
