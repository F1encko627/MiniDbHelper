# MiniDbHelper
> Python module for quick building minimalistic interface for database.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Install
Just clone or download...
```
pip3 install -r requirements.txt
```

# Usage example
```Python
from MiniDbHelper import MiniDbHelper, Layout
from PySide6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)

window = MiniDbHelper("Sells",
                      Layout(title="Primary",
                             fields=["Sell-id", "Product-id", "Summ"],
                             initial_data=["1", "2", "3", "4", "5", "6"]),
                      Layout(title="Notes",
                             fields=["Name", "Checked"]))

window.show()
sys.exit(app.exec())
```
## Result
![image](https://github.com/F1encko627/MiniDbHelper/assets/46199406/18d09420-b5b0-4bbe-ab2d-b05798972a8c)
