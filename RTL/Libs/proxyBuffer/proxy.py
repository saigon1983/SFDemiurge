'''
Класс ProxyBuffer представляет из себя виртуальный буфер для обмена общей для многих виджетов информацией
'''
from PyQt4.QtCore import *

class ProxyBuffer:
    def __init__(self, main):
        '''
        Конструктор прокси-буфера принимает один аргумент:
            main - ссылка на главное окно приложения
        '''
        self.MAIN = main			# Ссылка на главное окно
        self.CONFIG = main.CONFIG	# Ссылка на объект конфигураций
        self.SCALE = 3				# Текущий уровень масштабирования сцены
        self.TILE = QByteArray()    # Текущий активный тайл. По умолчанию - пустой массив байтов
        self.SIZE = int(self.CONFIG['EDITOR OPTIONS']['Tilesize'])# Текущий размер тайла
        self.LAYER = 1.0            # Текущий активный слой
#========== Методы установки атрибутов ==========
    def setActiveTile(self, pixmap):
        # Метод установки текущего активного тайла
        buffer = QBuffer(self.TILE)     # Создаем буфер
        buffer.open(QIODevice.WriteOnly)# Открываем буфер для записи
        pixmap.save(buffer, 'PNG')      # Сохраняем изображение в массив байтов
        buffer.close()                  # Закрываем буфер
        self.MAIN.TILE_VIEWER.setPixmap(pixmap.scaled(self.SIZE*2,self.SIZE*2)) # Помещаем изображение в TILE_VIEWER
    def setActualTilesize(self, factor):
        # Метод устанвки текущего активного слоя
        self.actualTilesize = int(self.CONFIG['EDITOR OPTIONS']['Tilesize'])//3*factor
        self.MAIN.SCENE_MANAGER.refresh()   # Обновляем менеджер сцены
        self.MAIN.TILESET_MANAGER.refresh() # Обновляем менеджер тайлсетов
    def setActiveLayer(self, value):
        # Метод установки текущего активного слоя
        self.LAYER = value
    def setScaleMode(self, value):
        # Метод установки текущего уровня масштабирования сцены
        self.SCALE = value