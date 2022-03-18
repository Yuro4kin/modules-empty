import re

# Группировка и сохранение результатов поиска- Сохраняющие скобки и группировка

# из текста нужно выделить данные в формате ключ и значение
text = "lat = 5, lon=7"
match = re.findall(r"\w+\s*=\s*\d+", text)
# \w - ключ \s - пробел, знак =, затем какие-то цифры
print(match)
# ['lat = 5', 'lon=7']

text_1 = "pi=3, a = 5"
match_1 = re.findall(r"\w+\s*=\s*\d+", text_1)
# \w - ключ \s - пробел, знак =, затем какие-то цифры
print(match_1)
# ['pi=3', 'a = 5']


# Сделаем, чтоб наш шаблон учитывал только ключи lat и lon, явно пропишем, | - или
match_3 = re.findall(r"lat\s*=\s*\d+|lon\s*=\s*\d+", text)
print(match_3)
# ['lat = 5', 'lon=7']

# Недостаток, дважды прописываем шаблон, применим группирующие скобки
# ?: означает, что эта группирующая скобка является несохраняющей
text_2 = "lat = 5, lon=7, a=5"
match_4 = re.findall(r"(?:lat|lon|a)\s*=\s*\d+", text_2)
print(match_4)
# ['lat = 5', 'lon=7'], последний ключ a не выделен, т.к. он не удовлетворяет именам

# Чтобы увидеть оба уровня, копирование тоже, нужно убрать ?:
# нужно поставить круглые скобки () 
match_5 = re.findall(r"((lat|lon)\s*=\s*\d+)", text_2)
print(match_5)
# [('lat = 5', 'lat'), ('lon=7', 'lon')]

# Воспользуемся функционалом круглых скобок и отдельно сохраним ключи и значения
match_6 = re.findall(r"(lat|lon)\s*=\s*(\d+)", text_2)
print(match_6)
# Появляется список кортежей, где первым элементом идет ключ, вторым идет значение
# [('lat', '5'), ('lon', '7')], анализировать и брать гораздо удобнее кортеж
# () - круглые скобки позволяют лучше фрагментировать наши анализируемые данные
# Отличия сохраняющие скобки (), несохраняющие скобки (?:)

# Рассмотрим атрибут src у тега img
text_3 = "Картинка <img src='bg.jpg'> в тексте</p>"
match_7 = re.findall(r"<img\s+[^>]*src=[\"'](.+?)[\"']", text_3)
print(match_7)
# определяем тег <img, далее пробелы \s+,
# затем произвольные символы, исключая угловую скобку [^>]
# затем произвольные символы пока не встретим  *src
# далее внутри атрибута выделяем путь к файлу [\"']
# ['bg.jpg'] - путь который был веделен
# (.+?) - круглые скобки чтоб отдельно сохранить путь к графическому файлу



# Но как можно использовать эти сохранения непосредственно внутри регулярного выражения?
# К ним можно обратиться с помощью такого синтаксиса:
# \i  (i – натуральное число: 1, 2, 3, …)
# Например, наш шаблон сработает и в таких случаях:
# <img src="bg. jpg'>
# <img src='bg. jpg">
# то есть, если прописать разные типы кавычек.
# Этот недостаток легко поправить с помощью обращения к соответствующему сохранению.
# Перепишем выражение так:
#                              'bg.jpg\" - пустая строка
text_4 = "<p>Картинка <img src='bg.jpg'> в тексте</p>"
match_8 = re.findall(r"<img\s+[^>]*src=([\"'])(.+?)\1", text_4)
print(match_8)

# При запуске увидим:
# [("'", 'bg.jpg')]
# Первая кавычка – это первая сохраняющая скобка, а вторая строка – это вторая скобка.
# Все сработало, как и должно быть. Причем, изменив нашу строку с разными кавычками:
# на выходе получим пустую коллекцию. И, обратите внимание,
# использовать в символьных классах [] ссылки на сохранения нельзя,
# мы их можем прописывать только внутри самого регулярного выражения.

