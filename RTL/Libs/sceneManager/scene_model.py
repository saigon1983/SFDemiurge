'''
В этом модуле описывается визуальная модель сцены
'''
import os, pickle
from random import choice
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from RTL.Libs.sceneManager.scene_tile import Tile

verticalLine = QPainter()

class SceneModel(QGraphicsScene):
    PASSABILITY = ('Empty','Solid','Hover')	# Список возможных значений проходимости клетки
    tileChanged = pyqtSignal() # Сигнал, оповещающий о том, что тайл был добавлен либо удален
    def __init__(self, main, sceneData, firstCreation = True):
        '''
        Конструктор класса принимает два аргумента:
            main        - ссылка на главное окно
            sceneData   - словарь параметров сцены
        '''
        self.mainWindow = main          # Ссылка на главное окно
        self.PROXY = main.PROXY         # Ссылка на прокси-буфер
        self.TILESIZE = int(main.CONFIG['EDITOR OPTIONS']['Tilesize'])
        self.setupData(sceneData)       # Устанавливаем переданные данные
        super().__init__(0, 0, float(self.TILESIZE * self.tiles_in_row), float(self.TILESIZE * self.tiles_in_col)) # Конструктор суперкласса
        self.setupTiles(self.tilelist)      # Расставляем тайлы по сцене, если они есть
        self.setTriggers(self.triggers)     # Настраиваем триггеры
        self.setPassability()               # Настраиваем карту проходимости
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
    def setTriggers(self, triggers):
        # Метод установки значений по умолчанию триггеров сцены
        self.saved = True   # Флаг сохранности сцены. Значение False означает, что сцена была изменена и изменения не сохранены
    def setPassability(self):
        # Метод установки таблицы проходимости сцены. На этапе отладки программы доступна возможность генерирования
        # случайной карты проходимости в случае отсутствия аргумента
        if not self.walkMap:
            # Если карты проходимости нет, генерируем ее случайным образом (доступно на этапе отладки)
            self.walkMap = {}
            for x in range(1, self.tiles_in_row+1):
                self.walkMap[x] = {}
                for y in range(1, self.tiles_in_col+1):
                    self.walkMap[x][y] = {}
                    self.walkMap[x][y]['passability'] = choice(SceneModel.PASSABILITY)
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
        if self.PROXY.DRAW_BACK:
            sidesizeX  	= self.width()  	                        # Ширина сцены
            sidesizeY 	= self.height() 	                        # Высота сцены
            back.setBrush(Qt.lightGray)  		                    # Фон для всего виджета
            back.drawRect(0, 0, sidesizeX + 7000, sidesizeY + 5000) # Отрисовка внешнего фона
            back.setBrush(Qt.darkBlue)       	                    # Фон, занимающий только саму карту
            back.drawRect(0, 0, sidesizeX, sidesizeY) 	            # Отрисовка фона выбранного размера локации
    def drawForeground(self, fore, rect):
        # Метод отрисовки переднего фона. Зависит от текущего режима viewMode
        tilesize    = self.TILESIZE # Базовый размер тайла
        if self.PROXY.VIEW_MODE == 'Simple' and self.PROXY.DRAW_GRID:
            # Если выбран простой режим отображения и включен триггер отрисовки сетки - рисуем сетку с базовым размером тайла
            fore.setPen(Qt.darkYellow)  # Устанавливаем цвет кисти
            sidesizeX  	= self.width()  # Ширина сцены
            sidesizeY 	= self.height() # Высота сцены
            # Проверяем текущий размер тайла
            # Отрисовываем сетку
            for x in range(0, sidesizeX // tilesize):
                for y in range(0, sidesizeY // tilesize + 1):
                    fore.drawLine(x * tilesize, y * tilesize, x * tilesize + tilesize // 8, y * tilesize)
                    fore.drawLine(x * tilesize + (tilesize // 8) * 7, y * tilesize, (x + 1) * tilesize, y * tilesize)
            for x in range(0, sidesizeX // tilesize + 1):
                for y in range(0, sidesizeY // tilesize):
                    fore.drawLine(x * tilesize, y * tilesize, x * tilesize, y * tilesize + tilesize // 8)
                    fore.drawLine(x * tilesize, y * tilesize + (tilesize // 8) * 7, x * tilesize, (y + 1) * tilesize)
        elif self.PROXY.VIEW_MODE == 'Passability':
            # Если выбран режим отображения проходимости - сетка не рисуется
            for x in range(1, self.tiles_in_row + 1):
                for y in range(1, self.tiles_in_col + 1):
                    fore.setPen(QPen(Qt.NoPen))	# Отключаем перо
                    cell = self.walkMap[x][y]['passability']	# Фиксируем текущий элемент таблицы проходимости
                    # Фиксируем необходимый координаты верхнего левого и правого нижнего угла квадрата
                    X = tilesize * (x-1)
                    Xa = X + tilesize // 6 * 2
                    Y = tilesize * (y-1)
                    Ya = Y + tilesize // 6 * 2
                    Sa = tilesize // 3	# Фиксируем ширину иконки
                    if cell == 'Solid':
                        # Если клетка непроходима - рисуем красный крест на красном фоне
                        fore.setBrush(QColor(255,0,0,50))
                        fore.drawRect(X,Y,tilesize,tilesize)
                        pen = QPen()
                        pen.setWidth(2)
                        pen.setColor(Qt.red)
                        fore.setPen(pen)
                        fore.drawLine(Xa, Ya, Xa + Sa, Ya + Sa)
                        fore.drawLine(Xa + Sa, Ya, Xa, Ya + Sa)
                    elif cell == 'Hover':
                        # Если под клеткой можно проходить - рисуем синий прямоугольник на синем фоне
                        fore.setBrush(QColor(0,0,255,50))
                        fore.drawRect(X,Y,tilesize,tilesize)
                        pen = QPen()
                        pen.setWidth(2)
                        pen.setColor(Qt.blue)
                        pen.setJoinStyle(Qt.MiterJoin)
                        fore.setPen(pen)
                        fore.drawRect(QRect(Xa, Ya, Sa, Sa))
                    elif cell == 'Empty':
                        # Если клетка проходима - рисуем зеленый круг на зеленом фоне
                        fore.setBrush(QColor(0,255,0,50))
                        fore.drawRect(X,Y,tilesize,tilesize)
                        pen = QPen()
                        pen.setWidth(2)
                        pen.setColor(Qt.green)
                        fore.setPen(pen)
                        fore.drawEllipse(QRect(Xa, Ya, Sa, Sa))
                    else:
                        # Во всех остальных случаях выводим сообщение об ошибке
                        raise ValueError('Wrong passability value in cell {}:{}'.format(x, y))
# ==========Методы получения различных данных==========
    def placeTile(self, tile):
        # Метод добавления тайла на сцену
        self.addItem(tile)      # Добавляем тайл на сцену
        self.unsaved()          # Сцена изменена
        self.tileChanged.emit() # Отправляем сообщение
    def removeTile(self, tile):
        # Метод удаления тайла со сцены
        self.removeItem(tile)   # Удаляем тайл со сцены
        self.unsaved()          # Сцена изменена
        self.tileChanged.emit() # Отправляем сообщение
    def unsaved(self):
        # Метод-уведомление, что сцена изменена
        self.saved = False                  # Устанавливаем флаг сохранности в положение False
        self.mainWindow.PROJECT.changed()   # Уведомляем проект о том, что он изменен
    def save(self):
        # Метод сохранения данных сцены в файл
        self.sceneFile = self.mainWindow.getCurrentPath() + "\\Scenes\\" + self.IDstr + '.sdf'
        with open(self.sceneFile, 'wb') as sceneFile:
            pickle.dump(self.getSceneData(), sceneFile)
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
        # TODO Далее должны следовать различные триггеры, но они пока отсутствуют, т.к. все были вынесены в прокси-буфер
        self.sceneData['WalkMap'] = self.walkMap
        return self.sceneData    # Возвращаем получившийся словарь
    def duplicate(self):
        # Метод возвращает копию текущей сцены
        return SceneModel(self.mainWindow, self.getSceneData(), False)
    @classmethod
    def fromSceneData(cls, main, pathToFile):
        # Метод конструирует объект сцены на основе данных из файла
        with open(pathToFile, 'rb') as sceneFile:
            sceneData = pickle.load(sceneFile)
        return cls(main, sceneData, False)