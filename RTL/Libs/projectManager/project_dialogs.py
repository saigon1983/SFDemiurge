'''
В этом модуле описаны все диалоговые окна, которые могут вызываться из действий меню элементов структуры проекта
'''
from PyQt4.QtGui import *
from PyQt4.QtCore  import *

class Dialog_NewGroup(QDialog):
    # Виджет создания новой группы в структуре проекта
    def __init__(self, menu):
        super().__init__(menu)              # Конструктор суперкласса
        self.setWindowTitle('Новая группа') # Заголовок окна
        self.parentMenu = menu              # Ссылка на родительское меню
        self.callingItem = menu.callingItem # Ссылка на вызывающий элемент
        self.setButtons()                   # Настраиваем кнопки виджета
        self.setFields()                    # Настраиваем поля виджета
        self.setLayouts()                   # Настраиваем расположение элементов в виджете
        self.validateInputs()               # Проверяем валидацию ввода
    def setButtons(self):
        # Метод настройки кнопок управления виджета. Представляет из себя стандратные кнопки Ok|Cancel
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
    def setFields(self):
        # Метод настройки полей виджета. По умолчанию именем новой группы является следующий ее порядковый номер
        self.groupName = QLineEdit()                            # Создаем поле ввода названия группы
        self.groupName.setText('Group GR' + str(self.callingItem.root.groupsCounter + 1).zfill(4))
        self.groupName.textChanged.connect(self.validateInputs) # Соединяем сигнал изменения текста с методом валидации
    def setLayouts(self):
        # Метод размещения элементов по виджету
        mainLayout = QVBoxLayout(self)                          # Создаем компоновщик
        mainLayout.addWidget(QLabel('Введите название группы:'))# Создаем поле описания действия
        mainLayout.addWidget(self.groupName)                    # Размещаем поле ввода
        mainLayout.addWidget(self.buttons)                      # Размещаем кнопки
    def validateInputs(self):
        # Метод проверки валидации. Текстовое поле должно содержать текст и этот текст не должен ранее использоваться
        # для названия группы
        if self.groupName.text() and self.groupName.text() not in self.callingItem.root.usedGroupNames:
            self.buttons.buttons()[0].setDisabled(False)
        else:
            self.buttons.buttons()[0].setDisabled(True)
    def accept(self):
        # Переопределяем метод подтверждения действия
        super().accept()                                    # Передаем подтверждение суперклассу
        self.callingItem.addNewGroup(self.groupName.text()) # Создаем новую группу в вызывающем элементе

class Dialog_NewScene(QDialog):
    # Виджет создания новой сцены в структуре проекта
    # Список наименований полей
    LABELNAMES = ['Идентификатор:','Название:','Ширина (в клетках):','Высота (в клетках):','Базовый тайлсет:']
    def __init__(self, menu):
        super().__init__(menu)              # Конструктор суперкласса
        self.setWindowTitle('Новая сцена')  # Заголовок окна
        self.parentMenu = menu              # Ссылка на родительское меню
        self.callingItem = menu.callingItem # Ссылка на вызывающий элемент
        self.setButtons()                   # Настраиваем кнопки виджета
        self.setFields()                    # Настраиваем поля виджета
        self.setLayouts()                   # Настраиваем расположение элементов в виджете
    def setButtons(self):
        # Метод настройки кнопок управления виджета. Представляет из себя стандратные кнопки Ok|Cancel
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
    def setFields(self):
        # Метод настройки полей виджета
        self.setIDField()
        self.setNameField()
        self.setSizeFields()
        self.setTilesetField()
        self.fields = (self.sceneID, self.sceneName, self.sceneWidth, self.sceneHeight, self.sceneTileset)
        self.validateInputs()
    def setLayouts(self):
        # Метод размещения элементов в виджете
        self.mainVLayout = QVBoxLayout(self)	# Основная внешняя зона
        for i in range(6):
            HLayout = QHBoxLayout()                             # Вспомогательный горизонатльный компоновщик
            if i == 5:
                HLayout.addWidget(self.buttons)                 # Размещаем кнопки
            else:
                label = QLabel(Dialog_NewScene.LABELNAMES[i])   # Наименование поля
                label.setFixedWidth(105)                        # Фиксируем ширину поля
                HLayout.addWidget(label)                        # Размещаем поле в компоновщике
                HLayout.addStretch(1)                           # Добавляем пустоту
                HLayout.addWidget(self.fields[i])               # Добавляем сам виджет поля
            self.mainVLayout.addLayout(HLayout)                 # Совмещаем компоновщики
    def validateInputs(self):
        # Создание сцены возможно только если: ширина и высота равны 5 или более (до 999), имя сцены не пустое и такого
        # имени еще нет в списке имен сцен
        if int(self.sceneWidth.text()) >= 5 and int(self.sceneHeight.text()) >= 5 and \
            self.sceneName.text() and self.sceneName.text() not in self.callingItem.rootItem.usedSceneNames:
            self.buttons.buttons()[0].setDisabled(False)
        else:
            self.buttons.buttons()[0].setDisabled(True)
    def setIDField(self):
        # Метод настройки поля отображения ID создаваемой сцены
        self.sceneID = QLabel('EL' + str(self.callingItem.element.root.ElementCounter).zfill(4))
    def setNameField(self):
        # Метод настройки поля ввода названия сцены. По умолчанию предлагается название соответствующее порядковому номеру
        self.sceneName = QLineEdit()                                # Создаем поле ввода названия сцены
        self.sceneName.setText('Scene AR' + str(self.callingItem.rootItem.scenesCounter + 1).zfill(4))
        self.sceneName.textChanged.connect(self.validateInputs)     # Соединяем сигнал изменения текста с методом валидации
        self.sceneName.setAlignment(Qt.AlignVCenter | Qt.AlignRight)# Выравниваем текст по вертикали и правому краю
    def setSizeFields(self):
        # Метод настройки полей ввода ширины и высоты сцены
        self.sceneWidth = QLineEdit()                   # Поле ширины
        self.sceneHeight = QLineEdit()                  # Поле высоты
        sizeFields = (self.sceneWidth, self.sceneHeight)# Помещаем поля в кортеж для более быстрой обработки
        for field in sizeFields:
            field.setAlignment(Qt.AlignVCenter | Qt.AlignRight) # Выравниваем текст по вертикали и правому краю
            field.setFixedWidth(25)                             # Задаем фиксированную ширину поля
            field.setValidator(QIntValidator())                 # Допускаем ввод только цифровых значений
            field.setMaxLength(3)                               # Ограничиваем ввод только трех цифр
            field.setText('5')                                  # Ставим по умолчанию минимальное значение, равное 5
            field.textChanged.connect(self.validateInputs)      # Соединяем сигнал изменения текста с методом валидации
    def setTilesetField(self):
        # Метод настройки поля выбора базового тайлсета
        self.sceneTileset = QComboBox()                                             # Создаем выпадающий список
        tilesets = self.callingItem.mainWindow.TILESET_SELECTOR.tilesetData.NAMES   # Получаем список имен тайлсетов
        self.sceneTileset.addItems(tilesets)                                        # Заполняем ими выпадающий список
    def accept(self):
        # Переопределяем метод подтверждения действия
        super().accept()                        # Передаем подтверждение суперклассу
        # Создаем объект данных сцены, исходя из заданных значений полей
        sceneData = {'Name': self.sceneName.text(),
                     'Width': int(self.sceneWidth.text()),
                     'Height': int(self.sceneHeight.text()),
                     'MainTileset': self.sceneTileset.currentText()}
        self.callingItem.addNewScene(sceneData) # Создаем новую сцену в вызывающем элементе