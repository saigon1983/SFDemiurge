'''
Класс ProjectCreator является простым диалоговым окном создания нового проекта. В поле ввода ожидается
название нового проекта. Подтверждение создания возможно только в случае, если имя проекта состоит из
латинских или русских букв или цифр. Возможны элементы подчеркивания.
'''
import re, os, sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class ProjectCreator(QDialog):
	def __init__(self, projectsFolderPath):
		'''
		Конструктор класса принимает один аргумент:
			projectsFolderPath - путь к каталогу с проектами
		'''
		# Создаем список существующих проектов
		self.existingProjects 	= os.listdir(projectsFolderPath)
		super().__init__()		# Инициализируем суперкласс
		self.setup()				# Настраиваем окно
		self.setButtons()		# Настраиваем кнопки
		self.setWidgets()		# Настраиваем виджеты
		self.setLayouts()		# Настраиваем размещение компоенентов
		self.validateInputs()	# Проверяем валидность текущего значения
		self.exec()				# Запускаем обработку
#========== Методы настройки экземпляра ==========
	def setup(self):
		# Настраиваем параметры виджета
		self.setWindowTitle('Создание нового проекта')	# Заголовок
		self.setFixedSize(300,100)									# Фиксированный размер
	def setButtons(self):
		# Настройка стандартных кнопок подтверждения/отмены
		self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
		self.buttons.accepted.connect(self.accept)
		self.buttons.rejected.connect(self.reject)
	def setWidgets(self):
		# Настройка элементов окна
		# Простые метки с текстом
		self.label1 = QLabel('Имя каталога:')
		self.label1.setFixedWidth(75)
		self.label1.setToolTip('Укажите имя для каталога. Имя не должно содержать символы "|", "/", "*", "<", ">", "?", ":"')
		self.label1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
		self.label2 = QLabel('Имя проекта:')
		self.label2.setFixedWidth(75)
		self.label2.setToolTip('Укажите имя Вашего проекта. По умолчанию назначается имя каталога')
		self.label2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
		# Поле ввода названия папки проекта
		self.nameField = QLineEdit()
		self.nameField.setFixedWidth(200)
		self.nameField.textChanged.connect(self.validateInputs)		# Соединяем сигнал с проверкой правильности имени
		# Поле ввода названия папки проекта
		self.folderField = QLineEdit()
		self.folderField.setFixedWidth(200)
		self.folderField.textChanged.connect(self.validateInputs)		# Соединяем сигнал с проверкой правильности имени
		self.folderField.textChanged.connect(self.nameField.setText)	# Соединяем сигнал с проверкой правильности имени
	def setLayouts(self):
		# Настраиваем компоновщики
		self.vLayout = QVBoxLayout(self)				# Основной вертикальный
		self.hLayout1 = QHBoxLayout()					# Первый горизонтальный
		self.hLayout1.addWidget(self.label1)			# Добавляем метку
		self.hLayout1.addWidget(self.folderField)		# Добавляем поле
		self.hLayout2 = QHBoxLayout()					# Второй горизонтальный
		self.hLayout2.addWidget(self.label2)			# Добавляем метку
		self.hLayout2.addWidget(self.nameField)		# Добавляем поле
		self.hLayout3 = QHBoxLayout()					# Третий горизонтальный
		self.hLayout3.addStretch(1)						# Добавляем пробел
		self.hLayout3.addWidget(self.buttons)			# Добавляем кнопки
		self.hLayout3.addStretch(1)						# Добавляем пробел
		self.vLayout.addLayout(self.hLayout1)			# Подключаем к основному
		self.vLayout.addLayout(self.hLayout2)			# Подключаем к основному
		self.vLayout.addLayout(self.hLayout3)			# Подключаем к основному
#========== Методы проверок валидности ==========
	def validName(self):
		# Проверка корректности имени проекта. В имени не должно содержаться знаков "|", "/", "*", "<", ">", "?", ":"
		if re.search('[|/*<>?:]', self.folderField.text()): return False
		else: return True
	def noSuchProject(self):
		# Проверка наличия уже существующего каталога с таким же именем
		if self.folderField.text() in self.existingProjects: return False
		else: return True
	def validateInputs(self):
		# Ввод считается правильным, если введена непустая строка без запрещенных символов и каталога с таким именем
		# еще нет в папке проектов
		if self.folderField.text() and self.validName() and self.noSuchProject():	self.buttons.buttons()[0].setDisabled(False)
		else:	self.buttons.buttons()[0].setDisabled(True)
#========== Методы подтверждения выбора ==========
	def accept(self):
		# Метод подтверждения ввода
		folderName = self.folderField.text().replace('\\','')		# Удаляем символы экранирования, если они есть
		if not self.nameField.text():	projectName = folderName	# Если имя проекта не задано, оно станет таким же, как имя папки
		else:	projectName = self.nameField.text()
		self.inputResults = (projectName, folderName)				# Сохраняем имена в кортеже inputResults
		super().accept()