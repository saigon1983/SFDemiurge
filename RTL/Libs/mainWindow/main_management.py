'''
В этом модуле описывается класс, осуществляющий менеджмент меню, панели инструментов и
строки состояния главного окна
'''
from RTL.Libs.mainWindow.main_widgets import MenuBar, MainMenu, ToolBar, StatusBar
from RTL.Libs.mainWindow.main_actions import *

class BarsManager:
    def __init__(self, main):
        # Инициализируем менеджер
        self.mainWindow = main
        # Инициализируем виджеты
        self.setWidgets()	# Подключаем виджеты
        self.setActions()	# Подключаем доступные действия
        self.setupAll()		# Настраиваем виджеты
#========== Методы настройки виджетов главного окна ==========
    def setWidgets(self):
        # Метод инициализации виджетов
        self.mainWindow.MAINMENU    = MenuBar(self.mainWindow)	# Подключаем главное меню
        self.mainWindow.TOOLBAR     = ToolBar(self.mainWindow)	# Подключаем панель инструментов
        self.mainWindow.STATUSBAR   = StatusBar(self.mainWindow)# Подключаем строку состояния
    def setActions(self):
        # Метод настройки доступных действий QAction
        self.tilesizeSwitchersGroup = TilesizeSwitchers(self.mainWindow, self.mainWindow.PROXY.setActualTilesize)
        self.layerSwitchersGroup = LayerSwitchers(self.mainWindow, self.mainWindow.PROXY.setActiveLayer)
        self.layerVisibilityGroup = LayersVisibilitySwitchers(self.mainWindow, self.mainWindow.PROXY.switchDrawScene)
        self.drawGridAction = DrawGridAction(self.mainWindow)
        self.drawPassAction = DrawPassAction(self.mainWindow)
        self.viewScaler = ViewScaler(self.mainWindow)
        self.newAction  = NewProjectAction(self.mainWindow)
        self.openAction = OpenProjectAction(self.mainWindow)
        self.saveAction = SaveProjectAction(self.mainWindow)
        self.quitAction = QuitAction(self.mainWindow)
        self.undoAction = UndoAction(self.mainWindow)
        self.redoAction = RedoAction(self.mainWindow)
    def setupAll(self):
        # Метод, запускающий настройку всех виджетов
        self.setMainMenu()	# Настройка главного меню
        self.setToolBar()	# Настройка панели инструментов
        self.setStatusBar()	# Настройка строки состояния
#========== Методы непосредственной настройки каждой панели ==========
    def setMainMenu(self):
        # Метод настройки главного меню
        # Метод настройки главного меню
        #=============================================
        self.menuProject    = MainMenu('Проект', self.mainWindow)
        self.menuProject.addAction(self.newAction)
        self.menuProject.addAction(self.openAction)
        self.menuProject.addAction(self.saveAction)
        self.menuProject.addSeparator()
        self.menuProject.addAction(self.quitAction)
        #=============================================
        self.menuEdit 		= MainMenu('Правка', self.mainWindow)
        self.menuEdit.addAction(self.undoAction)
        self.menuEdit.addAction(self.redoAction)
        #=============================================
        self.menuScene	= MainMenu('Сцена', self.mainWindow)
        self.menuScene.addActions(self.tilesizeSwitchersGroup.actions())
        self.menuScene.addSeparator()
        self.menuScene.addActions(self.layerSwitchersGroup.actions())
        self.menuScene.addSeparator()
        self.menuScene.addActions(self.layerVisibilityGroup.actions())
        self.menuScene.addSeparator()
        self.menuScene.addAction(self.drawGridAction)
        self.menuScene.addAction(self.drawPassAction)
        #=============================================
        menuDatabase 	    = MainMenu('База данных', self.mainWindow)
        #=============================================
        menuGame 		    = MainMenu('Игра', self.mainWindow)
        #=============================================
        menuHelp 			= MainMenu('Справка', self.mainWindow)
        #=============================================
        MENUS = (self.menuProject, self.menuEdit, self.menuScene, menuDatabase, menuGame, menuHelp)
        for menu in MENUS:
            self.mainWindow.MAINMENU.addMenu(menu)
    def setToolBar(self):
        # Метод настройки панели инструментов
        self.mainWindow.TOOLBAR.addAction(self.openAction)
        self.mainWindow.TOOLBAR.addAction(self.saveAction)
        self.mainWindow.TOOLBAR.addSeparator()
        self.mainWindow.TOOLBAR.addAction(self.undoAction)
        self.mainWindow.TOOLBAR.addAction(self.redoAction)
        self.mainWindow.TOOLBAR.addSeparator()
        self.mainWindow.TOOLBAR.addActions(self.tilesizeSwitchersGroup.actions())
        self.mainWindow.TOOLBAR.addSeparator()
        self.mainWindow.TOOLBAR.addActions(self.layerSwitchersGroup.actions())
        self.mainWindow.TOOLBAR.addSeparator()
        self.mainWindow.TOOLBAR.addActions(self.layerVisibilityGroup.actions())
        self.mainWindow.TOOLBAR.addSeparator()
        self.mainWindow.TOOLBAR.addAction(self.drawGridAction)
        self.mainWindow.TOOLBAR.addAction(self.drawPassAction)
        self.mainWindow.TOOLBAR.addSeparator()
        self.mainWindow.TOOLBAR.addWidget(self.viewScaler)
    def setStatusBar(self):
        # Метод настроуки строки состояния
        pass
#========== Методы управления панелями и действиями ==========
    def updateUndoRedo(self):
        # Метод обновления состояния кнопок Undo и Redo
        self.undoAction.setEnabled(True if self.mainWindow.SCENE_MANAGER.pastScenes   else False)
        self.redoAction.setEnabled(True if self.mainWindow.SCENE_MANAGER.futureScenes else False)
    def updateGridPass(self, mode, drawFG):
        # Метод обновления кнопок переключения режимов отрисовки сетки и отрисовки карты проходимости
        # Если активен режим просмотра проходимости
        if mode == 'Passability':
            self.drawPassAction.setChecked(True)
            self.drawGridAction.setChecked(False)
            self.drawGridAction.setEnabled(False)
        # Если активен другой режим просмотра сцены
        else:
            self.drawGridAction.setEnabled(True)
            self.drawGridAction.setChecked(drawFG)
            self.drawPassAction.setChecked(False)