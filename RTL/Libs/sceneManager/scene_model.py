'''
В этом модуле описывается визуальная модель сцены
'''
from configobj import ConfigObj
from PyQt4.QtGui import *
from PyQt4.QtCore import *
# Считываем базовый размер тайла
TILESIZE = int(ConfigObj("config.ini")['EDITOR OPTIONS']['Tilesize'])

class SceneModel(QGraphicsScene):
    PASSABILITY = ('Empty','Solid','Hover')	# Список возможных значений проходимости клетки
    def __init__(self, main, sceneData):
        '''
        Конструктор класса принимает два аргумента:
            main        - ссылка на главное окно
            sceneData   - словарь параметров сцены
        '''
        self.mainWindow = main      # Ссылка на главное окно
        self.PROXY = main.PROXY     # Ссылка на прокси-буфер
        self.setupData(sceneData)   # Устанавливаем переданные данные
        super().__init__(0, 0, float(TILESIZE * self.tiles_in_row), float(TILESIZE * self.tiles_in_col)) # Конструктор суперкласса
        self.placeTiles(self.tilelist)      # Расставляем тайлы по сцене, если они есть
        self.setTriggers(self.triggers)     # Настраиваем триггеры
        self.setPassability(self.walkMap)   # Настраиваем карту проходимости
# ==========Перегруженные методы доступа к атрибутам сцены==========
    def width(self):		return int(super().width())
    def height(self):		return int(super().height())
# ==========Методы-установщики==========
    def setupData(self, sceneData):
        # Метод установки атрибутов сцены на основе переданных данных sceneData
        self.data = sceneData
        self.ID             = self.data['ID']           # Уникальный номер сцены
        self.IDstr          = self.data['IDString']     # Уникальный номер сцены встроковом представлении
        self.name           = self.data['Name']         # Имя сцены
        self.tiles_in_row   = self.data['Width']        # Ширина в тайлах
        self.tiles_in_col   = self.data['Height']       # Высота в тайлах
        self.tileset        = self.data['MainTileset']  # Имя базового тайлсета
        self.tilelist       = self.data['Tiles']        # Набор тайлов в виде списка
        self.triggers       = self.data['Triggers']     # Набор триггеров в виде словаря
        self.walkMap        = self.data['WalkMap']      # Карта проходимости в виде словаря
    def placeTiles(self, tilelist):
        # Метод размещения тайлов из списка tilelist по сцене
        for tile in tilelist: self.addItem(tile.duplicate())
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
    def setPassability(self, passmap):
        # Метод установки таблицы проходимости сцены. На этапе отладки программы доступна возможность генерирования
        # случайной карты проходимости в случае отсутствия аргумента
        pass
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
    def save(self, path):
        # Метод сохранения данных сцены в файл
        print(self.IDstr)