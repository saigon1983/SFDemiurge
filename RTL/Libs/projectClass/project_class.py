'''
Класс Project отражает состояние проекта. Хранит текущие настройки проекта, его пути. При создании проекта с нуля
создает папку проекта в соответствующем каталоге, копирует туда все необходимые файлы и ресурсы. При обращении
к экземпляру из редактора может предоставлять необходимые данные о проекте. Так же подерживает фукнции загрузки
и сохранения проекта
'''
import shutil, os, pickle
from RTL.Libs.projectClass.project_creator import ProjectCreator
from RTL.Libs.projectClass.project_structure import *

class Project:
    PROJECTSLOCATION    = 'Projects'	# Путь к каталогу проектов
    SOURSESLOCATION     = r'RTL\Game'	# Путь к каталогу базовых ресурсов проекта
    def __init__(self, main, projectData):
        '''
        Конструктор класса принимает три аргумента:
            main					- ссылка на главное окно
            projectData 		- словарь основных данных о проекте
            projectStructure	- объект структуры проекта
        '''
        self.mainWindow = main
        self.data 	= projectData			# Ссылка на данные проекта
        self.name 	= self.data['Name']		# Имя проекта
        self.folder	= self.data['Folder']	# Имя каталога проекта
        self.path	= os.path.join(Project.PROJECTSLOCATION, self.folder)	# Путь к каталогу проекта
        self.pid	= self.data['PID']		# Порядковый номер проекта
        self.tree	= self.data['Structure']# Структура проекта
        self.save()							# Сохраняем проект в каталог в файл с именем project.data
#========== Методы управления проектом ==========
    def changed(self):
        # Метод-слот, устанавливающий флаг проекта saved в положение False
        self.saved = False
        self.mainWindow.setHeader() # Меняем заголовок окна (добавляем зведочку к названию)
    def save(self):
        # Метод сохранения проекта в файл
        with open(os.path.join(self.path, 'project.data'), 'wb') as projectFile:
            pickle.dump(self.data, projectFile)
        self.saved	= True  # Триггер сохраненности проекта. Равен False, если в проекте есть несохраненные изменения
#========== Методы класса создания экземпляра ==========
    @classmethod
    def fromStratch(cls, main):
        # Метод создания проекта "с нуля". Создаются имя проекта, имя каталога, базовая структура
        CONFIG = main.CONFIG
        # Запускаем окно создания проекта, где вводим его имя и имя папки
        projectCreator = ProjectCreator(Project.PROJECTSLOCATION)
        # Если получен положительный ответ (создание прошло успешно), продолжаем работу
        if projectCreator.result() == 1:
            # Сохраняем результаты работы окна создания (кортеж с именем проекта и названием папки)
            results = projectCreator.inputResults
            # Создаем объект данных (словарь), на основе которого строится экземпляр класса
            newProjectData = {}
            # Создаем объект структуры проекта, который строится в методе класса structureTemplate()
            newProjectStructure = Project.structureTemplate(results[0], os.path.join(Project.PROJECTSLOCATION, results[1]))	#
            # Заполняем данные о проекте
            newProjectData['Name'] 		= results[0]			# Имя проекта
            newProjectData['Folder'] 	= results[1]			# Папка проекта
            newProjectData['PID'] 		= int(CONFIG['PROJECTS OPTIONS']['PID']) + 1	# Порядковый номер проекта
            newProjectData['Structure'] = newProjectStructure	# Структура проекта
            # Увеличиваем порядковый номер в файле конфигураций
            CONFIG['PROJECTS OPTIONS']['PID'] = newProjectData['PID']
            CONFIG.write()
            # Создаем папку проекта
            path = os.path.join(Project.PROJECTSLOCATION, newProjectData['Folder'])
            os.mkdir(path)
            os.mkdir(path + '\\Scenes')
            # Перемещаем в нее все необходимые файлы и ресурсы
            for file in os.listdir(Project.SOURSESLOCATION):
                shutil.copy(os.path.join(Project.SOURSESLOCATION, file), os.path.join(path, file))
            # Создаем экземпляр класса на основе подготовленных данных
            newProject = cls(main, newProjectData)
            # Помещаем путь к папке нового проекта в список последних запущенных проектов
            Project.saveToRecents(newProject)
            # Возвращаем полученный проект
            return newProject
    @classmethod
    def fromFile(cls, main, folderpath):
        # Метод создания проекта на основе данных, полученных из файла project.data в папке folderpath
        with open(os.path.join(folderpath, 'project.data'), 'rb') as projectFile:
            newProjectData 	= pickle.load(projectFile)
        return cls(main, newProjectData)
    @classmethod
    def saveToRecents(cls, project):
        # Метод записывает переданный проект в список последних проектов. Если текущих проектов уже 8, то происходит
        # смещение на 1 единицу вниз (первый в списке проект удаляется, а текущий проект записывается последним)
        CONFIG = project.mainWindow.CONFIG
        recentProjects = project.mainWindow.recentProjects()
        if len(recentProjects) < 8:
            CONFIG['SYSTEM OPTIONS']['Recent {}'.format(len(recentProjects))] = project.path
        else:
            for i in range(7):
                CONFIG['SYSTEM OPTIONS']['Recent {}'.format(i)] = recentProjects[i+1]
            CONFIG['SYSTEM OPTIONS']['Recent 7'] = project.path
        CONFIG.write()
    @classmethod
    def structureTemplate(cls, name, folder):
        # Метод создания шаблонной структуры проекта для создания проекта "с нуля"
        tree = ProjectRootElement(name, folder = folder)# Создаем корневой элемент
        tree.addScene(ProjectWorldMapElement(tree))     # Подгружаем в него объект карты мира
        return tree                                     # Возвращаем корневой элемент