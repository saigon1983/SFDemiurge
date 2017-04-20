'''
В файле описываются все классы структуры проекта представляет из себя некое дерево, которое содержит все
подгруппы проекта, а так же названия всех сцен и их данные
'''

class ProjectRootElement:
    # Корневой элемент проекта
    ElementCounter  = 0 # Счетчик всех элементов
    GroupsCounter   = 1 # Счетчик подгрупп
    ScenesCounter   = 1 # Счетчик сцен
    def __init__(self, name, tag = 'Root element', parent = None):
        '''
        Констурктор принимает 3 аргумента
            name -      имя элемента
            tag -       Тег элемента. Может быть трех значений ('Root element', 'Group element', 'Scene element')
            parent -    объект-родитель. Отсутствует по умолчанию для корневого элемента
        '''
        # Создание списков
        self.GROUPS = []        # Список вложенных групп
        self.SCENES = []        # Список вложенных сцен
        # Создание атрибутов класса
        self.name   = name      # Имя
        self.tag    = tag       # Тег
        self.parent = parent    # Объект-родитель
        self.correctLevels()    # Корректировка уровней
        # Создание идентификаторов
        self.elemID = ProjectRootElement.ElementCounter # Порядковый номер элемента
        self.typeID = 0                                 # Порядковый номер по типу элемента
        self.elemIDstr  = 'EL'+str(self.elemID).zfill(4)# Строковое представление ID элемента
        self.typeIDstr  = 'RT0000'                      # Строковое представление ID типа
        ProjectRootElement.ElementCounter += 1          # Увеличиваем счетчик элементов на 1
#========== Методы настройки элементов ==========
    def correctLevels(self):
        # Метод корректировки (установки) уровней вложенности элемента
        # Для корня уровень вложенности всегда равен 0, для остальных элементов - УВ родителя + 1
        if self.tag == 'Root element':  self.level = 0
        else:   self.level = self.parent.level + 1
        # Рекурсивно обходим все вложенные элементы
        for group in self.GROUPS: group.correctLevels()
        for scene in self.SCENES: scene.correctLevels()
    def correctCounters(self):
        # Метод коррекции показаний счетчиков объектов. Запускается при загрузке структуры из файла
        if self.tag == 'Root element':  ProjectRootElement.ElementCounter += 1
        for group in self.GROUPS:
            ProjectRootElement.ElementCounter += 1
            ProjectRootElement.GroupsCounter  += 1
            group.correctCounters()
        for scene in self.SCENES:
            ProjectRootElement.ElementCounter += 1
            ProjectRootElement.ScenesCounter  += 1
#========== Методы внутреннего менеджмента ==========
    def changeParent(self, newParent):
        # Метод смены родителя. Удаляет объект из списков родителя, добавляет его в списки нового родителя
        if self.tag == 'Group element':
            self.parent.GROUPS.remove(self)
            newParent.GROUPS.append(self)
        if self.tag == 'Scene element':
            self.parent.SCENES.remove(self)
            newParent.SCENES.append(self)
        self.parent = newParent
        self.correctLevels()    # Корректируем уровни вложенности
    def addGroup(self, someData):
        # Метод добавляет к списку групп новую группу. Если в качестве аргумента передается строка, она
        # считается именем группы и на ее основе создается новый объект ProjectGroupElement. Если в качестве
        # аргумента передается объект группы, то ему просто меняется родитель
        if type(someData) == str:                   ProjectGroupElement(someData, self)
        elif type(someData) == ProjectGroupElement: someData.changeParent(self)
        else: raise TypeError('Wrong someData passed to addGroup() method! Must be String or ProjectGroupElement,\
                              but {} recieved!'.format(type(someData)))
    def addScene(self, someData):
        # Метод добавляет к списку сцен новую сцену. Если в качестве аргумента передается строка, она
        # считается именем сцены и на ее основе создается новый объект ProjectSceneElement. Если в качестве
        # аргумента передается объект сцены, то ему просто меняется родитель
        if type(someData) == str:                   ProjectSceneElement(someData, self)
        elif type(someData) == ProjectSceneElement: someData.changeParent(self)
        else: raise TypeError('Wrong someData passed to addScene() method! Must be String or ProjectSceneElement,\
                              but {} recieved!'.format(type(someData)))
#========== Методы внешнего менеджмента ==========
    def compile(self):
        # Метод обходит все вложенные элементы и сохраняет их данные в словарь
        pass
#========== Методы представления объекта ==========
    def info(self, tab = ''):
        # Метод возвращает строку, представляющую из себя дерево структуры
        tab = tab
        info = ''
        info += tab + '{} ({}). Level {}\n'.format(self.name, self.tag, self.level)
        tab += '\t'
        for G in self.GROUPS: info += G.info(tab)
        for S in self.SCENES: info += S.info(tab)
        return info
    def __str__(self):
        # Перегруженный метод строкового представления объекта
        return self.info().strip()
class ProjectGroupElement(ProjectRootElement):
    # Элемент подгруппы
    def __init__(self, name, parent):
        '''
        Конструктор принимает два аргумента, т.к. тег создается автоматически
        '''
        super().__init__(name, 'Group element', parent) # Инициализируем суперкласс
        self.typeID = ProjectRootElement.GroupsCounter  # Порядковый номер по типу элемента
        self.typeIDstr  = 'GR'+str(self.typeID).zfill(4)# Строковое представление ID типа
        ProjectRootElement.GroupsCounter += 1           # Увеличиваем счетчик элементов типа на 1
        self.parent.GROUPS.append(self)                 # Добавляем экземпляр в список групп родителя

class ProjectSceneElement(ProjectRootElement):
    # Элемент сцены. В отличие от остальных, не может содержать вложенных сцен и групп
    # Отменяем использование добавляющих методов
    addGroup = property(doc='(!) Disallowed inherited')
    addScene = property(doc='(!) Disallowed inherited')
    def __init__(self, name, parent, sceneData = {}, sceneObject = None):
        '''
        Конструктор принимает два аргумента, т.к. тег создается автоматически
        '''
        super().__init__(name, 'Scene element', parent) # Инициализируем суперкласс
        self.typeID = ProjectRootElement.ScenesCounter  # Порядковый номер по типу элемента
        self.typeIDstr  = 'AR'+str(self.typeID).zfill(4)# Строковое представление ID типа
        ProjectRootElement.ScenesCounter += 1           # Увеличиваем счетчик элементов типа на 1
        self.setupScene(sceneData, sceneObject)         # Запускаем настройку сцены
        self.parent.GROUPS.append(self)                 # Добавляем экземпляр в список сцен родителя
    def setupScene(self, someSceneData, someSceneObject):
        # Создаем данные о сцене, либо принимая те, что передаются в аргументе someSceneData, либо
        # устанавливая значения по умолчанию
        self.sceneData = {}
        self.sceneData['Name'] 			= someSceneData.setdefault('Name',          self.name)
        self.sceneData['Width'] 		= someSceneData.setdefault('Width',         10)
        self.sceneData['Height'] 		= someSceneData.setdefault('Height',        10)
        self.sceneData['Tiles'] 	    = someSceneData.setdefault('Tiles',         [])
        self.sceneData['WalkMap'] 		= someSceneData.setdefault('WalkMap',       {})
        self.sceneData['Triggers'] 	    = someSceneData.setdefault('Triggers',      {})
        self.sceneData['MainTileset']   = someSceneData.setdefault('MainTileset',   '')
        # Корректируем имя сцены
        self.name = self.sceneData['Name']
        # Привязываем соответствующий элементу объект сцены. По умолчанию отсутствует