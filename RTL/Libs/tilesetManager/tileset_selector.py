'''
В модуле описывается виджет выбора текущего тайлсета
'''
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from RTL.Libs.tilesetManager.tileset_data import TilesetData

class TilesetSelector(QComboBox):
	def __init__(self, main):
		self.mainWindow = main				# Ссылка на главное окно
		super().__init__(self.mainWindow)	# Конструктор суперкласса
		self.initData()						# Создаем базу данных доступных тайлсетов
		self.setup()						# Запускаем настройку виджета
	def setup(self):
		# Метод настройки виджета
		self.setFixedHeight(int(self.mainWindow.CONFIG['EDITOR OPTIONS']['Tilesize']) * 2 + 4)	# Фиксируем высоту виджета
		self.setEditable(True)								# Делаем виджет редактируемым
		self.lineEdit().setReadOnly(True)					# Запрещаем ручное изменение элементов
		self.lineEdit().setFont(QFont('times', 18, 87))		# Настраиваем шрифт
		self.lineEdit().setAlignment(Qt.AlignCenter)		# Выравниваем название тайлсета по центру виджета
		self.currentIndexChanged.connect(self.setTileset)	# Настраиваем реакцию на выбор нового тайлсета из списка
	def initData(self):
		# Метод инициализации данных о тайлсетах
		self.tilesetData = TilesetData()
		for name in self.tilesetData.DATA:	self.addItem(name)	# Загуржаем список оступных тайлсетов в виджет
	def setTileset(self):
		# Метод установки активного тайлсета
		selectedTilesetData = self.tilesetData.DATA[self.tilesetData.NAMES[self.currentIndex()]]
		self.mainWindow.TILESET_MANAGER.setTileset(selectedTilesetData)