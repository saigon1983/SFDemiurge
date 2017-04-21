'''
Класс MainGui описывает устройство главного окна приложения,
интерфейс которого обеспечивает доступ ко всем основным
возможностям редактора
'''
import os
from PyQt4.QtGui import *
from RTL.Libs.proxyBuffer.proxy import *
from RTL.Libs.projectClass.project_class import Project
from RTL.Libs.mainWindow.main_management import BarsManager
from RTL.Libs.tilesetManager.tileset_manager import TilesetManager
from RTL.Libs.tilesetManager.tile_viewer import TileViewer
from RTL.Libs.tilesetManager.tileset_selector import TilesetSelector
from RTL.Libs.projectManager.project_manager import ProjectManager
from RTL.Libs.sceneManager.scene_manager import SceneManager

class MainGui(QMainWindow):
    def __init__(self, config, project = None):
        '''
        Конструктор принимает два аргумента:
            config 	- ссылка на объект конфигурации, являющийся доступом к файлу основных конфигураций
            project 	- ссылка на текущий проект, с которым работает редактор. По умолчанию None. В этом случае редактор ищет
                          ссылку на последний запущенный проект, либо запускает создание нового проекта
        '''
        QMainWindow.__init__(self)		# Инициализируем суперкласс
        self.setupSelf()				# Настраиваем виджет
        self.configSelf(config, project)# Настраиваем атрибуты
        self.setHeader()				# Пишем корректный заголовок
        self.setupLayouts()				# Настраиваем компоновщики
        self.initWidgets()				# Инициализируем виджеты
        self.placeWidgets()				# Устанавливаем виджеты в компоновщики
#========== Методы настройки экземпляра ==========
    def setupSelf(self):
        # Метод настройки виджета
        self.setCentralWidget(QFrame())	# Задаем центральный виджет
        self.move(100,100)	  # Располагаем окно на 100 пикселей правее и на 100 пикселей ниже левого верхнего угла монитора
        #self.showMaximized() # Запускает приложение в окне на весь экран
        #self.showFullScreen()# Запускает приложение в полноэкранном режиме
    def configSelf(self, config, project):
        # Метод настройки атрибутов экземпляра
        self.CONFIG 	= config		# Ссылка на файл конфигураций
        self.setupProject(project)		# Загрузка/построение проекта
        self.PROXY 	= ProxyBuffer(self)	# Ссылка на прокси-буфер
    def setHeader(self):
        # Метод настройки заголовка окна
        self.setWindowTitle('SForce Demiurge v. {}. Build {}. Project: {}{}'.format(
                                                                        self.CONFIG['MAIN OPTIONS']['Version'],
                                                                        self.CONFIG['MAIN OPTIONS']['Build'],
                                                                        self.PROJECT.name,
                                                                        self.saveStatus())) # Заголовок окна
    def saveStatus(self):
        # Метод проверки сохраненности проекта. Возвращает "*", если проект изменен и не сохранен и пустую строку в ином случае
        if self.PROJECT.saved: return ''
        else: return '*'
    def setupLayouts(self):
        # Метод настройки менеджера размещения
        self.mainHLayout = QHBoxLayout(self.centralWidget())# Основной, горизонтальный (на 2 элемента)
        self.mainVLayout = QVBoxLayout()                    # Левый, вертикальный
        self.tilesetLayout = QHBoxLayout()					# Компоновщик виджетов работы с тайлсетом
        self.mainVLayout.addLayout(self.tilesetLayout)
        self.mainHLayout.addLayout(self.mainVLayout)
    def initWidgets(self):
        # Метод конструирования виджетов
        self.TILE_VIEWER			= TileViewer(self)	# Виджет отображения текущего тайла
        self.TILESET_MANAGER 	= TilesetManager(self)	# Виджет работы с тайлсетом
        self.PROJECT_MANAGER	= ProjectManager(self)	# Виджет менеджмента структуры проекта
        self.SCENE_MANAGER	= SceneManager(self)		# Виджет менеджмента структуры проекта
        self.TILESET_SELECTOR	= TilesetSelector(self)	# Виджет отображения текущего тайла
        self.BARS = BarsManager(self)					# Настройка основных панелей
    def placeWidgets(self):
        # Метод размещения виджетов по компоновщикам
        self.mainVLayout.addWidget(self.TILESET_MANAGER)
        self.mainVLayout.addWidget(self.PROJECT_MANAGER)
        self.mainHLayout.addWidget(self.SCENE_MANAGER)
        self.tilesetLayout.addWidget(self.TILE_VIEWER)
        self.tilesetLayout.addWidget(self.TILESET_SELECTOR)
#========== Методы управления текущим проектом ==========
    def projectSave(self):
        # Метод сохранения проекта
        self.PROJECT.save() # Сохраняем проект
        self.setHeader()    # Меняем заголовок окна (убираем зведочку из названия)
        print('Project saved!')
    def projectLoad(self):
        # Метод загрузки проекта из файла
        projectPath = os.path.dirname(QFileDialog.getOpenFileName(self, 'Выберите проект', './Projects', filter = 'Файлы проекта (*.data)'))
        self.PROJECT = Project.fromFile(self, projectPath)  # Запускаем окно загрузки проекта
        self.PROJECT_MANAGER.initProject()                  # Устанавливаем созданный проект текущим
        self.setHeader()                                    # Обновляем заголовок окна
        print('Project loaded!')
    def projectCreate(self):
        # Метод создания нового проекта
        self.PROJECT = Project.fromStratch(self)# Создаем новый проект посредством менеджера создания
        self.PROJECT_MANAGER.initProject()      # Устанавливаем созданный проект текущим
        self.setHeader()                        # Обновляем заголовок окна
        print('Project created!')
#========== Методы для начала работы ==========
    def getRecentProjects(self):
        # Метод возвращает список последних запускаемых проектов
        self.recentProjects = []
        for i in range(8):
            link = self.CONFIG['SYSTEM OPTIONS']['Recent {}'.format(i)]
            if link:	self.recentProjects.append(link)
    def setupProject(self, project):
        # Метод установки текущего проекта
        if project: self.PROJECT = project	# Если проект явно передан, просто устанавливаем его
        else:								# Если проект не передан, запускаем процедуру выбора проекта
            self.getRecentProjects()
            if self.recentProjects:
                self.PROJECT = Project.fromFile(self, self.recentProjects[-1])
            else:
                self.PROJECT = Project.fromStratch(self)
#========== Методы завершения работы приложения ==========
    def closeEvent(self, event):
        # Метод перехвата события выхода из приложения. Проверяет сохранность всех данных и закрывает редактор
        if self.couldExit():
            self.quitProgram()
            event.accept()
        else:
            event.ignore()
    def couldExit(self):
        # Метод проверки возможности безопасно закрыть приложение
        return True	# TODO: в дальнейшем заменить True на проверку сохранения всех изменений
    def quitProgram(self):
        # Метод выхода из приложения. Перед закрытием совершает ряд необходимых операций, после чего завершает работу
        print('Closed!')
        qApp.quit()