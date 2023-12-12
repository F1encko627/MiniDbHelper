from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, 
    QTableWidgetItem, QLabel, QFormLayout, 
    QLineEdit, QWidget, QPushButton, QHBoxLayout, 
    QMessageBox, QVBoxLayout, QMessageBox, QGroupBox, QCheckBox, QSpinBox
)
from PySide6.QtGui import QIcon
import sys
from collections.abc import Callable


BoolFalseStr = ["0", "FALSE", "NONE", "N", "NO", "0", "NOPE", "NAN", "NINE", "НЕТ", "Н", "ЛОЖЬ"]


class Layout():
    def __init__(self, title : str,
                 fields : dict,
                 btn_add_name : str = "Add",
                 btn_del_name : str = "Delete",
                 on_add : Callable = lambda x: True,
                 on_del : Callable = lambda y: True,
                 initial_data : list = None):
        self.title = title
        self.fields = fields
        self.btn_add_name = btn_add_name
        self.btn_del_name = btn_del_name
        self.on_add = on_add
        self.on_del = on_del
        self.initial_data = initial_data


class MiniDbHelper(QMainWindow): 
    def __init__(self, windowTitle : str, *layout : Layout) -> None:        
        super().__init__()
        
        self.setGeometry(100, 100, 600, 400)
        
        self.setWindowTitle(windowTitle)
        
        main = QWidget()
        self.mainLayout = QHBoxLayout()
        main.setLayout(self.mainLayout)
        
        self.internals = dict()
        
        self.dbs = 0;
        
        for l in layout:
            self.dbs += 1
            self.NewPanel(l)
            
        self.setCentralWidget(main)
        self.setWindowIcon(QIcon('res/ico.png'))
    
    
    def NewPanel(self, l : Layout) -> None:
        
        '''=================================================
        Group Layout
        ================================================='''
        
        self.internals[l.title] = dict()
        
        groupbox = QGroupBox()
        groupbox.setTitle(l.title)
        self.mainLayout.addWidget(groupbox)
        subLayout = QVBoxLayout()
        groupbox.setLayout(subLayout)
        
        '''=================================================
        Table/Grid
        ================================================='''
        
        grid = QTableWidget()
        grid.setColumnCount(len(l.fields))
        
        subLayout.addWidget(grid)
        
        for column in range(0, len(l.fields) - 1):
            grid.setColumnWidth(column, 100)
        
        grid.setHorizontalHeaderLabels(l.fields)
        
        if (l.initial_data):
            self.__populateGrid(grid, l.fields, l.initial_data)
        
        formLayout = QFormLayout()
        
        subLayout.addLayout(formLayout)
        
        inputs = list()
        
        for title, type in zip(l.fields.keys(), l.fields.values()):
            label = QLabel(title)
            input = None
            
            if "bool" in type:
                input = QCheckBox()
            elif "unsigned" in type:
                input = QSpinBox()
            else:
                input = QLineEdit()
                
            inputs.append(input)
            
            formLayout.addRow(label, input)
        
        '''=================================================
        Buttons
        ================================================='''
        
        btnLayout = QHBoxLayout()
        
        subLayout.addLayout(btnLayout)
        
        btnAdd = QPushButton(text=l.btn_add_name)
        btnAdd.clicked.connect(lambda state: self.__addDataFromInputsToGrid(inputs, l.fields, grid, l.on_add))
        btnLayout.addWidget(btnAdd)
        btnDel = QPushButton(text=l.btn_del_name)
        btnDel.clicked.connect(lambda state: self.__deleteRowFromGrid(inputs, grid, l.on_del))
        btnLayout.addWidget(btnDel)


    def __clearInputs(self, inputs) -> None:
        for inpt in inputs:
            inpt.clear()


    def __inputsNotEmpty(self, inputs, fields: dict) -> bool:
        for input, title, type in zip(inputs, fields.keys(), fields.values()):
            if type == "bool":
                continue
            
            if not input.text().strip():
                QMessageBox.critical(self.window, 'Error', 'Please enter ' + title)
                input.setFocus()
                return False
            
        return True


    def __addDataFromInputsToGrid(self, inputs, fields, grid, on_add) -> None:
        if not self.__inputsNotEmpty(inputs, fields):
            return False
        
        if not on_add([inpt.text() for inpt in inputs]):
            QMessageBox.critical(self, 'Error', 'btn_add_action error')
            return False
        
        row = grid.rowCount()
        grid.insertRow(row)
        
        for type, col in zip(fields.values(), range(len(fields))):
            self.__addRowWithDataToGrid(type, col, row, grid, self.__getValsFromInput(inputs, fields))
            
        self.__clearInputs(inputs)


    def __deleteRowFromGrid(self, inputs, grid, on_del) -> None:
        current_row = grid.currentRow()
        
        if not on_del([inpt.text() for inpt in inputs]):
            QMessageBox.critical(self, 'Error', 'btn_del_action error')
            return False
        
        if current_row < 0:
            return QMessageBox.warning(self, 'Warning','Please select a record to delete')
        button = QMessageBox.question(
            self,
            'Confirmation',
            'Are you sure that you want to delete row ' + str(current_row + 1) + '?',
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
            )
        
        if button == QMessageBox.StandardButton.Yes:
            grid.removeRow(current_row)


    def __populateGrid(self, grid: QTableWidget, fields: dict, initial_data) -> None:
        vals = self.__convertToVals(initial_data, fields)
        _start = 0
        _end = len(vals) + 1
        _step = len(fields)
        
        for __start, __end in zip(range(_start, _end, _step), range(_step, _end, _step)):
            print(vals[__start:__end])
            print(__start, __end)
            self.__addRowWithDataToGrid(grid, fields, vals[__start:__end])


    def __addRowWithDataToGrid(self, grid: QTableWidget, fields, vals) -> None:
        row = grid.rowCount()
        grid.insertRow(row)
        
        for _type, val, col in zip(fields.values(), vals, range(len(fields))):
            if "bool" in _type:
                checkbox = QCheckBox()
                checkbox.setChecked(val)
                grid.setCellWidget(row, col, checkbox)
            if "unsigned" in _type:
                updown = QSpinBox()
                updown.setValue(int(val))
                grid.setCellWidget(row, col, updown)
            else:
                grid.setItem(row, col, QTableWidgetItem(val))
    
    
    def __getValsFromInput(self, inputs: list[QWidget], fields: dict) -> list:
        vals = list()
        
        for input, type in zip(inputs, fields.values()):
            if "bool" in type:
                vals.append(input.isChecked())
            if "unsigned" in type:
                vals.append(str(input.value()))
            else:
                vals.append(str(input.text()))
                
        return vals


    def __convertToVals(self, data: list[str], fields: dict) -> list:
        vals = list()
        keys = list(fields.keys())
        
        i = 0
        
        for value in data:
            if "bool" in fields[keys[i%len(fields)]]:
                if value.capitalize() in BoolFalseStr:
                    vals.append(False)
                else:
                    vals.append(True)
            else:
                vals.append(value)
                
            if i <= len(data):
                i += 1
            else:
                break

        return vals


if (__name__ == "__main__"):

    app = QApplication(sys.argv)
    
    window = MiniDbHelper("Sells",
                          Layout(title="Primary",
                                 fields={"id" : "int", "summ": "int", "priority": "unsigned"},
                                 initial_data=["1", "2", "3", "4", "5", "6"]),
                          Layout(title="Notes",
                                 initial_data=["1", "2", "3", "0"],
                                 fields={"Name": "", "Checked": "bool"}))
    
    window.show()
    
    sys.exit(app.exec())