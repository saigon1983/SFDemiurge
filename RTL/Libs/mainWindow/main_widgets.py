'''
В этом модуле описаны три вспомогательных виджета главного окна: панель меню, панель
инструментов и строка состояния
'''
from PyQt4.QtGui import *

class MenuBar(QMenuBar):
	# Класс, определяющий виджет главного меню приложения
	def __init__(self, main):
		self.mainWindow = main				# Сохраняем ссылку на главное окно приложения
		super().__init__(self.mainWindow)	# Инициализируем суперкласс
		self.mainWindow.setMenuBar(self)	# Устанавливаем меню в окно
		
class MainMenu(QMenu):
	# Класс, определяющий верхний уровень меню приложения
	def __init__(self, name, menuBar):
		super().__init__(name, menuBar)
		
class ToolBar(QToolBar):
	# Класс, определяющий виджет панели инструментов
	def __init__(self, main):
		self.mainWindow = main						# Сохраняем ссылку на главное окно приложения
		self.name = 'Панель инструментов'			# Задаем название виджета
		super().__init__(self.name, self.mainWindow)# Инициализируем суперкласс
		self.mainWindow.addToolBar(self)			# Устанавливаем панель в окно
		
class StatusBar(QStatusBar):
	# Класс, определяющий виджет строки состояния
	def __init__(self, main):
		self.mainWindow = main				# Сохраняем ссылку на главное окно приложения
		super().__init__(self.mainWindow)	# Инициализируем суперкласс
		self.mainWindow.setStatusBar(self)	# Устанавливаем меню в окно