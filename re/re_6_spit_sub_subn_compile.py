import re

# Методы re.match, re.split, re.sub, re.subn, re.compile

# Синтаксис match: 
#    re.match(pattern, string, flags)
# который определяет совпадение шаблона pattern в начале строки string
# с учетом флагов flags (если они указаны). Обратите внимание, в отличие от
# метода search, который ищет совпадение шаблона в любом месте строки,
# метод match смотрим совпадение только вначале.
# Он возвращает объект совпадения re.Match, либо значение None,
# если шаблон не был найден.
# Рассмотрим такой пример. Пусть в строке ожидается номер телефона в формате:
# +4(xxx)xxx-xx-xx
# где x – любая цифра. Нужно проверить и извлечь данный формат.
# Для этого пропишем следующее правило:

text = " +4(123)456-78-90"
match = re.match(r"\+4\(\d{3}\)\d{3}-\d{2}-\d{2}", text)
# (\d{3}\) - три цифры в круглых скобках             
print(match)
# получим объект Match совпадения:
# <re.Match object; span=(0, 16), match='+7(123)456-78-90'>
# Но, если вначале строки добавить любой символ - например пробел,
# text = " +4(123)456-78-90"
# то совпадение найдено не будет None, т.к. метод match выполняет
# поиск только сначала строки, в этом единственное отличие от метода search().


#   re.split
# метод
#   re.split(pattern, string, flags)
# выполняет разбивку строки string по заданному шаблону pattern.
# Например, у нас имеется вот такой многострочный текст:
text_1 = """<point lon="40.8482" lat="52.6274" />
<point lon="40.8559" lat="52.6361" />; <point lon="40.8614" lat="52.651" />
<point lon="40.8676" lat="52.6585" />, <point lon="40.8672" lat="52.6626" />
"""
# Требуется получить множество строк, которые разделяются между собой
# или переносом строки (\n), или символами ; и ,.
# Воспользуемся методом split со следующим шаблоном и укажем у него разделитель \n;, :
match_1 = re.split(r"[\n;,]+", text_1)
# \n;, - указываем символы по которым можно разбивать строки 
print(match_1)
# На выходе получим список из следующих строк элементов
# выделили все элементы, разбили между собой и получили строки


# Следующий метод sub() выполняет замену в строке string найденных совпадений
# строкой repl или результатом работы ф-ции
# Синтаксис:
#     re.sub(pattern, repl, string, count, flags)
# pattern – регулярное выражение;
# repl – строка или функция для замены найденного выражения;
# string – анализируемая строка;
# count – максимальное число замен (если не указано, то неограниченно);
# flags – набор флагов (по умолчанию не используются).

# Выполняет замену в строке найденных совпадений строкой или результатом
# работы функции repl и возвращает преобразованную строку.
# В качестве примера с помощью метода sub преобразуем вот такой текст:
text_2 = """Istanbul
London
Berlin
Madrid
Rome"""

# в множество строк
# в список формата HTML:
# <option>Istanbul</option>
# <option>London</option>
# <option>Berlin</option>
# <option>Madrid</option>
# <option>Rome</option>

# шаблон и следующим параметром порядок замены найденных вхождений:
match_2 = re.sub(r"\s*(\w+)\s*", r"<option>\1</option>\n", text_2)
# \s*   - пробельные символы 
# (\w+) - выделяем слово
# \1    - обращаемся к выделенному слову
# <option> - тег до и после слова </option>
# \n       - перенос строки
print(match_2)
# на выходе строка - список, мы взяли каждую строку и вместо нее подставили строчку
# в строке замены repl мы можем использовать ссылки на сохраняющие группы.
# В данном случае ссылка \1 содержит выделенный город из текста.
# Затем эта строка окаймляется тегами <option>\1</option>
# и получается искомый список.

# Но, кроме строки можно передавать ссылку на функцию,
# которая должна возвращать строку, подставляемую вместо найденного вхождения.
# Например, добавим тегам option атрибут value и сформируем такой список,
# где value меняется от 1 до 5:
# <option value='1'>Istanbul</option>
# <option value='2'>London</option>
# <option value='3'>Berlin</option>
# <option value='4'>Madrid</option>
# <option value='5'>Rome</option>
# Для этого вначале определим функцию:

