'''
В модуле описывается класс TilesetData, который является простым хранилищем данных о тайлсете
'''
import os
from configobj import ConfigObj
from collections import OrderedDict

class TilesetData:
	PATH = r'RTP\Tilesets'
	def __init__(self):
		self.setup()	# Заупскаем настройку экземпляра
	def setup(self):
		# Метод настройки экземпляра
		self.LIST = ConfigObj(os.path.join(TilesetData.PATH, 'tileset_list.ini'))	# Объект с информацией из файла
		self.DATA = OrderedDict()	# Отформатированный для работы с виджетамми словарь с текущими тайлсетами
		self.NAMES 	= 	[]			# Список уже использованных названий тайлсетов
		self.FILES		=	[]		# Список уже использованных названий файлов тайлсетов
		self.count = 0				# Счетчик количества использовуемых тайлсетов
		for tileset in self.LIST:	# Запускаем обработку данных
			# Увеличиваем счетчик на 1
			self.count += 1
			# Записываем данные в форматированный список
			self.DATA[self.LIST[tileset]['Name']] = {'File': os.path.join(TilesetData.PATH, self.LIST[tileset]['File']),
													 'Line': self.LIST[tileset]['Line'],
													 'Type': self.LIST[tileset]['Type']}
			# Добавляем название тайлсета в список используемых названий
			self.NAMES.append(self.LIST[tileset]['Name'])
			# Добавляем название файла тайлсета в список используемых названий файлов
			self.FILES.append(self.LIST[tileset]['File'])
		
	def appendToFile(self, data):
		# Метод записи данных о новом тайлсете в файл
		# Выполняем проверку на задвоение имени тайлсета или имени файла
		if data['Name'] in self.NAMES: raise ValueError('Tileset name {} already exists!'.format(data['Name']))
		if data['File'] in self.FILES: raise ValueError('Tileset filename {} already exists!'.format(data['File']))
		newEntry 	= 'TILESET ' + str(self.count + 1).zfill(3)	# Новый заголовок типа 'TILESET 0XX', где 0XX - трехзначный порядковый номер тайлсета, генерирующийся автоматически
		newData 	= OrderedDict()										# Создаем новый упорядоченный словарь, необходимый для корректной записи данных в файл
		# Добавляем записи в порядке верной очередности
		newData['Name'] = data['Name']
		newData['Type'] = data['Type']
		newData['File'] = data['File']
		newData['Line'] = data['Line']
		self.LIST[newEntry] = newData
		self.LIST.write()	# Записываем в файл
		self.setup()			# Повторно производим устанвоку, чтобы новые данные зафиксировались