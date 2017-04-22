'''
В этом модуле описываются элементы дерева структуры проекта - объекты подклассы QStandardItem, необходимые для отражения
структуры проекта в виде дерева в виджете PROJECT_MANAGER
'''
from RTL.Libs.sceneManager.scene_model import SceneModel
from RTL.Libs.projectManager.project_element_menu import *
from RTL.Libs.projectClass.project_structure import *
class RootElement(QStandardItem):

    def __init__(self, selectorWindow, element, rootItem = None, parentItem = None):
        '''
        Конструктор принимает следующие входящие элементы:
            selectorWindow  - ссылка на окно-родитель объекта
            element         - элемент структуры проекта
            rootItem        - ссылка на корневой элемент
            parentItem      - ссылка на объект-родитель
        '''
        self.mainWindow = selectorWindow.mainWindow
        self.selectorWindow = selectorWindow
        self.element = element
        super().__init__(self.element.name)
        self.setPopupMenu()
        self.setup(rootItem, parentItem)
    def setPopupMenu(self):
        # Метод настройки всплывающего меню
        self.popupMenu = PMRootMenu(self)
    def callPopupMenu(self, position):
        # Метод вызова всплывающего меню
        self.popupMenu.move(self.selectorWindow.viewport().mapToGlobal(position))
        self.popupMenu.show()
    def setup(self, rootItem, parentItem):
        self.name = self.element.name
        self.tag  = self.element.tag
        if not rootItem:
            self.rootItem = self
            self.initRoot()
        else:
            self.rootItem = rootItem
        self.ID = self.element.elemID
        self.rootItem.objectCounter += 1
        self.listOfGroups = []              # Список для зависимых групп
        self.listOfScenes = []              # Список для зависимых сцен
        if self.tag != 'Scene element':
            i = 0
            for group in self.element.GROUPS:
                newGroup = GroupElement(self.selectorWindow, group, self.rootItem, self)
                self.setChild(i, 0, newGroup)
                i += 1
            for scene in self.element.SCENES:
                newScene = SceneElement(self.selectorWindow, scene, self.rootItem, self)
                self.setChild(i, 0, newScene)
                i += 1
        # Задем иконку для узла в зависимости от его типа
        self.setIcon(QIcon(QPixmap(r"RTL\Images\Icons\{}Icon.png".format(self.tag.split()[0].lower()))))
    def initRoot(self):
        # Метод инициализации корня структуры. Необходим в первую очередь для обнуления счетчиков
        self.objectCounter = 0   # Счетчик всех элементов
        self.groupsCounter = 0   # Счетчик групп
        self.scenesCounter = 0   # Счетчик сцен
        self.usedGroupNames = [] # Список использованных имен групп
        self.usedSceneNames = [] # Список использованных имен сцен
    def addNewGroup(self, groupName):
        newGroupStructElement = ProjectGroupElement(groupName, self.element, self.element.root)
        newGroupElement = GroupElement(self.selectorWindow, newGroupStructElement, self.rootItem, self)
        self.insertRow(len(self.listOfGroups), newGroupElement)
        self.mainWindow.PROJECT.changed()
    def addNewScene(self, sceneData):
        newSceneStructElement = ProjectSceneElement(sceneData['Name'], self.element, self.element.root, sceneData)
        newSceneElement = SceneElement(self.selectorWindow, newSceneStructElement, self.rootItem, self)
        self.insertRow(self.rowCount(), newSceneElement)	 # Добавляем элемент в отображение
        self.mainWindow.PROJECT.changed()
    def compile(self):
        # Метод обходит все элемнты, координирует их данные с данными узлов структуры и сохраняет сцены в файлы
        for group in self.listOfGroups:
            group.compile()
        for scene in self.listOfScenes:
            scene.save()

class GroupElement(RootElement):
    def __init__(self, selectorWindow, element, rootItem, parentItem):
        super().__init__(selectorWindow, element, rootItem, parentItem) # Вызываем конструктор суперкласса
    def setup(self, rootItem, parentItem):
        super().setup(rootItem, parentItem)
        self.rootItem.groupsCounter += 1
        self.rootItem.usedGroupNames.append(self.name)
        self.parentItem = parentItem
        self.parentItem.listOfGroups.append(self)
    def setPopupMenu(self):
        # Перегружаем метод вызова контекстного меню
        self.popupMenu = PMGroupMenu(self)

class SceneElement(RootElement):
    def __init__(self, selectorWindow, element, rootItem, parentItem):
        super().__init__(selectorWindow, element, rootItem, parentItem) # Вызываем конструктор суперкласса
    def setup(self, rootItem, parentItem):
        super().setup(rootItem, parentItem)
        self.rootItem.scenesCounter += 1
        self.rootItem.usedSceneNames.append(self.name)
        self.parentItem = parentItem
        self.parentItem.listOfScenes.append(self)
        self.sceneModel = SceneModel(self.mainWindow, self.element.sceneData)
    def setPopupMenu(self):
        # Перегружаем метод вызова контекстного меню
        self.popupMenu = PMSceneMenu(self)
    def setSceneToEditor(self):
        # Метод загрузки сцены в редактор
        self.mainWindow.SCENE_MANAGER.setScene(self.sceneModel) # Загружаем сцену в виджет
        self.mainWindow.SCENE_MANAGER.refresh()                 # Обновляем редактор
    def save(self):
        print('Scene {} saved!'.format(self.sceneModel.IDstr))

