'''
Основной файл, запускающий всю программу
'''
import sys
from time import sleep
from configobj import ConfigObj
from RTL.Libs.mainWindow.main_window import *

# Создаем объект приложения
app = QApplication(sys.argv)
# Загружаем файл конфигурации редактора
CONFIG = ConfigObj("config.ini")

def splashScreen(time=3):
	# Функция вызова экрана заставки
	image = QPixmap(r'RTL\Images\Splashscreen\Splashscreen logo.png')	# Загружаем изображение
	loadingScreen = QSplashScreen(image, Qt.WindowStaysOnTopHint)		# Создаем виджет
	app.processEvents()		# Запускаем обработчик
	loadingScreen.show()	# Отображаем заставку
	sleep(time)				# Засыпаем на time секунд
	loadingScreen.hide()	# Скрываем заставку
def deleteRecents():
	# Вспомогательный метод. Удаляет все записи о последних открытых проектах
	for i in range(8):
		CONFIG['SYSTEM OPTIONS']['Recent {}'.format(i)] = ''
	CONFIG.write()
def loadProject(app):
	# Функция загрузки приложения
	CONFIG['MAIN OPTIONS']['Build'] = str(int(CONFIG['MAIN OPTIONS']['Build'])+1)
	CONFIG.write()
	main = MainGui(CONFIG)
	main.show()
	sys.exit(app.exec())
	
if __name__ == '__main__':
	#splashScreen()
	#deleteRecents()
	loadProject(app)
	pass