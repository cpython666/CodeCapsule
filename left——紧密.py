from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QStackedWidget
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFontMetrics, QFont


class FolderBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)

        # 主布局
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 顶部切换按钮
        self.btn_library = QPushButton("库")
        self.btn_library.setCheckable(True)
        self.btn_library.setChecked(True)
        self.btn_tags = QPushButton("标签")
        self.btn_tags.setCheckable(True)

        # 水平布局存放切换按钮
        toggle_layout = QHBoxLayout()
        toggle_layout.setContentsMargins(0, 0, 0, 0)
        toggle_layout.setSpacing(0)
        toggle_layout.addWidget(self.btn_library)
        toggle_layout.addWidget(self.btn_tags)

        # StackedWidget 作为主导航区域
        self.stack = QStackedWidget()

        # Library 视图
        self.library_list = QListWidget()
        self.library_list.addItems(["📥 Inbox", "⭐ Favorites", "📂 All Snippets", "🗑 Trash"])
        self.library_list.setSpacing(0)

        # 设置 library_list 高度刚好适应内容
        item_count = self.library_list.count()  # 列表项数量
        item_height = self.library_list.sizeHintForRow(0)  # 每项高度
        total_height = item_height * item_count + 2  # 加上微小的边框调整
        self.library_list.setFixedHeight(total_height)

        # Folders 视图
        self.folder_list = QListWidget()
        self.folder_list.addItems(["📁 Default", "📁 Vue", "📁 Untitled folder", "📁 Untitled folder"])
        self.folder_list.setSpacing(0)

        # Library 界面
        library_widget = QWidget()
        library_layout = QVBoxLayout()
        library_layout.setContentsMargins(5,5,5,5)
        library_layout.setSpacing(0)
        library_layout.addWidget(self.library_list)
        library_layout.addWidget(self.folder_list)
        library_widget.setLayout(library_layout)

        # Tags 界面
        tags_widget = QListWidget()
        tags_widget.addItems(["🏷️ Tag 1", "🏷️ Tag 2", "🏷️ Tag 3"])
        tags_widget.setSpacing(0)

        # 添加到 QStackedWidget
        self.stack.addWidget(library_widget)
        self.stack.addWidget(tags_widget)

        # 绑定按钮切换事件
        self.btn_library.clicked.connect(lambda: self.switch_view(0))
        self.btn_tags.clicked.connect(lambda: self.switch_view(1))

        # 添加到主布局
        layout.addLayout(toggle_layout)
        layout.addWidget(self.stack)

        # 设置布局比例
        layout.setStretch(0, 0)  # toggle_layout 不拉伸
        layout.setStretch(1, 1)  # stack 占满剩余空间

        # 确保 folder_list 拉伸
        library_layout.setStretch(0, 0)  # library_list 不拉伸
        library_layout.setStretch(1, 1)  # folder_list 拉伸

        self.setLayout(layout)

    def switch_view(self, index):
        self.stack.setCurrentIndex(index)
        self.btn_library.setChecked(index == 0)
        self.btn_tags.setChecked(index == 1)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sidebar Example")
        self.setContentsMargins(0, 0, 0, 0)
        self.setGeometry(100, 100, 150, 500)

        self.sidebar = FolderBar()
        self.setCentralWidget(self.sidebar)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()