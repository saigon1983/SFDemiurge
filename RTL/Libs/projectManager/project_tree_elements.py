'''
В этом модуле описываются элементы дерева структуры проекта - объекты подклассы QStandardItem, необходимые для отражения
структуры проекта в виде дерева в виджете PROJECT_MANAGER
'''
from PyQt4.QtGui import *

class RootElement(QStandardItem):
    # Класс корня структуры. Он же предок для всех элементов-узлов структуры
    objectCounter = 0   # Счетчик всех элементов
    groupsCounter = 0   # Счетчик групп
    scenesCounter = 0   # Счетчик сцен
    usedGroupNames = [] # Список использованных имен групп
    usedSceneNames = [] # Список использованных имен сцен
    def __init__(self, selectorWindow, element):
        '''
        Конструктор принимает следующие входящие элементы:
            main            - ссылка на главное окно
            selectorWindow  - ссылка на окно-родитель объекта
            element         - элемент структуры проекта
        '''
        self.mainWindow = selectorWindow.mainWindow # Ссылка на главное окно
        self.selectorWindow = selectorWindow        # Ссылка на виджет QTreeView
        super().__init__(element.name)              # Конструктор супрекласса
        self.element = element                      # Связь с элементом структуры проекта
        self.setup()                                # Запускаем настройку экземпляра
        self.setPopupMenu()                         # Запускаем настройки всплывающего меню
    def setup(self):
        # Метод настройки экземпляра
        self.name   = self.element.name     # Имя элемента
        self.tag    = self.element.tag      # Имя тега (тип элемента)
        self.ID     = self.element.elemID   # Порядковый номер элемента
        RootElement.objectCounter += 1      # Увеличиваем счетчик элементов на 1
        self.listOfGroups = []              # Список для зависимых групп
        self.listOfScenes = []              # Список для зависимых сцен
        # Далее происходит рекурсивный обход структуры проекта и создание соответствующих элементов дерева для каждого
        # элемента структуры
        if self.tag != 'Scene element':     # Для всех элементов, не являющихся сценой
            i = 0   # Номер строки в дереве для вложенного элемента
            for group in self.element.GROUPS:   # Перебираем все вложенные группы
                newGroup = GroupElement(self.selectorWindow, group) # Создаем новый элемент группы
                self.listOfGroups.append(newGroup)                  # Добавляем группу в список зависимых групп
                self.setChild(i, 0, newGroup)                       # Создаем потомка текущему элементу
                i += 1                                              # Увеличиваем номер строки на 1
            for scene in self.element.SCENES:   # Перебираем все вложенные сцены
                newScene = SceneElement(self.selectorWindow, scene) # Создаем новый элемент сцены
                self.listOfScenes.append(newScene)                  # Добавляем сцену в список зависимых сцен
                self.setChild(i, 0, newScene)                       # Создаем потомка текущему элементу
                i += 1                                              # Увеличиваем номер строки на 1
        # Задем иконку для узла в зависимости от его типа
        print(self.tag)
        self.setIcon(QIcon(QPixmap(r"RTL\Images\Icons\{}Icon.png".format(self.tag.split()[0].lower()))))
    def setPopupMenu(self):
        # Метод настройки всплывающего меню
        pass
    def popupMenu(self, position):
        # Метод вызова всплывающего меню
        pass

class GroupElement(RootElement):
    '''
    Подкласс, отвечающий за элемент группы. По сути мало чем отличается от родителя, за исключением всплывающего меню
    '''
    def __init__(self, selectorWindow, element):
        RootElement.groupsCounter += 1              # Увеличиваем счетчик групп на 1
        super().__init__(selectorWindow, element)   # Вызываем конструктор суперкласса
        RootElement.usedGroupNames.append(self.name)# Помещаем имя группы в список уже использованных имен групп
    def setPopupMenu(self):
        # Перегружаем метод вызова контекстного меню
        pass

class SceneElement(RootElement):
    '''
    Подкласс, отвечающий за элемент сцены. Связывает между собой графическое представление сцены и элемент сцены в
    структуре проекта. Обеспечивает интерфейс настройки и редактирования основных параметров сцены
    '''
    def __init__(self, selectorWindow, element):
        RootElement.scenesCounter += 1              # Увеличиваем счетчик сцен на 1
        super().__init__(selectorWindow, element)   # Вызываем конструктор суперкласса
        RootElement.usedSceneNames.append(self.name)# Помещаем имя сцены в список уже использованных имен сцен
    def setPopupMenu(self):
        # Перегружаем метод вызова контекстного меню
        pass
    def setSceneToEditor(self):
        # Метод загрузки сцены в редактор
        pass