from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QStackedWidget
)
from PySide6.QtCore import Qt

class FolderBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0,0,0,0)

        layout = QVBoxLayout()
        # 顶部切换按钮
        self.btn_library = QPushButton("库")
        self.btn_library.setCheckable(True)
        self.btn_library.setChecked(True)
        self.btn_tags = QPushButton("标签")
        self.btn_tags.setCheckable(True)
        # 水平布局存放切换按钮
        toggle_layout = QHBoxLayout()
        toggle_layout.addWidget(self.btn_library)
        toggle_layout.addWidget(self.btn_tags)

        # StackedWidget 作为主导航区域
        self.stack = QStackedWidget()

        # Library 视图
        self.library_list = QListWidget()
        self.library_list.addItems(["📥 Inbox", "⭐ Favorites", "📂 All Snippets", "🗑 Trash"])

        # Folders 视图
        self.folder_list = QListWidget()
        self.folder_list.addItems(["📁 Default", "📁 Vue", "📁 Untitled folder", "📁 Untitled folder"])

        # Library 界面
        library_widget = QWidget()
        library_layout = QVBoxLayout()
        library_layout.addWidget(self.library_list)
        library_layout.addWidget(QPushButton('+'))
        library_layout.addWidget(self.folder_list)
        library_widget.setLayout(library_layout)

        # Tags 界面（可以改成不同的内容）
        tags_widget = QListWidget()
        tags_widget.addItems(["🏷️ Tag 1", "🏷️ Tag 2", "🏷️ Tag 3"])

        # 添加到 QStackedWidget
        self.stack.addWidget(library_widget)
        self.stack.addWidget(tags_widget)

        # 绑定按钮切换事件
        self.btn_library.clicked.connect(lambda: self.switch_view(0))
        self.btn_tags.clicked.connect(lambda: self.switch_view(1))

        layout.addLayout(toggle_layout)
        layout.addWidget(self.stack)
        self.setLayout(layout)

    def switch_view(self, index):
        self.stack.setCurrentIndex(index)
        self.btn_library.setChecked(index == 0)
        self.btn_tags.setChecked(index == 1)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sidebar Example")
        # self.setGeometry(100, 100, 300, 500)
        self.setContentsMargins(0,0,0,0)

        self.sidebar = FolderBar()
        self.setCentralWidget(self.sidebar)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
