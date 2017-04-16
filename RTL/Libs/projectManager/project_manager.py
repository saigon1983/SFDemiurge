'''
Модуль с описанием виджета выбора (и создания) сцен. Представляет из себя виджет QTreeView, настроенный на работу с
структурой проекта. Позволяет создавать новые сцены, распределять их по группам и открывать их для редактирвоания
'''
from PyQt4.QtGui import *

class ProjectManager(QTreeView):
	def __init__(self, main):
		self.mainWindow =main					# Ссылка на главное окно
		super().__init__(self.mainWindow)	# Инициализируем суперкласс
		self.setup()									# Настройка виджета
	def setup(self):
		# Метод настрйоки виджета
		self.setFixedWidth(300)													# Фиксируем ширину виджета
		self.setMinimumHeight(110)											# Устанавливаем минимальную высоту виджета
		self.setHeaderHidden(True)											# Скрываем заголовки
		self.setEditTriggers(QAbstractItemView.NoEditTriggers)	# Запрещаем редактирование названий элементов