'''
В этом файле описываются вспомогательные функции, необходимые для работы с редактором
'''
from PyQt4.QtCore import *

def adjustToTilesize(givenCoords, tileSize):
    '''
    Функция корректирует переданные координаты согласно текущему размеру тайла и возвращает объект
    класса QPoint с новыми координатами
    '''
    # Проверяем переданный размера тайла
    if type(tileSize) != int:  # Размер тайла должен быть целым числом
        raise TypeError('Uncorrect type of givenCoords! Must be int, but {} was given!'.format(type(tileSize)))
    elif tileSize < 2:         # Размер тайла не должен быть меньше 2
        raise ValueError('Value of givenCoords must be 2 and over!')
    # Масштабирование производитс в зависимости от того, каким типом является первый аргумент
    if type(givenCoords) == tuple or type(givenCoords) == list and len(givenCoords) == 2:
        # Если первый аргумент кортеж или список
        x = int(givenCoords[0]) // tileSize * tileSize
        y = int(givenCoords[1]) // tileSize * tileSize
    elif type(givenCoords) in [QPoint, QPointF]:
        # Если первый аргумент класс QPoint или QPointF
        x = int(givenCoords.x()) // tileSize * tileSize
        y = int(givenCoords.y()) // tileSize * tileSize
    else:
        # Во всех остальных случаях возбуждаем ошибку
        raise TypeError('givenCoords must be tuple, list, QPoint or QPointF, but {} was given!'.format(type(givenCoords)))
    return QPoint(x, y) # Возвращаем класс точки с целочисленными координатами