# В ряде случаев использовать цифры при обращении к сохраненному блоку не очень удобно,
# поэтому синтаксис позволяет назначать им имена:
# (?P<name>…)
# и, затем, обращаться к ним:
# (?P=name)
# Перепишем последнее регулярное выражение с использованием имен, получим:
# Тепеоь мы не связаны с индексом круглой скобки, мы обращаемся по имени
match = re.findall(r"<img\s+[^>]*src=(?P<quote>[\"'])(.+?)(?P=quote)", text_4)
print(match_8)
# [("'", 'bg.jpg')]
# Результат будет прежним. Однако, имена лучше назначать для сложных выражений,
# в простых они добавляют только громоздкости и здесь понятнее смотрятся цифры.


# Давайте в качестве практического примера рассмотрим парсинг вот такого xml-файла:
# Будем выделять lon lat с определенными значениями
with open("map.xml", "r") as f:
    lat = []
    lon = []
    for text in f:
        match = re.findall(r"<point\s+[^>]*?lon=([\"\'])([0-9.,]+)\1\s+[^>]*lat=([\"\'])([0-9.,]+)\1", text)
        print(match)
 
    print(lon, lat, sep="\n")

# Мы здесь открываем файл на чтение с использованием менеджера контекста а,
# затем, построчно считываем из файла информацию.
# Каждая строчка будет помещаться в переменную text.
# Далее выполняется анализ с помощью шаблона
# Для каждой строки применяем регулярное выражение, выделяя атрибуты lon и lat.
# начала обращаемся к тегу point. Затем ищем ключ lon и для него выделяем соотв. значения
# Тоже самое для lat

#Сначала идут пустые строчки, где не соответствуют шаблону
# В тех строчках, где нет данных атрибутов, имеем пустую коллекцию,
# а где формат совпадает, получаем четыре значения из сохраняющих круглых скобок.
# Здесь нам нужны значения с индексом 1 – для lon и 3 – для lat.
# [('"', '40.8482', '"', '52.6274')]
# И, записывая все в такую программу:

with open("map.xml", "r") as f:
    lat = []
    lon = []
    for text in f:
        match = re.findall(r"<point\s+[^>]*?lon=([\"\'])([0-9.,]+)\1\s+[^>]*lat=([\"\'])([0-9.,]+)\1", text)
        if len(match) > 0:
            lon.append(match[0][1])
            lat.append(match[0][3])
 
    print(lon, lat, sep="\n")
# делаем проверку, если match одержит либо какие-то данные, это не пустая квадратная скобка,
# то мы в lon добавляем это значение, берем 0 индекс, это кортеж будет. У этого
# кортежа берем первый индекс. Для lat берем 3 индекс.
# Результат - сформировано два списка, lon и lat, которые состоят из данных считанного
# с этого файла



# Но, как вы понимаете, это не лучшая реализация поставленной задачи.
# Что если регулярное выражение изменится и индексы станут другими?
# Придется поправлять весь программный код, связанный с этим шаблоном!
# Это не очень удобно. Здесь лучше использовать имена сохраняющих групп,
# а затем, обращаться к данным по этим именам. Поэтому перепишем программу так:
# Воспользуемся другим методом search(), который возвращает не просто коллекцию,
# а объект из которого можно получить словарь, содержащий коллекцию сохраненных именованных групп.
# и проверка, если совпадение было найдено, то мы берем словарь с сохраняющими группами
# и проверяем есть ли в этом слловаре ключи lon и lat. Если они есть то добавляем
# соответствующие значения. Получаем теже значения, но мы использовали имена
# сохраняющих груп. Это удобно, если в будущем шаблон изменится, программа остается неизменной.
# Также по именам обращаемся к данным и добавляем их в соответствующие коллекции.
#
with open("map.xml", "r") as f:
    lat = []
    lon = []
    for text in f:
        match = re.search(r"<point\s+[^>]*?lon=([\"\'])(?P<lon>[0-9.,]+)\1\s+[^>]*lat=([\"\'])(?P<lat>[0-9.,]+)\1", text)
        if match:
            v = match.groupdict()
            if "lon" in v and "lat" in v:
                lon.append(v["lon"])
                lat.append(v["lat"])
 
    print(lon, lat, sep="\n")


