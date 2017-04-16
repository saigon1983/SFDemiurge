'''
В этом модуле описывается класс представления тайлсета, являющийся наследником класса QGraphicsScene
'''
from PyQt4.QtGui import *

class Tileset(QGraphicsScene):
	def __init__(self, main, pixmap):
		super().__init__()				# Инициализируем суперкласс
		self.config(main)	# Запускаем метод установки необходимых атрибутов
		self.setup(pixmap)				# Запускаем метод настройки виджета
	def config(self, main):
		# Метод установки необходимых атрибутов
		self.CONFIG = main.CONFIG	# Ссылка на объект конфигурации
		self.PROXY = main.PROXY		# Ссылка на прокси-буфер
		self.TILESIZE = int(self.CONFIG['EDITOR OPTIONS']['Tilesize'])	# Фиксируем основной размер тайлов
	def setup(self, pixmap):
		# Метод настройки виджета
		item = QGraphicsPixmapItem(pixmap)										# Создаем объект сцены как экземпляр QGraphicsPixmapItem
		item.setShapeMode(QGraphicsPixmapItem.BoundingRectShape)	# Устанавливаем контур сцены
		self.addItem(item)																		# Размещаем тайлсет на сцене в виде самостоятельного объекта