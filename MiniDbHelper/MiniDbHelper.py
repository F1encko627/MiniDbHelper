from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, 
    QTableWidgetItem, QLabel, QFormLayout, 
    QLineEdit, QWidget, QPushButton, QHBoxLayout, 
    QMessageBox, QVBoxLayout, QMessageBox, QGroupBox
)
from PySide6.QtGui import QIcon
import sys
from collections.abc import Callable

class Layout():

    def __init__(self, title : str,
                 fields : list[str],
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
        
    def __init__(self, windowTitle : str, *layout : Layout):        
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
            self.addData(l)
            
        self.setCentralWidget(main)
        self.setWindowIcon(QIcon('res/ico.png'))
    
    
    def addData(self, l : Layout):
        
        def __reset():
            for inpt in inputs:
                inpt.clear()
        
        def __valid():
            for index, input in enumerate(inputs):
                if not input.text().strip():
                    QMessageBox.critical(self, 'Error', 'Please enter ' + l.fields[index])
                    input.setFocus()
                    return False
                
            return True
        
        def __add():
            if not __valid():
                return
            
            if not l.on_add([inpt.text() for inpt in inputs]):
                QMessageBox.critical(self, 'Error', 'btn_add_action error')
                return False
            
            row = grid.rowCount()
            grid.insertRow(row)
            
            column = len(inputs)
            
            for input in inputs:
                grid.setItem(row - 1, column, QTableWidgetItem(input.text()))
                column += 1
                
            __reset()
        
        
        def __del():
            current_row = grid.currentRow()
            
            if not l.on_del([inpt.text() for inpt in inputs]):
                QMessageBox.critical(self, 'Error', 'btn_del_action error')
                return False
            
            if current_row < 0:
                return QMessageBox.warning(self, 'Warning','Please select a record to delete')

            button = QMessageBox.question(
                self,
                'Confirmation',
                'Are you sure that you want to delete the selected row?',
                QMessageBox.StandardButton.Yes |
                QMessageBox.StandardButton.No
            )
            if button == QMessageBox.StandardButton.Yes:
                grid.removeRow(current_row)
        
        
        def __populateGrid():
            grid.setRowCount((int)(len(l.initial_data) / len(l.fields)))
            
            for row in range(0, (int)(len(l.initial_data) / len(l.fields))):            
                for column in range(0, len(l.fields)):
                    grid.setItem(row, column, QTableWidgetItem(l.initial_data[row * len(l.fields) + column]))
        
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
            __populateGrid()
        
        formLayout = QFormLayout()
        
        subLayout.addLayout(formLayout)
        
        inputs = list()
        
        for field in l.fields:
            label = QLabel(field)
            input = QLineEdit()
            inputs.append(input)
            
            formLayout.addRow(label, input)
        
        '''=================================================
        Buttons
        ================================================='''
        
        btnLayout = QHBoxLayout()
        
        subLayout.addLayout(btnLayout)
        
        btnAdd = QPushButton(text=l.btn_add_name)
        btnAdd.clicked.connect(__add)
        btnLayout.addWidget(btnAdd)
        btnDel = QPushButton(text=l.btn_del_name)
        btnDel.clicked.connect(__del)
        btnLayout.addWidget(btnDel)
    
             
                    
if (__name__ == "__main__"):
    app = QApplication(sys.argv)
    
    with open("darkeum.qss","r") as file:
        app.setStyleSheet(file.read())
    
    window = MiniDbHelper("Sells",
                          Layout(title="Primary",
                                 fields=["Sell-id", "Product-id", "Summ"],
                                 initial_data=["1", "2", "3", "4", "5", "6"]),
                          Layout(title="Notes",
                                 fields=["Name", "Checked"]))
    
    window.show()
    
    print(app.allWidgets())
    
    sys.exit(app.exec())