import sys
import email.py

def create_multipliers():
    return [lambda x:i*x for i in range(5)]
    """ 
	�������� ����������, ������������ � ����������, ������ �� ����� ������ ���������� �������.
	�������� i ������ � ���������� ������� ��������� �� ����� �� ������. �������� i �� �����.
	""" 

	
for multiplier in create_multipliers(): print multiplier(2)
""" 
�� ���������� ������ ���������� ����. ��������� ��������, ������ ���������� ��������� � ���� ������� tab ��� ��������.
�������� ���������� ������ ���� � ����� ������
""" 

def sys(i): # ����������� ���� � ������� �������� ����������� ���������� Python
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
    ���������� ����������� �������. �������� ������������ ����������� match-case 
    """ 

def func0():
    e = None
    try:
        sys(int(sys.argv[1])) # ����������� ���� � ������� �������� ����������� ���������� Python
    """ 
	� Python 3 ������ � ����� ���������� ���������� �� ��� ���������.
	����� ��������� ������ �� ������ ����� ���������� �� ��������� ����� �����.
	"""
    except KeyError as e:
        print('key error')
    except ValueError as e:
        print('value error')
    print(e)


func0()