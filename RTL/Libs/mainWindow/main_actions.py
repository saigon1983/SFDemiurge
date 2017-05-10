'''
В этом модуле описаны объекты действий (наследники QAction) - различные дейсвтия, которые
отображаются в меню и/или панели инструментов
'''
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class AbstractAction(QAction):
    # Абстрактный класс AbstractAction является родителем всех классов, определяющих то или иной действие (QAction)
    def __init__(self, mainWindow, slot, value = None):
        '''
        Метод инициализации. принимает следующие аргументы:
            mainWindow 	- ссылка на главное окно редактора
            slot		- название связанного с активацией текущего действия метода
            value		- некоторое необязательное значение, которое будет пердано в связанный с активацией текущего действия метод
        '''
        self.mainWindow = mainWindow	# Ссылка на главное окно приложения
        super().__init__(mainWindow)	# Инициализируем через суперкласс
        # Подключаем сигнал активации действия к переданному методу
        if slot and value:	self.triggered.connect(lambda: slot(value))
        elif slot:			self.triggered.connect(slot)
#======== Настройка действий по выбору размера тайла========
class SetTilesizeAction(AbstractAction):
    # Класс действий по смене размера выбираемого тайла
    def __init__(self, mainWindow, slot, value):
        # Инициализируем через суперкласс
        super().__init__(mainWindow, slot, value)
        # Назначаем иконки
        icon = QIcon()
        icon.addPixmap(QPixmap("RTL\\Images\\Icons\\tile{}.png".format(value)))	# Иконка в неактивном состоянии
        icon.addPixmap(QPixmap("RTL\\Images\\Icons\\tile{}A.png".format(value)), QIcon.Normal, QIcon.On)	# Иконка в активном состоянии
        self.setIcon(icon)
        # Устанавливаем текст для отображения в главном меню приложения
        self.setText('Размер тайла: {0} на {0}'.format(mainWindow.PROXY.SIZE // (4- value)))
        # Делаем кнопку нажимаемой
        self.setCheckable(True)
class TilesizeSwitchers(QActionGroup):
    # Вспомогательный класс, определяющий группу переключателей текущего размера тайла
    def __init__(self, mainWindow, slot):
        # Инициализируем через суперкласс
        super().__init__(mainWindow)
        # Создаем группу действий (в данном случае из двух элементов)
        actions = (SetTilesizeAction(mainWindow, slot, 1),
                   SetTilesizeAction(mainWindow, slot, 2),
                   SetTilesizeAction(mainWindow, slot, 3))
        # Назначем активным по умолчанию последнее действие
        actions[-1].setChecked(True)
        # Подключаем действия к общей группе
        for action in actions:	self.addAction(action)
        # Делаем возможным выбор только одного из действий в группе
        self.setExclusive(True)
#======== Настройка действий по выбору активного слоя========
class SetLayerAction(AbstractAction):
    # Класс действий по смене текущего активного слоя
    def __init__(self, mainWindow, slot, value):
        # Инициализируем через суперкласс
        super().__init__(mainWindow, slot, value)
        # Назначаем иконки
        icon = QIcon()
        icon.addPixmap(QPixmap("RTL\\Images\\Icons\\{}.png".format(value)))	# Иконка в неактивном состоянии
        icon.addPixmap(QPixmap("RTL\\Images\\Icons\\{}A.png".format(value)), QIcon.Normal, QIcon.On)	# Иконка в активном состоянии
        self.setIcon(icon)
        # Устанавливаем текст для отображения в главном меню приложения
        self.setText('Активный слой: {}'.format(value))
        # Делаем кнопку нажимаемой
        self.setCheckable(True)
        # Назначаем комбинацию кнопок (Ctrl + цифра, соответствующая нужному слою)
        self.setShortcut(QKeySequence('Ctrl+{}'.format(value)))
class LayerSwitchers(QActionGroup):
    # Вспомогательный класс, определяющий группу переключателей текущего активного слоя
    def __init__(self, mainWindow, slot):
        # Инициализируем через суперкласс
        super().__init__(mainWindow)
        # Создаем группу действий (в данном случае из четырех элементов)
        actions = (SetLayerAction(mainWindow, slot, 1),
                   SetLayerAction(mainWindow, slot, 2),
                   SetLayerAction(mainWindow, slot, 3),
                   SetLayerAction(mainWindow, slot, 4))
        # Назначем активным по умолчанию первое действие
        actions[0].setChecked(True)
        # Подключаем действия к общей группе
        for action in actions:	self.addAction(action)
        # Делаем возможным выбор только одного из действий в группе
        self.setExclusive(True)
#======== Настройка действий по выбору типа отображения слоев ========
class SetLayersVisibility(AbstractAction):
    # Класс действий по смене отображения слоев сцены
    def __init__(self, mainWindow, slot, value):
        # Инициализируем через суперкласс
        super().__init__(mainWindow, slot, value)
        icon = QIcon()
        icon.addPixmap(QPixmap("RTL\\Images\\Icons\\mode{}.png".format(value)))	# Иконка в неактивном состоянии
        icon.addPixmap(QPixmap("RTL\\Images\\Icons\\mode{}A.png".format(value)), QIcon.Normal, QIcon.On)	# Иконка в активном состоянии
        self.setIcon(icon)
        # Устанавливаем текст для отображения в главном меню приложения
        text = ''
        if value == 'W':    text = 'Режим полного отображения сцены'
        elif value == 'A':  text = 'Режим отображения только активного слоя'
        elif value == 'T':  text = 'Режим частичного отображения неактивных слоев'
        self.setText(text)
        # Делаем кнопку нажимаемой
        self.setCheckable(True)
class LayersVisibilitySwitchers(QActionGroup):
    # Вспомогательный класс, определяющий группу переключателей режима отображения слоев сцены
    def __init__(self, mainWindow, slot):
        # Инициализируем через суперкласс
        super().__init__(mainWindow)
        # Создаем группу действий (в данном случае из трех элементов)
        actions = (SetLayersVisibility(mainWindow, slot, 'W'),
                   SetLayersVisibility(mainWindow, slot, 'T'),
                   SetLayersVisibility(mainWindow, slot, 'A'))
        # Назначем активным по умолчанию первое действие
        actions[0].setChecked(True)
        # Подключаем действия к общей группе
        for action in actions:	self.addAction(action)
        # Делаем возможным выбор только одного из действий в группе
        self.setExclusive(True)
#======== Настройка ползунка масштабирования сцены========
class ViewScaler(QSlider):
    # Виджет изменения масштаба отображения сцены
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        self.PROXY = self.mainWindow.PROXY
        super().__init__()
        self.setRange(0,4); self.setValue(3)
        self.setFixedWidth(40)   # Фиксируем ширину зумера
        self.setOrientation(Qt.Horizontal)   # Располагаем зумер горизонтально
        self.properToolTipText()
        self.valueChanged.connect(self.PROXY.setScaleMode, self.value())
        self.valueChanged.connect(self.mainWindow.SCENE_MANAGER.scaleChange)
        self.valueChanged.connect(self.properToolTipText)
    def properToolTipText(self):
        self.setToolTip('Текущий масштаб: {}:1'.format([0.25, 0.5, 1, 2, 4][self.PROXY.SCALE]))
#======== Настройка действия отрисовки вспомогательной сетки========
class DrawGridAction(AbstractAction):
    # Класс действия переключения режима отрисовки сетки
    def __init__(self, mainWindow):
        # Инициализируем через суперкласс
        super().__init__(mainWindow, mainWindow.PROXY.switchDrawGrid)
        # Назначаем иконки
        icon = QIcon()
        icon.addPixmap(QPixmap("RTL\\Images\\Icons\\grid.png"))	# Иконка в неактивном состоянии
        icon.addPixmap(QPixmap("RTL\\Images\\Icons\\gridA.png"), QIcon.Normal, QIcon.On)	# Иконка в активном состоянии
        self.setIcon(icon)
        # Устанавливаем текст для отображения в главном меню прилоения
        self.setText('Отрисовка вспомогательной сетки вкл/выкл')
        # Делаем кнопку нажимаемой
        self.setCheckable(True)
        # Фиксируем состояние кнопки в зависимости от текущего режима выбранной сцены
        self.setChecked(mainWindow.PROXY.DRAW_GRID)
        # Назначаем комбинацию клавиш для переключения режима
        self.setShortcut(QKeySequence('Ctrl+G'))
#======== Настройка действия отрисовки карты проходимости сцены========
class DrawPassAction(AbstractAction):
    # Класс действия переключения режима отрисовки проходимости
    def __init__(self, mainWindow):
        # Инициализируем через суперкласс
        super().__init__(mainWindow, mainWindow.PROXY.switchViewMode)
        # Назначаем иконки
        icon = QIcon()
        icon.addPixmap(QPixmap("RTL\\Images\\Icons\\pass.png"))	# Иконка в неактивном состоянии
        icon.addPixmap(QPixmap("RTL\\Images\\Icons\\passA.png"), QIcon.Normal, QIcon.On)	# Иконка в активном состоянии
        self.setIcon(icon)
        # Устанавливаем текст для отображения в главном меню приложения
        self.setText('Отрисовка карты проходимости вкл/выкл')
        # Делаем кнопку нажимаемой
        self.setCheckable(True)
        # Фиксируем состояние кнопки в зависимости от текущего режима выбранной сцены
        self.setChecked(mainWindow.PROXY.VIEW_MODE == 'Passability')
        # Назначаем комбинацию клавиш для переключения режима
        self.setShortcut( QKeySequence('Ctrl+P'))
#======== Настройка основных действий с проектом ========
class QuitAction(AbstractAction):
    def __init__(self, mainWindow):
        super().__init__(mainWindow, mainWindow.quitProgram)
        # Назначаем иконку
        icon = QIcon()
        icon.addPixmap(QPixmap("RTL\\Images\\Icons\\exit.png"))
        self.setIcon(icon)
        self.setText('Выход')
        self.setShortcut('Ctrl+Q')
class SaveProjectAction(AbstractAction):
    def __init__(self, mainWindow):
        super().__init__(mainWindow, mainWindow.projectSave)
        # Назначаем иконку
        icon = QIcon()
        icon.addPixmap(QPixmap("RTL\\Images\\Icons\\save.png"))
        self.setIcon(icon)
        self.setText('Сохранить проект')
        self.setShortcut('Ctrl+S')
class OpenProjectAction(AbstractAction):
    def __init__(self, mainWindow):
        super().__init__(mainWindow, mainWindow.projectLoad)
        # Назначаем иконку
        icon = QIcon()
        icon.addPixmap(QPixmap("RTL\\Images\\Icons\\load.png"))
        self.setIcon(icon)
        self.setText('Открыть проект')
        self.setShortcut('Ctrl+O')
class NewProjectAction(AbstractAction):
    def __init__(self, mainWindow):
        super().__init__(mainWindow, mainWindow.projectCreate)
        # Назначаем иконку
        icon = QIcon()
        icon.addPixmap(QPixmap("RTL\\Images\\Icons\\new.png"))
        self.setIcon(icon)
        self.setText('Создать проект')
        self.setShortcut('Ctrl+N')
#======== Настройка действий UNDO и REDO ========
class UndoAction(AbstractAction):
    def __init__(self, mainWindow):
        super().__init__(mainWindow, mainWindow.SCENE_MANAGER.setPreviousScene)
        icon = QIcon()
        icon.addPixmap(QPixmap("RTL\\Images\\Icons\\undo.png"))
        self.setIcon(icon)
        self.setText('Отменить последнее изменение')
        self.setShortcut(QKeySequence.Undo)
class RedoAction(AbstractAction):
    def __init__(self, mainWindow):
        super().__init__(mainWindow, mainWindow.SCENE_MANAGER.setFutureScene)
        icon = QIcon()
        icon.addPixmap(QPixmap("RTL\\Images\\Icons\\redo.png"))
        self.setIcon(icon)
        self.setText('Повторить последнее изменение')
        self.setShortcut(QKeySequence.Redo)