import requests # Модуль для обработки URL
from bs4 import BeautifulSoup # Модуль для работы с HTML
import time
import smtplib # Модуль для работы с почтой
import matplotlib.pyplot as plt
from datetime import datetime
import signal
import sys

# Основной класс:

class Currency:
  # Ссылка на нужную нам страницу
  DOLLAR_RUB = 'https://www.google.com/search?q=%D0%9A%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&sourceid=chrome&ie=UTF-8'
  
  # Заголовки для передачи вместе с URL
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
  
  current_converted_price = 0
  defference = 1 # Разница после которой будет отправлено сообщение на почту
  currency_history = []
  
  def __init__(self):
    # Установка курса валюты
    self.current_converted_price = float(self.get_currency_prise().replace(",", "."))
  
  # Метод для получения курса валюты
  def get_currency_prise(self):
    #парсим всю страницу
    full_page = requests.get(self.DOLLAR_RUB, headers=self.headers)
    
    # Разбираем через BeautifulSoup
    soup = BeautifulSoup(full_page.content, 'html.parser')
    
    # Получаем нужное для нас значение и возвращаем его
    convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
    return convert[0].text
  
  # Проверка изменения валюты
  def check_currency(self):
    currency = float(self.get_currency_prise().replace(",", "."))
    self.currency_history.append((datetime.now(), currency))
    self.plot_currency_history()
    if currency >= self.current_converted_price + self.defference:
      print("Курс сильно вырос, может пора что-то делать?")
      self.send_mail()
    elif currency <= self.current_converted_price - self.defference:
      print("Курс сильно упал, может пора что-то делать?")
      self.send_mail()
    
    print("Сейчас курс: 1 доллар = " + str(currency) + " RUB")
    time.sleep(3) # Засыпание программы на 3 секунды
    self.check_currency()
    
  # Отправка почты через SMTP
  def send_mail(self):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    
    server.login('xilalice64@gmail.com', 'Xaice9964!@#R')
    
    subject = 'Currency mail'
    body = 'Currency has been changed!'
    message = f'Subject: {subject}\n{body}'
    
    server.sendmail(
      'От кого',
      'Кому',
      message
    )
    server.quit()
  
  def plot_currency_history(self):
    times = [entry[0] for entry in self.currency_history]
    prices = [entry[1] for entry in self.currency_history]
    plt.plot(times, prices)
    plt.xlabel('Время')
    plt.ylabel('USD to RUB')
    plt.title('История обменного курса валюты')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('currency_history_plot.png')
    plt.close()
    
def signal_handler(sig, frame):
  print('Вы нажали Ctrl+C. Программа завершает работу.')
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Создание объекта и вызов метода
currency = Currency()
currency.check_currency()