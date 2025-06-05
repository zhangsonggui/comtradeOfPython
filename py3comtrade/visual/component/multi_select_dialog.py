from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QApplication, QComboBox, QListView, QPushButton, QVBoxLayout, QWidget


class MultiSelectComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)  # 防止手动输入
        self._model = QStandardItemModel()
        self.setModel(self._model)
        self.setView(QListView())
        self.setDuplicatesEnabled(False)

    def set_items(self, items, label_key="name"):
        """
        设置可选项
        :param items: 对象列表或字符串列表
        :param label_key: 如果是对象，显示的字段名
        """
        self._model.clear()
        for item in items:
            if isinstance(item, dict):
                text = item[label_key]
            elif hasattr(item, label_key):
                text = getattr(item, label_key)
            else:
                text = str(item)
            std_item = QStandardItem(text)
            std_item.setCheckable(True)
            std_item.setData(item, Qt.ItemDataRole.UserRole)  # 存储原始对象
            self._model.appendRow(std_item)

    def get_selected_items(self):
        """
        获取选中的原始对象
        """
        selected = []
        for i in range(self._model.rowCount()):
            index = self._model.index(i, 0)
            if self._model.data(index, Qt.ItemDataRole.CheckStateRole) == Qt.CheckState.Checked:
                selected.append(self._model.data(index, Qt.ItemDataRole.UserRole))
        return selected

    def get_selected_labels(self):
        """
        获取选中的文本标签
        """
        selected = []
        for i in range(self._model.rowCount()):
            index = self._model.index(i, 0)
            if self._model.data(index, Qt.ItemDataRole.CheckStateRole) == Qt.CheckState.Checked:
                selected.append(self._model.data(index, Qt.ItemDataRole.DisplayRole))
        return selected


class TestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MultiSelectComboBox 示例")
        layout = QVBoxLayout()

        self.combo_box = MultiSelectComboBox()

        # 模拟数据（可以是任意对象）
        class DataObj:
            def __init__(self, name):
                self.name = name

        data = [DataObj(f"项{i}") for i in range(1, 6)]

        self.combo_box.set_items(data, label_key="name")
        layout.addWidget(self.combo_box)

        btn = QPushButton("获取选中项")
        btn.clicked.connect(self.print_selected)
        layout.addWidget(btn)

        self.setLayout(layout)

    def print_selected(self):
        selected_objs = self.combo_box.get_selected_items()
        selected_names = self.combo_box.get_selected_labels()
        print("选中对象:", selected_objs)
        print("选中名称:", selected_names)


if __name__ == "__main__":
    app = QApplication([])
    win = TestWindow()
    win.show()
    app.exec()
