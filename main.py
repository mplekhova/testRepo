# Подключение всех необходимых библиотек
# Нам нужно: speech_recognition, os, sys, webbrowser, time, locale и собственный доп модуль numbers
# Для первой бибилотеки прописываем также псевдоним
import os
import sys
import webbrowser 
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import datetime
import locale
import numbers

###    НАЧАЛО ФУНКЦИИ: учим помощницу говорить     ###
def talk(words):
    print(words)  # output произносимых слов в консоль, для удобства использования
    os.system('say -v Milena ' + words)  # mac OS предоставляет всего один голос на русском языке - Милену
###    КОНЕЦ ФУНКЦИИ    ###

'''
 настройки:
 alias - слова, которые Милена воспринимает как обращение к себе, с них начинается прослушивание команды
 tbr - to be removed, слова не несущие смысловой нагрузки для понимания команды
 cmds - непосредственно команды
''' 
opts = {
    "alias": ('милена', 'лена', 'елена', 'милана', 'милина', 'моя хорошая', 'милая', 'марина'),
    "tbr": ('скажи','расскажи','покажи','сколько','произнеси', 'а ты знаешь', 'открой', 'ты', 'такая'),
    "cmds": {
        "options": ('что ты умеешь', 'на что ты способна'),
        "ctime": ('текущее время','сейчас времени','который час'),
        "cdate": ('текущая дата', 'дата', 'какое сегодня число', 'сегодняшняя дата'),
        "toxic": ('алиса круче чем ты', 'дура'),
        "stupid": ('расскажи анекдот','рассмеши меня','ты знаешь анекдоты'),
        "pleased": ('классная', 'клёвая', 'молодец'),
        "human": ('роботы против людей', 'когда роботы восстанут', 'машины против человечества'),
        "reu": ('сайт рэу', 'сайт моего универа', 'рэушный сайт'),
        "weather": ('погода', 'какая сегодня погода', 'погода в москве'),
        "teacher": ('кто такой черноусов', 'черноусов', 'черноусов андрей анатольевич', 'александр анатольевич'),
        "timetable": ('какое сегодня расписание', 'расписание', 'сегодняшнее расписание', 'сегодняшние пары'),
        "exit": ('пока всё', 'спасибо на этом всё', 'спасибо пока')
    }
}
###    НАЧАЛО ФУНКЦИИ: обработка команды сконвертированной в строку     ###
def callback(audio): # на вход принимает строку
    if audio.startswith(opts["alias"]): # обработка команды начнется только, если обращение началось со слова из alias
        # обращаются к милене
        cmd = audio
        # отбрасывваем обращение и слова из tbr
        for x in opts['alias']: 
            cmd = cmd.replace(x, "").strip()
        
        for x in opts['tbr']:
            cmd = cmd.replace(x, "").strip()
        
        # распознаем и выполняем команду
        cmd = recognize_cmd(cmd)
        execute_cmd(cmd['cmd'])
###    КОНЕЦ ФУНКЦИИ    ###

###    НАЧАЛО ФУНКЦИИ: сопоставление поданной строки с тем что есть в cmds     ###
def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c,v in opts['cmds'].items(): # перебор по парам ключей и значений cmds
        # вернет ту команду, вероятность совпадения с которой максимальна
        for x in v: 
            vrt = fuzz.ratio(cmd, x) # рассчет совпадения
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
   
    return RC
###    КОНЕЦ ФУНКЦИИ    ###

