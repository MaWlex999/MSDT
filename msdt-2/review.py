import sys
import email.py

def create_multipliers():
    return [lambda x:i*x for i in range(5)]
    """ 
	Значения переменных, используемых в замыканиях, ищутся во время вызова внутренней функции.
	Значение i ищется в окружающей области видимости во время ее вызова. Итерации i не будет.
	""" 

	
for multiplier in create_multipliers(): print multiplier(2)
""" 
Не соблюдение правил оформления кода. Вложенные элементы, должны отмечаться отступами в виде символа tab или пробелов.
Элементы синтаксиса должны идти с новой строки
""" 

def sys(i): # Пересечение имен с именами модулями стандартной библиотеки Python
    if i==1:
        raise KeyError(1)
    if i==2:
        raise ValueError(2)
    if i==3:
        raise ValueError(3)
    if i==4:
        raise ValueError(4)
    if i==5:
        raise ValueError(5)
    if i==6:
        raise ValueError(6)
    if i==7:
        raise ValueError(7)
    """ 
    Громоздкая конструкция условий. Логичнее использовать конструкцию match-case 
    """ 

def func0():
    e = None
    try:
        sys(int(sys.argv[1])) # Пересечение имен с именами модулями стандартной библиотеки Python
    """ 
	В Python 3 объект в блоке исключения недоступен за его пределами.
	Нужно сохранить ссылку на объект блока исключения за пределами этого блока.
	"""
    except KeyError as e:
        print('key error')
    except ValueError as e:
        print('value error')
    print(e)


func0()