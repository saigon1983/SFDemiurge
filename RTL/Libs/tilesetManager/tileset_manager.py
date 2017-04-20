'''
В этом модуле описывается класс TilesetManager - виджет для работы с представлением тайлсета. Он позволяет переключаться
между различными зонами тайлсета, выбирать активный тайл, менять тайлсет и просматривать текущее изображение в отдельном
виджете.
По сути, менеджер состоит из четырех виджетов:
	TilesetManager 	- подкласс виджета QTabWidget, от которого потомку необходимо перенять возможность переключаться между
	вкладками, каждая из которых содержит виджет...
	TilesetViewer 	- подкласс QGraphicsView. Этот виджет является объектом доступа к текущей графической сцене, которая и
	отражает часть тайлсета.
	TilesetSelector - потомок QComboBox. Этот виджет позволяет выбрать текущий тайлсет из списка доступных
	TileViewer 		- потомок QLabel. Необходим для просмотра текущего активного тайла в отдельном окне
'''
from PyQt4.QtGui import *
from RTL.Libs.tilesetManager.tileset_viewer import *

class TilesetManager(QTabWidget):
	TABNAMES = ['A','B','C','D','E','F']	# Стандартные имена вкладок TODO: сменить на нормальные
	def __init__(self, main):
		'''
		Конструктор (на данном этапе) принимает следующие аргументы:
			main - ссылка на главное окно
		'''
		self.mainWindow	= main				# Ссылка на главное окно
		super().__init__(self.mainWindow)	# Инициализируем суперкласс
		self.setup()						# Запускаем метод настройки виджета
		self.setTileset()					# Устанавливаем тайлсет по умолчанию
		self.views[0].setActiveTile()		# Делаем активный первый тайл первого вида
	def setup(self):
		# Метод настройки виджета
		self.setTabPosition(1)		# Положение закладок - снизу
		self.setFixedSize(300, 600)	# Фиксируем размеры виджета
	def setTileset(self, tilesetData = {}):
		# Метод установки активного тайлсета
		index = self.currentIndex()	# Запоминаем индекс текущей активной вкладки
		self.clear()				# Очищаем виджет
		self.views = sliceFromImage(self.mainWindow, tilesetData)	# Получаем отображения тайлсета методом нарезки
		for view in self.views:	
			# Добавляем вкладки к виджету для каждой нарезки
			self.addTab(view, TilesetManager.TABNAMES[self.views.index(view)])
		self.setCurrentIndex(index)	# Делаем активной ту же вкладку, что была активной до смены тайлсета
		print('Tileset changed!')
	def refresh(self):
		# Метод обновления виджета
		self.update()