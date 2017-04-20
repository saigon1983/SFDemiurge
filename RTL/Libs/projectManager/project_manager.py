'''
Модуль с описанием виджета выбора (и создания) сцен. Представляет из себя виджет QTreeView, настроенный на работу с
структурой проекта. Позволяет создавать новые сцены, распределять их по группам и открывать их для редактирования
'''
from PyQt4.QtCore import *
from RTL.Libs.projectManager.project_tree_elements import *

class ProjectManager(QTreeView):
    def __init__(self, main):
        self.mainWindow =main				# Ссылка на главное окно
        super().__init__(self.mainWindow)	# Инициализируем суперкласс
        self.setup()						# Настройка виджета
        self.initProject()                  # Инициализируем проект
    def setup(self):
        # Метод настройки виджета
        self.setFixedWidth(300)									# Фиксируем ширину виджета
        self.setMinimumHeight(110)								# Устанавливаем минимальную высоту виджета
        self.setHeaderHidden(True)								# Скрываем заголовки
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)	# Запрещаем редактирование названий элементов
        self.setModel(QStandardItemModel(self))                 # Устанавливаем модель
        self.setContextMenuPolicy(Qt.CustomContextMenu)         # Устанавливаем политику вызова контекстного меню
        self.customContextMenuRequested.connect(self.popupMenu) # Перенаправляем вызов меню в собственный метод
        self.doubleClicked.connect(self.doubleClick)            # Соединяем сигнал двойного щелчка мыши с командой
    def initProject(self):
        # Метод загрузки данных о новом проекте и инициализации дерева проекта
        self.model().clear()                                    # Очищает текущую модель
        self.PROJECT = self.mainWindow.PROJECT                  # Ссылка на текущий проект
        self.structure = self.PROJECT.tree                      # Ссылка на структуры проекта
        self.projectRoot = RootElement(self, self.structure)    # Оформляем корень дерева
        self.model().appendRow(self.projectRoot)                # Добавляем все ряды в виджет
        self.expandAll()                                        # Раскрываем все узлы
    def popupMenu(self, position):
        # Метод вызова контекстного меню текущего выбранного элемента. Аргумент местоположения курсора position
        # передается автоматически из сигнала customContextMenuRequested
        if self.selectedIndexes():
            item = self.selectedIndexes()[0]            # Берем первый индекс из списка выделенных элементов
            element = item.model().itemFromIndex(item)  # Получаем активный элемент
            element.popupMenu(position)                 # Вызываем меню этого элемента
    def doubleClick(self, index):
        # Метод реакции на войной щелчок мышью. Для элементов сцены - открывает сцену в редакторе, для остальных -
        # сворачивает/разворачивает ветку
        pass