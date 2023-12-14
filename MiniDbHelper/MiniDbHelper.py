from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget,
    QLabel, QFormLayout, QLineEdit, QWidget,
    QPushButton, QHBoxLayout, QMessageBox,
    QVBoxLayout, QMessageBox, QGroupBox,
    QCheckBox, QDoubleSpinBox
)
from PySide6.QtGui import QIcon
import sys
from collections.abc import Callable


BoolFalseStr = ["0", "FALSE", "NONE", "N", "NO", "NEGATIVE", "NOPE", "NAN", "NINE", "НЕТ", "Н", "ЛОЖЬ"]


class Layout():
    def __init__(self, title : str,
                 fields : dict,
                 btn_add_name : str = "Add",
                 btn_del_name : str = "Delete",
                 on_add : Callable = lambda vals: vals,
                 on_del : Callable = lambda vals: True,
                 validator: Callable = None,
                 initial_data : list = None):
        self.title = title
        self.fields = fields
        self.btn_add_name = btn_add_name
        self.btn_del_name = btn_del_name
        self.on_add = on_add
        self.on_del = on_del
        self.validator = validator
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
        
        for title, _type in zip(l.fields.keys(), l.fields.values()):
            label = QLabel(title)
            _input = self.__getInputFieldByType(_type, None, False)
            inputs.append(_input)
            formLayout.addRow(label, _input)
        
        '''=================================================
        Buttons
        ================================================='''
        
        btnLayout = QHBoxLayout()
        
        subLayout.addLayout(btnLayout)
        
        btnAdd = QPushButton(text=l.btn_add_name)
        btnAdd.clicked.connect(lambda state: self.__addDataFromInputsToGrid(inputs, l.fields, grid, l.on_add, l.validator))
        btnLayout.addWidget(btnAdd)
        btnDel = QPushButton(text=l.btn_del_name)
        btnDel.clicked.connect(lambda state: self.__deleteRowFromGrid(inputs, grid, l.on_del))
        btnLayout.addWidget(btnDel)


    def __getInputFieldByType(self, _type: str, val, isDisabled: bool) -> QWidget:
        _input = None
        
        if "bool" in _type:
            _input = QCheckBox()
            if val:
                _input.setChecked(val)
        elif "int" in _type:
            _input = QDoubleSpinBox()
            _input.setDecimals(0)
            _input.setRange(-9223372036854775808, 9223372036854775807)
            if val:
                _input.setValue(val)
        elif "unsigned" in _type:
            _input = QDoubleSpinBox()
            _input.setDecimals(0)
            _input.setMaximum(9223372036854775807)
            if val:
                _input.setValue(val)
        else:
            _input = QLineEdit()
            if val:
                _input.setText(val)
            
        _input.setEnabled(not(isDisabled))
        
        return _input
            

    def __clearInputs(self, inputs, fields:dict) -> None:
        for inpt, _type in zip(inputs, fields.values()):
            if "bool" in _type:
                inpt.setChecked(False)
            else:
                inpt.clear()


    def __inputsNotEmpty(self, inputs: list, fields: dict) -> bool:
        for input, title, type in zip(inputs, fields.keys(), fields.values()):
            if type == "bool":
                continue
            
            if not input.text().strip():
                QMessageBox.critical(self.window(), 'Error', 'Please enter ' + title)
                input.setFocus()
                return False
            
        return True


    def __addDataFromInputsToGrid(self, inputs: list, fields: dict, grid: QTableWidget, on_add: Callable, validator: Callable) -> None:
        if not validator:
            if not self.__inputsNotEmpty(inputs, fields):
                return False
        else:
            err_str = validator(inputs, fields)
            if err_str != "~OK":
                QMessageBox.critical(self.window, 'Error', err_str)
        
        row = grid.rowCount()        
        self.__addRowWithDataToGrid(grid, fields, on_add(self.__getValsFromInput(inputs, fields)))
        self.__clearInputs(inputs, fields)


    def __deleteRowFromGrid(self, vals, grid, on_del) -> None:
        current_row = grid.currentRow()
        
        if not on_del(vals):
            return QMessageBox.warning(self, 'Error','Prohibited')
        
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


    def __populateGrid(self, grid: QTableWidget, fields: dict, initial_data: list) -> None:
        vals = self.__convertToVals(initial_data, fields)
        _start = 0
        _end = len(vals) + 1
        _step = len(fields)
        
        for __start, __end in zip(range(_start, _end, _step), range(_step, _end, _step)):
            self.__addRowWithDataToGrid(grid, fields, vals[__start:__end])


    def __addRowWithDataToGrid(self, grid: QTableWidget, fields: dict, vals: list) -> None:
        row = grid.rowCount()
        grid.insertRow(row)
        for _type, val, col in zip(fields.values(), vals, range(len(fields))):
            grid.setCellWidget(row, col, self.__getInputFieldByType(_type, val, True))
    
    
    def __getValsFromInput(self, inputs: list[QWidget], fields: dict) -> list:
        vals = list()
        
        for input, _type in zip(inputs, fields.values()):
            if "bool" in _type:
                vals.append(input.isChecked())
            if "unsigned" in _type or "int" in _type:
                vals.append(input.value())
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
            elif "unsigned"in fields[keys[i%len(fields)]] or "int" in fields[keys[i%len(fields)]]:
                vals.append(float(value))
            else:
                vals.append(value)
                
            if i <= len(data):
                i += 1
            else:
                break

        return vals


if (__name__ == "__main__"):

    app = QApplication(sys.argv)
    
    def truefalse(vals: list) -> list:
        _vals = list()
        
        for val in vals:
            if val is True:
                _vals.append(False)
            else:
                _vals.append(val)
                
        return _vals
        
    window = MiniDbHelper("Sells",
                          Layout(title="Primary",
                                 fields={"id" : "int", "summ": "int", "priority": "unsigned"},
                                 initial_data=["1", "2", "3", "4", "5", "6"]),
                          Layout(title="Notes",
                                 initial_data=["1", "2", "3", "0"],
                                 #on_add=truefalse,
                                 fields={"Name": "", "Checked": "bool"}))
    
    window.show()
    
    sys.exit(app.exec())