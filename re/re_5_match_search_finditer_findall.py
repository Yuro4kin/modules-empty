import re

# Свойства и методы объекта match

# Существует два различных подхода применения регулярных выражений:
# «здесь и сейчас» для однократного применения правила;
# компиляция и обработка, для многократного использования одного и того 


# Возможности извлечения результатов обработки строк дает объект re.Match

# индекс      _____0________
text = "<font color=#CC0000>"
# группы      ___1__ ___2___

match = re.search(r"#[\da-fA-F]{6}\b", text)
print(match)
# на выходе получаем объект re.Match со следующими свойствами:
# <re.Match object; span=(12, 19), match='#CC0000'>

# Свойства и методы объекта match
match_1 = re.search(r"(\w+)=(#[\da-fA-F]{6})\b", text)
# в шаблоне есть 
# две сохраняющие группы: 1     2

# метод search возвращает полное вхождение под индексом 0, которое нашли
# под индексами 1 и 2 сохраняющие группы, ключ и значение

print(match_1)

# метод search и другие ему подобные создают сохраняющие группы значений:
print(match.group(0))

print(match_1.group(0))
print(match_1.group(1))
print(match_1.group(2))

# Кортеж из груп, перечислим индексы через запятую, на выходе кортеж соответствующих значений
print(match_1.group(0, 1, 2))
# аналог - кортеж из груп, начиная с индекса 1
print(match_1.groups())
# lastindex содержит индекс последней сохраняющей группы,
# можем определить сколько групп содержится в match
print(match_1.lastindex)

# узнать позиции в тексте начала и конца группы,
# то для этого служат методы start и end: start это color - индексы как в строках
print(match_1.start(1))
print(match_1.end(1))

# Если по каким-то причинам группа не участвовала в совпадении
# (например, ее вхождение было от 0), то данные методы возвращают -1.
# Также мы можем получить сразу кортеж с начальной и конечной позициями для каждой группы:
print(match_1.span(0))
print(match_1.span(1))

# Для определения первого и последнего индексов, в пределах которых
# осуществлялась проверка в тексте, служат свойства:
print(match_1.endpos)
print(match_1.pos)

# свойство re: возвращает скомпилированное регулярное выражение
pattern = match_1.re
print(pattern)

# свойство string: возвращает анализируемую строку
print(match_1.string)

# определим две именованные сохраняющие группы, используя ключи: key и value.
# Воспользуемся методом объекта Match groupdict(), на выходе получим словарь
match_2 = re.search(r"(?P<key>\w+)=(?P<value>#[\da-fA-F]{6})\b", text)
# В результате, с помощью метода:
print(match_2.groupdict())
# можно получить словарь:  {'key': 'color', 'value': '#CC0000'}
# который содержит имя    группы и значение группа   значение
# НА ПРАКТИКЕ ОЧЕНЬ УДОБНО, КОГДА СОСТАВЛЯЕМ ШАБЛОН ИЗ ИМЕНОВАННЫХ ГРУПП,
# А ПОТОМ ОБРАЩАЕМСЯ ПО ОПРЕДЕЛЕННОМУ ИМЕНИ, ЧТОБ ПОЛУЧИТЬ СОХРАНЕННЫЕ ЗНАЧЕНИЯ


# Свойство match.lastgroup возвращает имя-ключ последней группы
#(или значение None, если именованных групп нет)
print(match_2.lastgroup)

# с помощью метода expand() можно формировать строку с использованием сохраненных групп:
# синтаксис:
# \g<name> - обращение к группе по имени;
# \1, \2, … - обращение к группе по номеру
# Формируем строку, сначала будет идти ключ, через : его значение
print(match_2.expand(r"\g<key>:\g<value>"))
# эквивалентная запись    r"\1:\2" - лучше не использовать, индексы могут измениться
# на выходе строка - 'color:#CC0000'



# Методы re.search, re.finditer и re.findall
# обратимся к методу re.search для поиска первого вхождения в тексте,
# удовлетворяющего регулярному выражению.
# синтаксис этого метода - три параметра 
#           re.search(pattern, string, flags)
# pattern – регулярное выражение - шаблон;
# string – анализируемая строка;
# flags – один или несколько флагов.
# особенностью метода search() является поиск именно первого вхождения
# если в строке несколько вхождений по данному шаблону, то будет найдено только первое вхождение
text_1 = "<font color=#CC0000 bg=#ffffff>"
#               атрибут 1      атрибут 2
match_3 = re.search(r"(?P<key>\w+)=(?P<value>#[\da-fA-F]{6})\b", text_1)
# второй атрибут никак не будет фигурировать в результатах объекта match
print(match_3)
# возвращаетс объект Match и он содержит первый атрибут
# выведет всего две группы для первого атрибута


# Если нужно найти все совпадения выделить обе группы, то можно воспользоваться методом
#   re.finditer(pattern, string, flags)
# который возвращает итерируемый объект, с помощью которого выполняется перебора всех найденных вхождений:
for match_4 in re.finditer(r"(?P<key>\w+)=(?P<value>#[\da-fA-F]{6})\b", text_1):
    print(match_4)
# внутри цикла будем выводить все наши совпадения
# можно находить несколько совпадений в одной строке


# Если на практике нам нужно получить лишь список найденных вхождений, групп
# и это проще реализовать с помощью метода findall() - синтаксис:
#    re.findall(pattern, string, flags)
match_5 = re.findall(r"(?P<key>\w+)=(?P<value>#[\da-fA-F]{6})\b", text_1)
print(match_5)
# Получим список из кортежей:  [('color', '#CC0000'), ('bg', '#ffffff')]
# В кортежах будут находиться полностью сохраняющие группы, полное вхождение будет отсутствовать

# Недостатком последнего метода является ограниченность полученных данных:
# здесь лишь список, тогда как два предыдущих метода возвращали объект re.Match,
# обладающий, как мы только что видели, богатым функционалом.
# Но, если списка достаточно, то метод findall может быть вполне удобным и подходящим.





