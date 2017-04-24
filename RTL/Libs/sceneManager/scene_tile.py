'''
В этом модуле описан класс тайла, который представляет из себя часть изображения
'''
from PyQt4.QtGui import *

class Tile(QGraphicsPixmapItem):
    PASSABILITY = ('Empty','Solid','Hover')		# Список доступных значений проходимости тайла
    def __init__(self, byteArray, x=0, y=0, z=0, passability = 'Empty', stripIndex = None):
        self.byteArray = byteArray                          # Сохраняем массив байтов (понадобится длс сравнения)
        super().__init__()                                  # Создаем суперкласс
        pixmap = QPixmap()
        pixmap.loadFromData(self.byteArray)                 # Преобразуем массив байтов в изображение
        self.setPixmap(pixmap)                              # Устанавливаем изображение
        self.setup(x, y, z, passability, stripIndex)        # Запускаем настройку атрибутов
    def setup(self, x, y, z, passability, stripIndex):
        # Метод настройки атрибутов тайла
        self.setShapeMode(QGraphicsPixmapItem.BoundingRectShape)# Устанавливаем квадратную форму тайла
        self.setPos(float(x), float(y))	# Помещаем тайл в позицию (x,y)
        self.setZValue(float(z))		# Устанавливаем высоту отрисовки тайла
        self.stripIndex = stripIndex	# Порядковый номер тайла в стрип-полосе. По умолчанию отсутствует
        self.passability = passability	# Тип проходимости тайла
    def changePassability(self, value):
        # Метод меняет тип проходимости тайла
        if value not in Tile.PASSABILITY: raise ValueError('Tile passability is not valid! Must be ("Empty","Solid","Hover")')
        self.passability = value
    def setStripIndex(self, index):
        # Метод устанавливает порядковый номер тайла в стрип-полосе
        self.stripIndex = index
    def getTileData(self):
        # Метод пакует информацию о тайле в словарь для сохранения в файл
        tileData = {'image':        self.byteArray,     # Изображение в виде массива байтов
                    'x': 			self.x(),           # Координата Х
				    'y': 			self.y(),           # Координата У
				    'z': 			self.zValue(),      # Координата Z
                    'passability': 	self.passability,   # Значение проходимости
				    'stripIndex': 	self.stripIndex}    # Индекс в полосе
        return tileData	# Возвращаем полученный словарь
    def duplicate(self, x = None, y = None, z = None, passability = None, stripIndex = None):
        # Метод возвращает копию текущего тайла
        an = self.byteArray[:]
        xn = x if x != None else self.x()
        yn = y if y != None else self.y()
        zn = z if z != None else self.zValue()
        pn = passability if passability != None else self.passability
        sn = stripIndex if stripIndex != None else self.stripIndex
        return Tile(an, xn, yn, zn, pn, sn) # Возвращаем получившийся тайл
    @classmethod
    def fromTileData(cls, tileData):
        # Метод класса конструирует тайл на основе zip-данных
        # Разбираем словарь tileData
        i = tileData['image'][:]
        x = tileData['x']
        y = tileData['y']
        z = tileData['z']
        p = tileData['passability']
        s = tileData['stripIndex']
        return cls(i, x, y, z, p, s)  # Возвращаем получившийся тайл
    def __eq__(self, other):
        # Переопределяем метод сравнения. Два тайла считаются равными, если совпадает их изображение (массив байтов),
        # независимо от координат, высоты и проходимости
        if self.byteArray == other.byteArray: return True
        else: return False