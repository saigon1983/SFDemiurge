'''
В этом модуле описываются пункты меню, вызываемого для элементов структуры проекта
'''
from RTL.Libs.projectManager.project_dialogs import *

class PMAction(QAction):
    # Абстрактный класс, являющийся предком всех специализированных действий меню
    def __init__(self, menu, name):
        '''
        Конструктор приниает следующие аргументы:
            menu - ссылка на родительское меню, в котором находится действие
            name - имя действия (название строки в меню)
        '''
        self.callingItem    = menu.callingItem      # Ссылка на вызывающий элемент
        self.parentMenu     = menu                  # Ссылка на родительское меню
        self.selectorWindow = menu.selectorWindow   # Ссылка на виджет редактирвоания проекта
        super().__init__(name, menu)                # Конструктор суперкласса
        self.triggered.connect(self.doAction)       # Связываем сигнал выбора с методом действия
    def doAction(self):
        # Метод реакции на выбор текущего дейтсвия. Должен быть перегружен в подклассе
        print('This method must be overloaded in a subclass {}!'.format(type(self)))
# ========== Далее следуют определния классов, каждый из которых отвечает за одно конкретное действие ==========
class PMAction_AddGroup(PMAction):
    # Действие по добавлению новой группы в структуру
    def __init__(self, menu):
        super().__init__(menu, 'Создать новую группу')
    def doAction(self):
        # Переопределяем метод действия
        dialog = Dialog_NewGroup(self.parentMenu)
        dialog.exec()

class PMAction_AddScene(PMAction):
    # Действие по добавлению новой группы в структуру
    def __init__(self, menu):
        super().__init__(menu, 'Создать новую сцену')
    def doAction(self):
        # Переопределяем метод действия
        dialog = Dialog_NewScene(self.parentMenu)
        dialog.exec()