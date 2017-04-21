'''
В этом модуле описываются элементы дерева структуры проекта - объекты подклассы QStandardItem, необходимые для отражения
структуры проекта в виде дерева в виджете PROJECT_MANAGER
'''
from RTL.Libs.projectManager.project_element_menu import *
from RTL.Libs.projectClass.project_structure import *

class RootElement(QStandardItem):
    # Класс корня структуры. Он же предок для всех элементов-узлов структуры
    def __init__(self, selectorWindow, element, root = None):
        '''
        Конструктор принимает следующие входящие элементы:
            selectorWindow  - ссылка на окно-родитель объекта
            element         - элемент структуры проекта
            root            - ссылка на корневой элемент
        '''
        self.mainWindow = selectorWindow.mainWindow # Ссылка на главное окно
        self.selectorWindow = selectorWindow        # Ссылка на виджет QTreeView
        super().__init__(element.name)              # Конструктор супрекласса
        self.element = element                      # Связь с элементом структуры проекта
        self.setup(root)                            # Запускаем настройку экземпляра
        self.setPopupMenu()                         # Запускаем настройки всплывающего меню
    def setup(self, root):
        # Метод настройки экземпляра
        self.name   = self.element.name     # Имя элемента
        self.tag    = self.element.tag      # Имя тега (тип элемента)
        if self.tag == 'Root element':
            self.initRoot()                 # Обнуляем счетчики, если инициализируется корень структуры
        if not root:    self.root = self    # Корнем корня является сам корень))
        else:           self.root = root    # Остальным элементам передается ссылка на корневой элемент
        self.ID     = self.element.elemID   # Порядковый номер элемента
        self.root.objectCounter += 1        # Увеличиваем счетчик элементов на 1
        self.listOfGroups = []              # Список для зависимых групп
        self.listOfScenes = []              # Список для зависимых сцен
        # Далее происходит рекурсивный обход структуры проекта и создание соответствующих элементов дерева для каждого
        # элемента структуры
        if self.tag != 'Scene element':     # Для всех элементов, не являющихся сценой
            i = 0   # Номер строки в дереве для вложенного элемента
            for group in self.element.GROUPS:   # Перебираем все вложенные группы
                newGroup = GroupElement(self.selectorWindow, group, self.root)  # Создаем новый элемент группы
                self.listOfGroups.append(newGroup)                              # Добавляем группу в список зависимых групп
                self.setChild(i, 0, newGroup)                                   # Создаем потомка текущему элементу
                i += 1                                                          # Увеличиваем номер строки на 1
            for scene in self.element.SCENES:   # Перебираем все вложенные сцены
                newScene = SceneElement(self.selectorWindow, scene, self.root)  # Создаем новый элемент сцены
                self.listOfScenes.append(newScene)                              # Добавляем сцену в список зависимых сцен
                self.setChild(i, 0, newScene)                                   # Создаем потомка текущему элементу
                i += 1                                                          # Увеличиваем номер строки на 1
        # Задем иконку для узла в зависимости от его типа
        self.setIcon(QIcon(QPixmap(r"RTL\Images\Icons\{}Icon.png".format(self.tag.split()[0].lower()))))
    def initRoot(self):
        # Метод инициализации корня структуры. Необходим в первую очередь для обнуления счетчиков
        self.objectCounter = 0   # Счетчик всех элементов
        self.groupsCounter = 0   # Счетчик групп
        self.scenesCounter = 0   # Счетчик сцен
        self.usedGroupNames = [] # Список использованных имен групп
        self.usedSceneNames = [] # Список использованных имен сцен
    def setPopupMenu(self):
        # Метод настройки всплывающего меню
        self.popupMenu = PMRootMenu(self)
    def callPopupMenu(self, position):
        # Метод вызова всплывающего меню
        self.popupMenu.move(self.selectorWindow.viewport().mapToGlobal(position))
        self.popupMenu.show()
    def addNewGroup(self, groupName):
        # Метод добавления новой группы
        newGroupStructure   = ProjectGroupElement(groupName, self.element)                      # Новый элемент структуры
        newGroupElement     = GroupElement(self.selectorWindow, newGroupStructure, self.root)   # Новый элемент дерева
        self.insertRow(len(self.listOfGroups), newGroupElement)                                 # Добавляем элемент в отображение
        self.mainWindow.PROJECT.changed()                                                       # Сообщаем проекту, что он изменен
    def addNewScene(self, sceneData):
        # Метод добавления новой сцены в проект
        newSceneSctructure  = ProjectSceneElement(sceneData['Name'], self.element, sceneData)   # Новый элемент структуры
        newSceneElement     = SceneElement(self.selectorWindow, newSceneSctructure, self.root)  # Новый элемент дерева
        self.insertRow(self.rowCount(), newSceneElement)	                                    # Добавляем элемент в отображение
        self.mainWindow.PROJECT.changed()                                                       # Сообщаем проекту, что он изменен

class GroupElement(RootElement):
    '''
    Подкласс, отвечающий за элемент группы. По сути мало чем отличается от родителя, за исключением всплывающего меню
    '''
    def __init__(self, selectorWindow, element, root):
        super().__init__(selectorWindow, element, root) # Вызываем конструктор суперкласса
        self.root.groupsCounter += 1                    # Увеличиваем счетчик групп на 1
        self.root.usedGroupNames.append(self.name)      # Помещаем имя группы в список уже использованных имен групп
    def setPopupMenu(self):
        # Перегружаем метод вызова контекстного меню
        self.popupMenu = PMGroupMenu(self)

class SceneElement(RootElement):
    '''
    Подкласс, отвечающий за элемент сцены. Связывает между собой графическое представление сцены и элемент сцены в
    структуре проекта. Обеспечивает интерфейс настройки и редактирования основных параметров сцены
    '''
    def __init__(self, selectorWindow, element, root):
        super().__init__(selectorWindow, element, root) # Вызываем конструктор суперкласса
        self.root.scenesCounter += 1                    # Увеличиваем счетчик сцен на 1
        self.root.usedSceneNames.append(self.name)      # Помещаем имя сцены в список уже использованных имен сцен
    def setPopupMenu(self):
        # Перегружаем метод вызова контекстного меню
        self.popupMenu = PMSceneMenu(self)
    def setSceneToEditor(self):
        # Метод загрузки сцены в редактор
        pass