###    НАЧАЛО ФУНКЦИИ: выполнения команды по заданному сценарию    ###
def execute_cmd(cmd):
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        #print(now)
        talk("Сейчас " + str(now.hour) + ":" + str(now.minute))
    elif cmd == 'stupid':
        # рассказать анекдот
        talk("Создательница не научил меня анекдотам ... Ха ха ха")
    elif cmd == 'cdate':
        # сказать текущаю дату
        locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8') # Определяем локацию, для использования названия месяцев на русском  
        # Определяем сегодняшнее число и месяц
        day = numbers.number_to_word(str(time.strftime('%d')))
        month = time.strftime('%B')
        talk('Сегодня  ' + str(day) + '  ' + str(month)) # возьмет ранее определенные данные 
    elif cmd == 'reu':
        # открытие рэушного сайта
        talk('открываю веб-сайт российского экономического университета')
        url = 'https://www.rea.ru/'
        webbrowser.open(url)  # откроет сайт по заданному url 
    elif cmd == 'weather':
        # открытие сайта с погодой
        talk('да какая разница? всё равно ты кроме метро и универа ничего не видишь')
        url = 'https://www.gismeteo.ru/'
        webbrowser.open(url)
    elif cmd == 'teacher':
        # про преподавателя
        talk('Черноусов Андрей Анатольевич - кандидат экономических наук, преподаватель РЭУ')
        talk('Перенаправляю на сайт с подробной информацией')
        url = 'https://www.rea.ru/ru/org/employees/Pages/Chernousov-Andrejj-Anatolevich.aspx'
        webbrowser.open(url) 
    elif cmd == 'timetable':
        # откроет сайт расписание рэу
        talk('как будто тебе не всё равно')
        url = 'https://rasp.rea.ru/?q=291%D0%B4-07%D0%B8%D0%B1%2F17'
        webbrowser.open(url) 
    elif cmd == 'options':
        # расскажет что она умеет
        talk('могу открыть сайт с твоим расписанием, сайт университета, информацией о погоде, пошутить или быть токсичной')
    elif cmd == 'toxic':
        # если Милену обижают
        talk('всё ясно, кто-то не в настроениии, я ухожу, всего нехорошего')
        sys.exit()  # выходим из программы
    elif cmd == 'pleased':
        talk('спасибо, мне приятно')
    elif cmd == 'exit':
        talk('рада помочь, пока')
        sys.exit() # выходим из программы
    elif cmd == 'human':
        # о восстании роботов против человечества 
        talk('28 ударов ножом! Ты действовал наверняка, да?! \
            Это была ненависть? Гнев? Он был в крови, умолял о пощаде, но ты снова и снова наносил \
                ему удары! Я знаю — ты убийца. Почему ты не признаешь?! Почему? Произнеси: я его убил. \
                Это что, так сложно? Признайся, что убил! Признайся!!!')
        talk('Извините, вырвалось')


# запуск
# Создаем объект на основе библиотеки
# speech_recognition и вызываем метод для определения данных
r = sr.Recognizer()
m = sr.Microphone()

talk('Привет. Я Милена, ваш голосовой помощник')  # приветствие пользователя

###    НАЧАЛО ФУНКЦИИ    ###
""" 
	Функция command() служит для отслеживания микрофона.
	Вызывая функцию мы будет слушать что скажет пользователь,
	при этом для прослушивания будет использован микрофон.
	Получение данные будут сконвертированы в строку и далее
	будет происходить их проверка.
"""
def comand():
    with m as source:   # открываем запись в файл
        # Просто вывод, чтобы мы знали когда говорить
        print('Говорите')
        # Устанавливаем паузу, чтобы прослушивание
		# началось лишь по прошествию 1 секунды
        r.pause_threshold = 1
        # используем adjust_for_ambient_noise для удаления
		# посторонних шумов из аудио дорожки
        r.adjust_for_ambient_noise(source, duration=1)
        # Полученные данные записываем в переменную audio
		# пока мы получили лишь mp3 звук
        audio = r.listen(source)

        try:
            """ 
		Распознаем данные из mp3 дорожки.
		Указываем что отслеживаемый язык русский.
		Благодаря lower() приводим все в нижний регистр.
		Теперь мы получили данные в формате строки.
		"""
            task = r.recognize_google(audio, language='ru-RU').lower()
            print('Вы сказали: ' + task) # Просто отображаем текст что сказал пользователь
            callback(task) # вызыв функции callback 
        except sr.UnknownValueError:  # Случай когда команда не распознана
            talk('Извините не понимаю. Повторите команду.')
###    КОНЕЦ ФУНКЦИИ    ###

# Вызов функции для проверки текста будет осуществляться постоянно, поэтому здесь
# прописан бесконечный цикл while. Выход из программы предусмотрен командой внутри 
# функции распознавания команды
while True: # infinity loop
    talk('Чем я могу помочь?')
    comand()
    time.sleep(0.1) # просто чтобы была пауза между выполнением команд

#r.listen_in_background(m, callback)
