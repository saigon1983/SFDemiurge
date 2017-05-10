# В этом модуле описывается класс TileGroup, который содержит ссылки на все тайлы, преданные этой группе

class TileGroup:
    def __init__(self, scene, zValue = 0.0):
        self.scene      = scene # Ссылка на родительскую сцену
        self.layer      = {}    # Словарь тайлов
        self.counter    = 0     # Счеткик текущего метсоположения для операций итерации
        self.zValue     = zValue# Высота списка, должна быть одинаковой у всех элементов в списке
    def append(self, *tiles):
        # Метод добавления тайла или списка тайлов в набор
        for tile in tiles:
            self.layer['{}:{}'.format(int(tile.x()), int(tile.y()))] = tile
            self.scene.addItem(tile)
    def remove(self, tile):
        # Метод удаления тайла из набора. Если такого тайла в наборе нет, ничего не происходит
        try:
            self.scene.removeTile(tile)
            del self.layer['{}:{}'.format(int(tile.x()), int(tile.y()))]
        except: return
    def becomeOpaque(self):
        # Метод делает все элементы слоя непрозрачными
        for tile in self.layer.values(): tile.setOpacity(1.0)
    def becomeTransparent(self):
        for tile in self.layer.values(): tile.setOpacity(0.2 + self.zValue / 10)
# Переопределяем некоторые методы, чтобы сделать объект итерируемым
    def __len__(self):
        # Перегруженный метод определения размера набора
        return len(self.layer)
    def __str__(self):
        # Метод возвращает строковое представление о наборе
        string = ''
        for key in self.layer.keys():
            string += '{} = {}\n'.format(key, self.layer[key])
        return string
    def __iter__(self):
        # Метод для реализации итерации набора в цикле for
        return self
    def __getitem__(self, index):
        # Метод для обращения к набору по индексам
        try:
            return self.layer[index]
        except: return None