count = 0
def replFind(m):        # принимает один аргумент, m объект Match
    global count        # обращается к глобальной переменной count 
    count += 1          # внутри ф-ции увеличиваем на 1
    return f"<option value='{count}'>{m.group(1)}</option>\n" # возвращаемый формат строки
                        # с помощью метода group() объекта Match обртаимся
                        # к сохраняющей группе (\w+) по индексу 1 и скажем
                        # то что мы выделили (\w+) подставим вместо строки {m.group(1)}
                        # {count} - подставлено будет значение переменной count
list_1 = re.sub(r"\s*(\w+)\s*", replFind, text_2)
#                               replFind - ссылка на функцию
print(list_1)
# <option value='1'>Istanbul</option> - добавлен атрибут value и его значение 1
# вызываем каждый раз функцию replfind, увеличиваем переменную count на 1,
# между тегами option сохраняем, что было в первой сохраняющей группе {m.group(1)}
# добавлен атрибут value и его значения


# Аналогично работает и метод
# subn(pattern, repl, string, count, flags)
# Только он возвращает не только преобразованную строку, но и число произведенных замен:
list_2, total = re.subn(r"\s*(\w+)\s*", r"<option>\1</option>\n", text_2)
# list_2 - то что мы получаем на выходе преобразованная строка
# total - колличество замен 
print(list_2, total)


# re.compile
# синтаксис метода
#     re.compile(pattern, flags)
# который выполняет компиляцию регулярного выражения
# и возвращает его в виде экземпляра класса Pattern.
# КОГДА ЦЕЛЕСООБРАЗНО ИСПОЛЬЗОВАТЬ - КОГДА ФОРМИРУЕМ ШАБЛОН И ПРЕДПОЛАГАЕМ, ЧТО
# МНОГО-МНОГО РАЗ ЕГО БУДЕМ ИСПОЛЬЗОВАТЬ
# Скомпилируем заранне,re.compile(pattern, flags) --> получим на выходе ссылку
# --> на объект Pattern --> потом через экземпляр этого объекта Pattern будем
# вызывать все те самые методы, что мы говорили, но уже не компилируя шаблон повторно.
# Компиляция регулярного выражения выполняется,
# если один и тот же шаблон используется многократно.
# Например, нашу предыдущую программу можно записать так:
# Преобразуем текст с помощью двух методов subn и sub используя один и тот же шаблон

text_2 = """Kyiv
Minsk
Amsterdam
Madrid
Rome"""

count = 0
def replFind_1(m):
    global count                                        # если нужно работать с глобальной переменной, эта строчка говорит, что дальше будем работать с переменной count как с глобальной переменной
    count += 1
    return f"<option value='{count}'>{m.group(1)}</option>\n"
 
rx = re.compile(r"\s*(\w+)\s*")                         # компилируем compile и получаем ссылку на класс Pattern
print(type(rx), "\n")                                   # <class 're.Pattern'>
print('Вызываем метод subn\n')
list, total = rx.subn(r"<option>\1</option>\n", text_2) # через ссылку вызываем метод subn 
# <option>\1</option>\n - и говорим что вместо найденного вхождения подставляем строчку
list2 = rx.sub(replFind_1, text_2)                      # вызываем метод sub, указывая ссылку на ф-цию
#              replFind_1 - ссылка на ф-цию
print(list, total, list2, sep="\n")                     # вывод рез-та в консоль
print('Вызываем метод sub\n')
# Для ускорения программы шаблон компилируется зараннее и затем его просто использовали
# Если в программах нужны подобные действия, то лучше компилировать шаблоны зараннее


# В общем случае, класс Pattern имеет все те же методы,
# что мы рассмотрели на этом и предыдущем занятиях модуля re
# и несколько уникальных свойств:

# flags – возвращает список флагов, которые были установлены при компиляции;
# pattern – строка исходного шаблона;
# groupindex – словарь, ключами которого являются имена сохраняющих групп,
# а значениями – номера групп (пустой, если имена не используются).

# Вот так можно оперировать регулярными выражениями через методы модуля re.
