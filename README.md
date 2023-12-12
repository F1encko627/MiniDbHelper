# MiniDbHelper

> Python module for quick building minimalistic interface for database.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

# Install

Just clone or download...

```
pip3 install -r requirements.txt
```

# Usage example

```Python
from MiniDbHelper.MiniDbHelper import MiniDbHelper, Layout
from PySide6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)

window = MiniDbHelper("Sells",
                      Layout(title="Primary",
                             fields={"id" : "int", "summ": "int", "priority": "short"},
                             initial_data=["1", "2", "3", "4", "5", "6"]),
                      Layout(title="Notes",
                             initial_data=["1", "2", "3", "0"],
                             fields={"Name": "", "Checked": "bool"}))

window.show()
sys.exit(app.exec())
```

## Result

![image](./assets/result.png)

# Input

```Python
data = {"Field Name": "type", "Another Field": "type"} #Dictionary
```

Supported types:
- "str" -> (QLineEdit)
- "int" -> (QLineEdit)
- "unsigned" -> (QSpinBox)
- "bool" -> (QCheckBox)

+ not specified -> "str"

# on_add() & on_delete() | TO-DO

Optional methods to check/process data when user clicks add/delete button

```Python
def on_add(*args) -> dict:
    ...
    return kwargs
```

Default: no action

# validator() | TO-DO

Optional method to control user input

```Python
def validator(*args) -> str:
    if some_error:
       return "Error text" #To show to user

    return "" #Just continue
```

Default: just checks if all input fields are not empty.

# TO-DO

- Окно должно быть готово к использованию сразу после создания экземпляра класса;
- Сквозная передача данных через подключаемые обработчики для модификации (например генерация ID);
- Хранить словари элементов чтобы можно было обращаться к ключевым позициям для их модификации или независимого получения данных;
- Полностью адаптивный интерфейс. Либо через QDockWidget либо через разделители для изменения размелов;
- Адаптация полей отображения-ввода под тип данных (задавать через словарь field-type при конфигурировании);
- Импорт/Экспорт данных CSV/Excel/...;
- Кастомные валидаторы;
- Возможность скрывать поля ввода для пользователя.