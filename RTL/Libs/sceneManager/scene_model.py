'''
В этом модуле описывается визуальная модель сцены
'''
import os, pickle
from configobj import ConfigObj
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from RTL.Libs.sceneManager.scene_tile import Tile

class SceneModel(QGraphicsScene):
    PASSABILITY = ('Empty','Solid','Hover')	# Список возможных значений проходимости клетки
    def __init__(self, main, sceneData, firstCreation = True):
        '''
        Конструктор класса принимает два аргумента:
            main        - ссылка на главное окно
            sceneData   - словарь параметров сцены
        '''
        self.mainWindow = main      # Ссылка на главное окно
        self.PROXY = main.PROXY     # Ссылка на прокси-буфер
        self.TILESIZE = int(main.CONFIG['EDITOR OPTIONS']['Tilesize'])
        self.setupData(sceneData)   # Устанавливаем переданные данные
        super().__init__(0, 0, float(self.TILESIZE * self.tiles_in_row), float(self.TILESIZE * self.tiles_in_col)) # Конструктор суперкласса
        self.setupTiles(self.tilelist)      # Расставляем тайлы по сцене, если они есть
        self.setTriggers(self.triggers)     # Настраиваем триггеры
        self.setPassability(self.walkMap)   # Настраиваем карту проходимости
        if firstCreation: self.save()       # Создаем файл для сцены в случае, когда сцена не загружена из файла
# ==========Перегруженные методы доступа к атрибутам сцены==========
    def width(self):		return int(super().width())
    def height(self):		return int(super().height())
# ==========Методы-установщики==========
    def setupData(self, sceneData):
        # Метод установки атрибутов сцены на основе переданных данных sceneData
        self.sceneData = sceneData
        self.ID             = self.sceneData['ID']           # Уникальный номер сцены
        self.IDstr          = self.sceneData['IDString']     # Уникальный номер сцены встроковом представлении
        self.name           = self.sceneData['Name']         # Имя сцены
        self.tiles_in_row   = self.sceneData['Width']        # Ширина в тайлах
        self.tiles_in_col   = self.sceneData['Height']       # Высота в тайлах
        try: self.tileset       = self.sceneData['MainTileset']  # Имя базового тайлсета
        except: self.tileset    = 'World Map Main'
        try: self.tilelist      = self.sceneData['Tiles']        # Набор тайлов в виде списка
        except: self.tilelist   = []
        try: self.triggers      = self.sceneData['Triggers']     # Набор триггеров в виде словаря
        except: self.triggers   = {}
        try: self.walkMap       = self.sceneData['WalkMap']      # Карта проходимости в виде словаря
        except: self.walkMap    = {}
    def setupTiles(self, tilelist):
        # Метод размещения тайлов из списка tilelist по сцене
        for tileData in tilelist: self.addItem(Tile.fromTileData(tileData))
    def placeTile(self, tile):
        # Метод помещает на сцену переданный тайл tile
        self.addItem(tile)
    def setTriggers(self, triggers):
        '''
		Метод установки триггеров сцены. Триггеры могут быть следующими:
			viewMode - режим просмотра сцены. Имеет следующие значения:
				Simple 			- простой режим, позволяющий видеть все объекты так, как они будут видны в игре
				Passability 	- режим просмотра проходимости сцены
			drawBG - триггер необходимости отрисовки заднего фона. Имеет положения True или False
			drawFG - триггер необходимости отрисовки вспомогательной сетки. Имеет положения True или False
		Если методу не передается какой-либо набор триггеров, они устанавливаются по умолчанию
		'''
        try:    self.viewMode   = triggers['viewMode']
        except: self.viewMode   = 'Simple'  # Режим просмотра сцены
        try:    self.drawBG     = triggers['drawBG']
        except: self.drawBG     = True      # Флаг отрисовки заднего фона
        try:    self.drawFG     = triggers['drawFG']
        except: self.drawFG     = True      # Флаг отрисовки переднего фона
        self.saved = True   # Флаг сохранности сцены. Значение False означает, что сцена была изменена и изменения не сохранены
    def setPassability(self, walkMap):
        # Метод установки таблицы проходимости сцены. На этапе отладки программы доступна возможность генерирования
        # случайной карты проходимости в случае отсутствия аргумента
        pass
    def createSceneFile(self):
        # Метод проверяет, есть ли в каталоге сцен файл, соответствующий данной сцене, и если его нет - создает его и
        # записывает в него первоначальные данные
        self.sceneFile = self.mainWindow.getCurrentPath() + "\\Scenes\\" + self.IDstr + '.sdf'
        if not os.path.exists(self.sceneFile):
            sceneFile = open(self.sceneFile, 'wb')
            sceneFile.close()
            self.save()
# ==========Перегруженные методы отрисовки заднего и переднего фонов==========
    def drawBackground(self, back, rect):
        # Метод отрисовки заднего фона
        if self.drawBG:
            sidesizeX  	= self.width()  	                        # Ширина сцены
            sidesizeY 	= self.height() 	                        # Высота сцены
            back.setBrush(Qt.lightGray)  		                    # Фон для всего виджета
            back.drawRect(0, 0, sidesizeX + 7000, sidesizeY + 5000) # Отрисовка внешнего фона
            back.setBrush(Qt.darkBlue)       	                    # Фон, занимающий только саму карту
            back.drawRect(0, 0, sidesizeX, sidesizeY) 	            # Отрисовка фона выбранного размера локации
    def drawForeground(self, fore, rect):
        # Метод отрисовки переднего фона. Зависит от текущего режима viewMode
        pass
    def save(self):
        # Метод сохранения данных сцены в файл
        self.sceneFile = self.mainWindow.getCurrentPath() + "\\Scenes\\" + self.IDstr + '.sdf'
        with open(self.sceneFile, 'wb') as sceneFile:
            pickle.dump(self.getSceneData(), sceneFile)
        print(self.sceneFile)
        self.saved =True
    def getSceneData(self):
        # Метод пакует данные сцены в словарь и возвращает его
        self.sceneData['ID'] = self.ID
        self.sceneData['IDString'] = self.IDstr
        self.sceneData['Name'] = self.name
        self.sceneData['Width'] = self.tiles_in_row
        self.sceneData['Height'] = self.tiles_in_col
        self.sceneData['MainTileset'] = self.tileset
        self.sceneData['Tiles'] = []
        for item  in self.items():
            self.sceneData['Tiles'].append(item.getTileData())
        self.sceneData['Triggers'] = {}
        self.sceneData['Triggers']['viewMode'] = self.viewMode
        self.sceneData['Triggers']['drawBG'] = self.drawBG
        self.sceneData['Triggers']['drawFG'] = self.drawFG
        self.sceneData['WalkMap'] = self.walkMap
        return self.sceneData    # Возвращаем получившийся словарь
    @classmethod
    def fromSceneData(cls, main, pathToFile):
        # Метод конструирует объект сцены на основе данных из файла
        with open(pathToFile, 'rb') as sceneFile:
            sceneData = pickle.load(sceneFile)
        return cls(main, sceneData, False)