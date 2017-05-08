'''
В этом модуле описывается простой класс отображения текущего виджета в небольшом окне
'''
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class TileViewer(QLabel):
	def __init__(self, main):
		self.mainWindow = main	# Ссылка на главное окно
		QLabel.__init__(self)			# Конструктор суперкласса
		self.setup()						# Запускаем настройку виджета
	def setup(self):
		# Метод настройки виджета
		self.basicTilseSize = int(self.mainWindow.CONFIG['EDITOR OPTIONS']['Tilesize'])	# Базовый размер тайла
		self.setFixedSize(self.basicTilseSize*2+6, self.basicTilseSize*2+4)				# Настраиваем габариты виджета
		self.setFrameStyle(QFrame.Panel | QFrame.Sunken)								# Настраиваем стиль виджета
		self.setMargin(2)																# Задаем отступы по краям
		self.setAlignment(Qt.AlignCenter)												# Центрируем изображение