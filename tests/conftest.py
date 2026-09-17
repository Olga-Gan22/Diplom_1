import sys
import os

# Добавляем корень проекта (на два уровня вверх от папки tests) в путь поиска модулей
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
