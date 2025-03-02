from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTreeView, QListWidget, QTextEdit, QSplitter, QTableWidget, QTableWidgetItem
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PySide6 massCode Clone")
        self.setGeometry(100, 100, 1000, 600)

        # 创建主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # 水平分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # 左侧文件夹视图
        self.folder_view = QTreeView()
        splitter.addWidget(self.folder_view)

        # 中间列表
        self.list_view = QListWidget()
        self.list_view.addItem("123")
        self.list_view.addItem("hello world~")
        splitter.addWidget(self.list_view)

        # 右侧文本编辑或表格
        self.text_edit = QTextEdit()
        self.table_view = QTableWidget(5, 3)  # 5 行 3 列
        self.table_view.setHorizontalHeaderLabels(["Fragment 1", "Fragment 2", "Fragment 3"])
        self.table_view.setItem(0, 0, QTableWidgetItem("1"))

        # 垂直布局让用户切换
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.table_view)
        right_layout.addWidget(self.text_edit)
        right_widget = QWidget()
        right_widget.setLayout(right_layout)
        splitter.addWidget(right_widget)

        # 主布局
        layout = QHBoxLayout()
        layout.addWidget(splitter)
        main_widget.setLayout(layout)

        # 工具栏
        toolbar = self.addToolBar("Tools")
        new_action = QAction("New", self)
        toolbar.addAction(new_action)

        # 状态栏
        self.statusBar().showMessage("Ready")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
