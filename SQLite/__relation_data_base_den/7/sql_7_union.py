import sqlite3 as sq
# SQLite #7: Оператор UNION объединения нескольких таблиц

# оператор UNION - объединяет таблицы построчно

# Например имеются две таблицы с одинаковой структурой
# записи из tab1 tab2 можно объединить в один сводный отчет с помощью оператора UNION

# SELECT score, `from` FROM tab1
# UNION SELECT val, type FROM tab2
# Возьмём данные из первой таблицы tab1 а именно поле score, поле `from`, f а не оператор FROM
# UNION - объединить --далее--> SELECT - выбрать из tab2, а именно поле val, type.
# Причем поле val совпадает по типу с полем score, a поле type совпадает по типу с полем `from` 
# Можем объединить записи друг за другом (объединение по полю score)

# записали поле `from` в обратных одинарных кавычках,
# чтобы указать, что это не оператор FROM, а поле с именем from
# Получим таблицу с шестью записями, причем, строки из исходных таблиц tab1 и tab2
# объединялись по значениям первого поля: сначала 100, потом 200 для tab1
# и 200 для tab2 и так далее.

# Например оставим только уникальные (неповторяющиеся) значения
# Вообще, оператор UNION оставляет только уникальные значения записей, повторяющиеся отбрасывает
# SELECT score FROM tab1
# UNION SELECT val FROM tab2

# Если же у первой таблицы tab1 во всех полях from укажем имя tab2:
# все записи поля `from` будут принимать значения tab2 вместо tab1
# UPDATE tab1 SET `from` = 'tab2'
# теперь первая и вторая таблицы совпадают по второму полю tab2

# Вернем поле в исходное значение tab1
# UPDATE tab1 SET `from` = 'tab1'

# Объединим данные следующим способом, возьмем данные из первой таблицы,
# только первое поле score, второе поле явно укажем 'table 1', чтоб СУБД знала как
# назвать второе поле, обзовем его через alias tbl
# UNION - когда будем объединять пропишем 'table 2' второе значение.
# Выполнив запрос, в втором поле(столбце) для записей из первой таблицы
# будет фигурировать значение table 1, а для записей из второй таблицы будет фигурировать 'table 2'

# Выполним сортировку сводной таблицы - данных, например, по полю score
# SELECT score, 'table 1' as tbl FROM tab1
# UNION SELECT val, 'table 2' FROM tab2
# ORDER BY score DESC

# Добавим фильтр и ограничение максимального числа записей, или 300, или 400
# добавим еще LIMIT 3 - взять первые три записи
# SELECT score, 'table 1' as tbl FROM tab1 WHERE score IN (300, 400)
# UNION SELECT val, 'table 2' FROM tab2
# ORDER BY score DESC
# LIMIT 3





