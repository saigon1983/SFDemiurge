'''
В данном модуле описаны меню, вызываемые нажатием правой кнопки мыши на элементах виджета QTreeView
'''

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from RTL.Libs.projectManager.project_menu_actions import *

class PMMenu(QMenu):
    # Абстрактный класс, являющийся предком всех специальных контекстных меню
    def __init__(self, callingItem):
        self.callingItem = callingItem                      # Ссылка на элемент, вызывающий меню
        self.selectorWindow = callingItem.selectorWindow    # Ссылка на виджет менеджера проекта
        super().__init__(self.selectorWindow)               # Инициализируем суперкласс
        self.setup()                                        # Запускаем настройку меню
    def setup(self):
        # Метод настройки меню. Для полноценной функциональности должен быть переопределен в потомке со ссылкой на себя
        self.setWindowFlags(Qt.Popup)   # Сообщаем программе, что окно меню не должно содержать рамок
        self.move(0, 0)                 # Определяем предварительные координаты окна меню

class PMRootMenu(PMMenu):
    # Контекстное меню корневого элемента
    def __init__(self, callingItem):
        super().__init__(callingItem)   # Вызываем конструктор суперкласса
    def setup(self):
        # Переопределнный метод настройки контента меню
        super().setup()
        self.addAction(PMAction_AddGroup(self)) # Добавить группу
        self.addAction(PMAction_AddScene(self)) # Добавить группу

class PMGroupMenu(PMMenu):
    # Контекстное меню элемента группы
    def __init__(self, callingItem):
        super().__init__(callingItem)   # Вызываем конструктор суперкласса
    def setup(self):
        # Переопределнный метод настройки контента меню
        super().setup()
        self.addAction(PMAction_AddGroup(self)) # Добавить группу
        self.addAction(PMAction_AddScene(self)) # Добавить группу

class PMSceneMenu(PMMenu):
    # Контекстное меню элемента сцены
    def __init__(self, callingItem):
        super().__init__(callingItem)   # Вызываем конструктор суперкласса
    def setup(self):
        # Переопределнный метод настройки контента меню
        super().setup()
        # TODO: Реализовать список опций