'''
class RootElement(QStandardItem):
    # Класс корня структуры. Он же предок для всех элементов-узлов структуры
    def __init__(self, selectorWindow, element, root = None, parent = None):

        Конструктор принимает следующие входящие элементы:
            selectorWindow  - ссылка на окно-родитель объекта
            element         - элемент структуры проекта
            root            - ссылка на корневой элемент

        self.mainWindow = selectorWindow.mainWindow # Ссылка на главное окно
        self.selectorWindow = selectorWindow        # Ссылка на виджет QTreeView
        super().__init__(element.name)              # Конструктор супрекласса
        self.element = element                      # Связь с элементом структуры проекта
        self.setup(root, parent)                    # Запускаем настройку экземпляра
        self.setPopupMenu()                         # Запускаем настройки всплывающего меню
    def setup(self, root, parent):
        # Метод настройки экземпляра
        self.name   = self.element.name     # Имя элемента
        self.tag    = self.element.tag      # Имя тега (тип элемента)
        if self.tag == 'Root element':
            self.initRoot()                 # Обнуляем счетчики, если инициализируется корень структуры
        if not root:    self.root = self    # Корнем корня является сам корень))
        else:           self.root = root    # Остальным элементам передается ссылка на корневой элемент
        if not parent: self.parent = self
        else:          self.parent = parent
        self.ID     = self.element.elemID   # Порядковый номер элемента
        self.root.objectCounter += 1        # Увеличиваем счетчик элементов на 1
        self.listOfGroups = []              # Список для зависимых групп
        self.listOfScenes = []              # Список для зависимых сцен
        # Далее происходит рекурсивный обход структуры проекта и создание соответствующих элементов дерева для каждого
        # элемента структуры
        if self.tag != 'Scene element':     # Для всех элементов, не являющихся сценой
            i = 0   # Номер строки в дереве для вложенного элемента
            for group in self.element.GROUPS:   # Перебираем все вложенные группы
                newGroup = GroupElement(self.selectorWindow, group, self.root, self)  # Создаем новый элемент группы
                self.listOfGroups.append(newGroup)                              # Добавляем группу в список зависимых групп
                self.setChild(i, 0, newGroup)                                   # Создаем потомка текущему элементу
                i += 1                                                          # Увеличиваем номер строки на 1
            for scene in self.element.SCENES:   # Перебираем все вложенные сцены
                newScene = SceneElement(self.selectorWindow, scene, self.root, self)  # Создаем новый элемент сцены
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
        newGroupStructure   = ProjectGroupElement(groupName, self.element, self.element.root)   # Новый элемент структуры
        newGroupElement     = GroupElement(self.selectorWindow, newGroupStructure, self.root, self)   # Новый элемент дерева
        self.insertRow(len(self.listOfGroups), newGroupElement)                                 # Добавляем элемент в отображение
        self.mainWindow.PROJECT.changed()                                                       # Сообщаем проекту, что он изменен
    def addNewScene(self, sceneData):
        # Метод добавления новой сцены в проект
        newSceneSctructure  = ProjectSceneElement(sceneData['Name'], self.element, self.element.root, sceneData)   # Новый элемент структуры
        newSceneElement     = SceneElement(self.selectorWindow, newSceneSctructure, self.root, self)  # Новый элемент дерева
        self.insertRow(self.rowCount(), newSceneElement)	                                    # Добавляем элемент в отображение
        self.mainWindow.PROJECT.changed()                                                       # Сообщаем проекту, что он изменен
    def compile(self):
        # Метод обходит все элемнты, координирует их данные с данными узлов структуры и сохраняет сцены в файлы
        for group in self.listOfGroups:
            group.compile()
        for scene in self.listOfScenes:
            scene.save()

class GroupElement(RootElement):

    Подкласс, отвечающий за элемент группы. По сути мало чем отличается от родителя, за исключением всплывающего меню

    def __init__(self, selectorWindow, element, root, parent):
        super().__init__(selectorWindow, element, root, parent) # Вызываем конструктор суперкласса
        self.root.groupsCounter += 1                    # Увеличиваем счетчик групп на 1
        self.root.usedGroupNames.append(self.name)      # Помещаем имя группы в список уже использованных имен групп
        self.parent.listOfGroups.append(self)
    def setPopupMenu(self):
        # Перегружаем метод вызова контекстного меню
        self.popupMenu = PMGroupMenu(self)

class SceneElement(RootElement):

    Подкласс, отвечающий за элемент сцены. Связывает между собой графическое представление сцены и элемент сцены в
    структуре проекта. Обеспечивает интерфейс настройки и редактирования основных параметров сцены

    def __init__(self, selectorWindow, element, root, parent):
        super().__init__(selectorWindow, element, root, parent) # Вызываем конструктор суперкласса
        self.root.scenesCounter += 1                    # Увеличиваем счетчик сцен на 1
        self.root.usedSceneNames.append(self.name)      # Помещаем имя сцены в список уже использованных имен сцен
        self.sceneModel = SceneModel(self.mainWindow, self.element.sceneData)
        self.parent.listOfScenes.append(self)
    def setPopupMenu(self):
        # Перегружаем метод вызова контекстного меню
        self.popupMenu = PMSceneMenu(self)
    def setSceneToEditor(self):
        # Метод загрузки сцены в редактор
        self.mainWindow.SCENE_MANAGER.setScene(self.sceneModel) # Загружаем сцену в виджет
        self.mainWindow.SCENE_MANAGER.refresh()                 # Обновляем редактор
    def save(self):
        print('Scene {} saved!'.format(self.sceneModel.IDstr))
'''