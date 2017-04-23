'''
В этом модуле описываются элементы дерева структуры проекта - объекты подклассы QStandardItem, необходимые для отражения
структуры проекта в виде дерева в виджете PROJECT_MANAGER
'''
import os
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
        self.mainWindow = selectorWindow.mainWindow # Ссылка на главное окно
        self.selectorWindow = selectorWindow        # Ссылка на виджет QTreeView
        self.element = element                      # Связь с элементом структуры проекта
        super().__init__(self.element.name)         # Конструктор супрекласса
        self.setPopupMenu()                         # Устнавливаем правильное всплывающего меню
        self.setup(rootItem, parentItem)            # Запускаем настройку экземпляра
    def setPopupMenu(self):
        # Метод настройки всплывающего меню
        self.popupMenu = PMRootMenu(self)
    def callPopupMenu(self, position):
        # Метод вызова всплывающего меню
        self.popupMenu.move(self.selectorWindow.viewport().mapToGlobal(position))
        self.popupMenu.show()
    def setup(self, rootItem, parentItem):
        # Метод настройки экземпляра
        self.name = self.element.name   # Имя элемента
        self.tag  = self.element.tag    # Имя тега (тип элемента)
        if not rootItem:
            self.rootItem = self
            self.initRoot()             # Если создается корневой элемент - обнуляем счетчики и ссылаемся на сам корень
        else:
            self.rootItem = rootItem    # В любом бругом случае, фиксируем ссылку на корневой элемент
        self.ID = self.element.elemID   # Порядковый номер элемента
        self.rootItem.objectCounter += 1# Увеличиваем счетчик элементов на 1
        self.listOfGroups = []          # Список для зависимых групп
        self.listOfScenes = []          # Список для зависимых сцен
        if self.tag != 'Scene element':
            # Далее происходит рекурсивный обход структуры проекта и создание соответствующих элементов дерева для каждого
            # элемента структуры
            i = 0
            for group in self.element.GROUPS:   # Перебираем все вложенные группы
                newGroup = GroupElement(self.selectorWindow, group, self.rootItem, self)# Создаем новый элемент группы
                self.setChild(i, 0, newGroup)                                           # Создаем потомка текущему элементу
                i += 1                                                                  # Увеличиваем номер строки на 1
            for scene in self.element.SCENES:   # Перебираем все вложенные сцены
                newScene = SceneElement(self.selectorWindow, scene, self.rootItem, self)# Создаем новый элемент сцены
                self.setChild(i, 0, newScene)                                           # Создаем потомка текущему элементу
                i += 1                                                                  # Увеличиваем номер строки на 1
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
        # Метод добавления новой группы
        newGroupStructElement = ProjectGroupElement(groupName, self.element, self.element.root)         # Новый элемент структуры
        newGroupElement = GroupElement(self.selectorWindow, newGroupStructElement, self.rootItem, self) # Новый элемент дерева
        print(len(self.listOfGroups))
        self.insertRow(len(self.listOfGroups)-1, newGroupElement)                                         # Добавляем элемент в отображение
        self.mainWindow.PROJECT.changed()                                                               # Сообщаем проекту, что он изменен
    def addNewScene(self, sceneData):
        # Метод добавления новой сцены в проект
        newSceneStructElement = ProjectSceneElement(sceneData['Name'], self.element, self.element.root, sceneData)  # Новый элемент структуры
        newSceneElement = SceneElement(self.selectorWindow, newSceneStructElement, self.rootItem, self)             # Новый элемент дерева
        self.insertRow(self.rowCount(), newSceneElement)	                                                        # Добавляем элемент в отображение
        self.mainWindow.PROJECT.changed()                                                                           # Сообщаем проекту, что он изменен
    def compile(self):
        # Метод обходит все элемнты, координирует их данные с данными узлов структуры и сохраняет сцены в файлы
        for group in self.listOfGroups:
            group.compile() # Для групп выполняем рекурсивную компиляци.
        for scene in self.listOfScenes:
            scene.save()    # Для сцен выполняем сохранение в файл

class GroupElement(RootElement):
    # Подкласс, отвечающий за элемент группы. По сути мало чем отличается от родителя, за исключением всплывающего меню
    def __init__(self, selectorWindow, element, rootItem, parentItem):
        super().__init__(selectorWindow, element, rootItem, parentItem) # Вызываем конструктор суперкласса
    def setup(self, rootItem, parentItem):
        # Переопределнный метод настройки экземпляра
        super().setup(rootItem, parentItem)             # Вызывам метод настройки супекласса
        self.rootItem.groupsCounter += 1                # Увеличиваем счетчик групп на 1
        self.rootItem.usedGroupNames.append(self.name)  # Помещаем имя группы в список уже использованных имен групп
        self.parentItem = parentItem                    # Фиксируем родителя
        self.parentItem.listOfGroups.append(self)       # Добавляем экземпляр в список групп родителя
    def setPopupMenu(self):
        # Перегружаем метод вызова контекстного меню
        self.popupMenu = PMGroupMenu(self)

class SceneElement(RootElement):
    # Подкласс, отвечающий за элемент сцены. Связывает между собой графическое представление сцены и элемент сцены в
    # структуре проекта. Обеспечивает интерфейс настройки и редактирования основных параметров сцены
    def __init__(self, selectorWindow, element, rootItem, parentItem):
        super().__init__(selectorWindow, element, rootItem, parentItem) # Вызываем конструктор суперкласса
    def setup(self, rootItem, parentItem):
        # Переопределнный метод настройки экземпляра
        super().setup(rootItem, parentItem)                                     # Вызывам метод настройки супекласса
        self.rootItem.scenesCounter += 1                                        # Увеличиваем счетчик сцен на 1
        self.rootItem.usedSceneNames.append(self.name)                          # Помещаем имя сцены в список уже использованных имен сцен
        self.parentItem = parentItem                                            # Фиксируем родителя
        self.parentItem.listOfScenes.append(self)                               # Добавляем экземпляр в список сцен родителя
        if os.path.exists(self.element.sceneData['SceneFile']):
            self.sceneModel = SceneModel.fromSceneData(self.mainWindow, self.element.sceneData['SceneFile'])
        else:
            self.sceneModel = SceneModel(self.mainWindow, self.element.sceneData)   # Создаем экземпляр сцены
    def setPopupMenu(self):
        # Перегружаем метод вызова контекстного меню
        self.popupMenu = PMSceneMenu(self)
    def setSceneToEditor(self):
        # Метод загрузки сцены в редактор
        self.mainWindow.SCENE_MANAGER.setScene(self.sceneModel) # Загружаем сцену в виджет
        self.mainWindow.SCENE_MANAGER.refresh()                 # Обновляем редактор
    def save(self):
        # Метод сохранения сцены. Вызывает аналогичный метод у экземпляра сцены
        self.sceneModel.save()