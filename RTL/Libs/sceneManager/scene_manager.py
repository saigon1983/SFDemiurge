'''
В этом модуле описан менеджер сцены - виджет, позволяющий выполнять все операции по редактированию сцены
'''
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class SceneManager(QGraphicsView):
	def __init__(self, main):
		self.mainWindow = main				# Ссылка на главное окно
		super().__init__(self.mainWindow)	# Инициализируем суперкласс
		self.setup()						# Запускаем настройку виджета
#==========Методы установки и настройки начального состояния==========
	def setup(self):
		# Метод настройки виджета
		self.basicTilseSize = int(self.mainWindow.CONFIG['EDITOR OPTIONS']['Tilesize'])	    # Базовый размер тайла
		self.setMinimumSize((self.basicTilseSize + 1) * 20, self.basicTilseSize * 20 + 5)	# Минимальный размер
		self.PROXY = self.mainWindow.PROXY					# Ссылка на прокси-буфер
		self.setMouseTracking(True)							# Виджет отслеживает положение мыши
		self.setDragMode(QGraphicsView.RubberBandDrag) 		# Вариант реакции на нажатие мыши
		self.setAlignment(Qt.AlignLeft | Qt.AlignTop)       # Точка (0, 0) сцены всегда отображается в левом верхнем углу
		self.setTransformationAnchor(QGraphicsView.NoAnchor)# Точка (0, 0) сцены всегда отображается в левом верхнем углу
		self.scaleChange()     								# Устанавливаем двойной зум по умолчанию
	def refresh(self):
		# Метод обновления виджета
		self.update()
	def scaleChange(self):
		# Метод смены масштабирования
		delta = [0.25, 0.5, 1, 2, 4][self.PROXY.SCALE] 				# Выбираем масштаб в зависимости от положения ползунка масштабирования
		self.setTransform(QTransform(QMatrix(delta,0,0,delta,0,0))) # Устанавливаем масштаб