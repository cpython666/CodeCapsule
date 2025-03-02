import sys
import os
import json
from pathlib import Path
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QListWidget, QStackedWidget, QTextEdit,
    QComboBox, QSplitter, QFormLayout, QFileDialog, QLabel, QScrollArea, QInputDialog
)
from PySide6.QtCore import Qt, QSettings, QFileSystemWatcher
from PySide6.QtGui import QIcon, QFontMetrics, QFont


class SnippetCard(QWidget):
    """自定义代码片段卡片"""
    def __init__(self, filename, mod_time, parent=None):
        super().__init__(parent)
        self.filename = filename
        self.setStyleSheet("""
            QWidget {
                background-color: #F5F5F5;
                border: 1px solid #D3D3D3;
                border-radius: 5px;
                padding: 10px;
                margin: 5px 0;
            }
            QWidget:hover {
                background-color: #E0E0E0;
            }
        """)

        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)

        # 文件名
        filename_label = QLabel(filename)
        filename_label.setStyleSheet("QLabel { font-size: 14px; font-weight: bold; }")
        layout.addWidget(filename_label)

        layout.addStretch()

        # 修改时间
        time_label = QLabel(mod_time)
        time_label.setStyleSheet("QLabel { font-size: 12px; color: #999; }")
        layout.addWidget(time_label)

        self.setLayout(layout)


class FolderBar(QWidget):
    def __init__(self, code_dir, on_folder_changed, on_new_folder):
        super().__init__()
        self.code_dir = code_dir
        self.on_folder_changed = on_folder_changed
        self.on_new_folder = on_new_folder
        self.setContentsMargins(0, 0, 0, 0)

        # 主布局
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(0)

        # 搜索框和“+”按钮
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(5)  # 搜索框和按钮之间的间距
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.setStyleSheet("QLineEdit { padding: 5px; border: 1px solid #D3D3D3; border-radius: 5px; }")
        self.search_bar.setFixedHeight(30)  # 固定高度
        top_layout.addWidget(self.search_bar)

        self.new_folder_button = QPushButton("+")
        self.new_folder_button.clicked.connect(self.create_new_folder)
        self.new_folder_button.setFixedHeight(30)  # 与搜索框高度一致
        self.new_folder_button.setFixedWidth(30)
        self.new_folder_button.setStyleSheet("QPushButton { border-radius: 5px; }")
        top_layout.addWidget(self.new_folder_button)
        layout.addLayout(top_layout)

        # LIBRARY / TAGS 切换按钮
        self.btn_library = QPushButton("库")
        self.btn_library.setCheckable(True)
        self.btn_library.setChecked(True)
        self.btn_tags = QPushButton("标签")
        self.btn_tags.setCheckable(True)

        button_style = """
            QPushButton {
                background-color: white;
                color: black;
                border: none;
                padding: 5px;
                font-size: 14px;
            }
            QPushButton:checked {
                background-color: #007AFF;
                color: white;
            }
            QPushButton:hover:!checked {
                background-color: #E0E0E0;
            }
        """
        self.btn_library.setStyleSheet(button_style)
        self.btn_tags.setStyleSheet(button_style)

        font = QFont()
        font.setPointSize(12)
        self.btn_library.setFont(font)
        self.btn_tags.setFont(font)
        font_metrics = QFontMetrics(font)
        button_height = font_metrics.height() + 14
        self.btn_library.setFixedHeight(button_height)
        self.btn_tags.setFixedHeight(button_height)

        toggle_layout = QHBoxLayout()
        toggle_layout.setContentsMargins(0, 0, 0, 0)
        toggle_layout.setSpacing(0)
        toggle_layout.addWidget(self.btn_library)
        toggle_layout.addWidget(self.btn_tags)
        layout.addLayout(toggle_layout)

        # StackedWidget 作为主导航区域
        self.stack = QStackedWidget()

        # Library 视图
        self.library_list = QListWidget()
        self.library_list.addItems(["📥 Inbox", "⭐ Favorites", "📂 All Snippets", "🗑 Trash"])
        self.library_list.setSpacing(0)
        item_count = self.library_list.count()
        item_height = self.library_list.sizeHintForRow(0)
        total_height = item_height * item_count + 2
        self.library_list.setFixedHeight(total_height)

        self.folder_list = QListWidget()
        self.folder_list.setSpacing(0)
        self.update_folder_list()

        library_widget = QWidget()
        library_layout = QVBoxLayout()
        library_layout.setContentsMargins(0, 5, 0, 0)
        library_layout.setSpacing(0)
        library_layout.addWidget(self.library_list)
        library_layout.addWidget(self.folder_list)
        library_widget.setLayout(library_layout)

        tags_widget = QListWidget()
        tags_widget.addItems(["🏷️ Tag 1", "🏷️ Tag 2", "🏷️ Tag 3"])
        tags_widget.setSpacing(0)

        self.stack.addWidget(library_widget)
        self.stack.addWidget(tags_widget)

        self.btn_library.clicked.connect(lambda: self.switch_view(0))
        self.btn_tags.clicked.connect(lambda: self.switch_view(1))
        self.folder_list.currentItemChanged.connect(self.on_folder_changed)

        layout.addWidget(self.stack)

        layout.setStretch(0, 0)
        layout.setStretch(1, 0)
        layout.setStretch(2, 1)
        library_layout.setStretch(0, 0)
        library_layout.setStretch(1, 1)

        # 监听目录变化
        self.watcher = QFileSystemWatcher()
        self.watcher.addPath(str(self.code_dir))
        self.watcher.directoryChanged.connect(self.update_folder_list)

        self.setLayout(layout)

    def switch_view(self, index):
        self.stack.setCurrentIndex(index)
        self.btn_library.setChecked(index == 0)
        self.btn_tags.setChecked(index == 1)

    def update_folder_list(self):
        self.folder_list.clear()
        for folder in os.listdir(self.code_dir):
            folder_path = os.path.join(self.code_dir, folder)
            if os.path.isdir(folder_path):
                self.folder_list.addItem(f"📁 {folder}")
        # 默认选中第一个文件夹
        if self.folder_list.count() > 0:
            self.folder_list.setCurrentRow(0)

    def create_new_folder(self):
        folder_name, ok = QInputDialog.getText(self, "新建文件夹", "请输入文件夹名称:")
        if ok and folder_name:
            new_folder_path = os.path.join(self.code_dir, folder_name)
            if not os.path.exists(new_folder_path):
                os.makedirs(new_folder_path)
                # 创建空的 metadata.json
                with open(os.path.join(new_folder_path, "metadata.json"), "w", encoding="utf-8") as f:
                    json.dump({}, f, indent=4)
                self.update_folder_list()
                self.on_new_folder()


class CodeCapsule(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("代码胶囊")
        self.current_project = None

        self.base_dir = Path.cwd()
        self.default_folder = self.base_dir / "code_dir"
        self.code_dir = self.default_folder
        self.setup_default_folder()

        self.folder_bar = FolderBar(str(self.code_dir), self.on_folder_changed, self.on_new_folder)

        self.content_edit = QTextEdit()
        self.content_edit.setReadOnly(True)
        self.tags_edit = QLineEdit()
        self.tags_edit.setPlaceholderText("Add Tag")
        self.code_type_combo = QComboBox()
        self.code_type_combo.addItems(["txt", "python", "java", "bash"])
        self.open_button = QPushButton("打开文件夹")

        # 中间代码片段列表（自定义组件）
        self.snippet_container = QWidget()
        self.snippet_layout = QVBoxLayout()
        self.snippet_container.setLayout(self.snippet_layout)
        self.snippet_scroll = QScrollArea()
        self.snippet_scroll.setWidget(self.snippet_container)
        self.snippet_scroll.setWidgetResizable(True)

        # 中间区域顶部添加“+”按钮
        snippet_widget = QWidget()
        snippet_widget_layout = QVBoxLayout()
        # 搜索框和“+”按钮
        top_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.setStyleSheet("QLineEdit { padding: 5px; border: 1px solid #D3D3D3; border-radius: 5px; }")
        self.new_snippet_button = QPushButton("+")
        self.new_snippet_button.clicked.connect(self.create_new_snippet)
        top_layout.addWidget(self.search_bar)
        top_layout.addWidget(self.new_snippet_button)

        snippet_widget_layout.addLayout(top_layout)
        snippet_widget_layout.addWidget(self.snippet_scroll)
        snippet_widget.setLayout(snippet_widget_layout)

        # 右侧布局
        snippet_view = QWidget()
        snippet_layout = QVBoxLayout()
        metadata_layout = QFormLayout()
        metadata_layout.addRow("标签:", self.tags_edit)
        metadata_layout.addRow("代码类型:", self.code_type_combo)
        snippet_layout.addWidget(self.content_edit)
        snippet_layout.addLayout(metadata_layout)
        snippet_layout.addWidget(self.open_button)
        snippet_view.setLayout(snippet_layout)

        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.addWidget(self.folder_bar)
        main_splitter.addWidget(snippet_widget)
        main_splitter.addWidget(snippet_view)

        main_splitter.setSizes([150, 300, 350])
        self.setCentralWidget(main_splitter)

        self.open_button.clicked.connect(self.open_folder)
        self.content_edit.textChanged.connect(self.on_text_changed)

        settings = QSettings("MyCompany", "CodeCapsule")
        folder = settings.value("code_dir", str(self.default_folder))
        if folder and os.path.exists(folder):
            self.code_dir = folder
            self.folder_bar.code_dir = self.code_dir
            self.folder_bar.watcher.addPath(str(self.code_dir))

        # 默认选中第一个文件夹
        if self.folder_bar.folder_list.count() > 0:
            self.folder_bar.folder_list.setCurrentRow(0)

    def setup_default_folder(self):
        if not os.path.exists(self.default_folder):
            os.makedirs(self.default_folder)
            print(f"创建默认示例文件夹: {self.default_folder}")

            project1_path = self.default_folder / "demo_project1"
            os.makedirs(project1_path)
            with open(project1_path / "snippet1.py", "w", encoding="utf-8") as f:
                f.write("print('Hello, World!')\n")
            with open(project1_path / "snippet2.sh", "w", encoding="utf-8") as f:
                f.write("#!/bin/bash\necho 'Hello from Bash'\n")
            metadata1 = {
                "snippet1.py": {"tags": ["python", "example"], "code_type": "python"},
                "snippet2.sh": {"tags": ["bash", "script"], "code_type": "bash"}
            }
            with open(project1_path / "metadata.json", "w", encoding="utf-8") as f:
                json.dump(metadata1, f, indent=4)

            project2_path = self.default_folder / "demo_project2"
            os.makedirs(project2_path)
            with open(project2_path / "snippet3.java", "w", encoding="utf-8") as f:
                f.write("public class Hello {\n    public static void main(String[] args) {\n        System.out.println(\"Hello, Java!\");\n    }\n}\n")
            metadata2 = {
                "snippet3.java": {"tags": ["java", "example"], "code_type": "java"}
            }
            with open(project2_path / "metadata.json", "w", encoding="utf-8") as f:
                json.dump(metadata2, f, indent=4)
            print("在默认文件夹中创建示例文件")

    def on_folder_changed(self):
        selected_folder = self.folder_bar.folder_list.currentItem()
        if selected_folder:
            folder_name = selected_folder.text().replace("📁 ", "")
            self.current_project = os.path.join(self.code_dir, folder_name)
            print(f"切换到文件夹: {self.current_project}")
            self.content_edit.setReadOnly(True)
            self.content_edit.setText("")
            self.tags_edit.setText("")
            self.code_type_combo.setCurrentIndex(0)
            self.content_edit.setProperty("current_file", None)
            self.update_snippet_list()

    def on_new_folder(self):
        # 新建文件夹时刷新代码片段列表
        self.on_folder_changed()

    def update_snippet_list(self):
        # 清空现有卡片
        for i in reversed(range(self.snippet_layout.count())):
            widget = self.snippet_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # 填充新卡片
        project_path = self.current_project
        if not project_path or not os.path.exists(project_path):
            print(f"无效的项目路径: {project_path}")
            return

        metadata_path = os.path.join(project_path, "metadata.json")
        metadata = {}
        if os.path.exists(metadata_path):
            try:
                metadata = json.load(open(metadata_path, 'r'))
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"加载 metadata.json 失败: {e}")
                metadata = {}

        files = os.listdir(project_path)
        print(f"当前文件夹中的文件: {files}")
        for file in files:
            if file != "metadata.json":
                file_path = os.path.join(project_path, file)
                mod_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%H:%M")
                card = SnippetCard(file, mod_time)
                card.mousePressEvent = lambda event, f=file: self.on_snippet_clicked(f)
                self.snippet_layout.addWidget(card)
        self.snippet_layout.addStretch()

        # 默认选中第一个卡片
        if self.snippet_layout.count() > 1:  # 排除 stretch
            first_card = self.snippet_layout.itemAt(0).widget()
            if first_card:
                self.on_snippet_clicked(first_card.filename)

    def on_snippet_clicked(self, filename):
        if not self.current_project:
            print("当前项目路径未设置")
            return

        file_path = os.path.join(self.current_project, filename)
        print(f"点击代码片段: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.content_edit.setText(f.read())
        except FileNotFoundError:
            print(f"文件未找到: {file_path}")
            self.content_edit.setText("文件未找到")
        metadata_path = os.path.join(self.current_project, "metadata.json")
        metadata = {}
        if os.path.exists(metadata_path):
            try:
                metadata = json.load(open(metadata_path, 'r'))
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"加载 metadata.json 失败: {e}")
                metadata = {}
        snippet_data = metadata.get(filename, {})
        self.tags_edit.setText(", ".join(snippet_data.get("tags", [])))
        self.code_type_combo.setCurrentText(snippet_data.get("code_type", "txt"))
        self.content_edit.setReadOnly(False)
        self.content_edit.setProperty("current_file", filename)

    def on_text_changed(self):
        selected_filename = self.content_edit.property("current_file")
        if selected_filename and self.current_project:
            file_path = os.path.join(self.current_project, selected_filename)
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.content_edit.toPlainText())
            except Exception as e:
                print(f"保存文件失败: {e}")
            metadata_path = os.path.join(self.current_project, "metadata.json")
            metadata = {}
            if os.path.exists(metadata_path):
                try:
                    metadata = json.load(open(metadata_path, 'r'))
                except (json.JSONDecodeError, FileNotFoundError) as e:
                    print(f"加载 metadata.json 失败: {e}")
                    metadata = {}
            tags = [tag.strip() for tag in self.tags_edit.text().split(",")]
            metadata[selected_filename] = {"tags": tags, "code_type": self.code_type_combo.currentText()}
            try:
                with open(metadata_path, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, indent=4)
            except Exception as e:
                print(f"保存 metadata.json 失败: {e}")
            self.update_snippet_list()

    def create_new_snippet(self):
        if not self.current_project:
            return
        filename, ok = QInputDialog.getText(self, "新建代码片段", "请输入文件名:")
        if ok and filename:
            file_path = os.path.join(self.current_project, filename)
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("")
                self.update_snippet_list()

    def open_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择主文件夹")
        if folder:
            self.code_dir = folder
            self.folder_bar.code_dir = self.code_dir
            self.folder_bar.watcher.removePath(str(self.code_dir))
            self.folder_bar.watcher.addPath(str(self.code_dir))
            self.folder_bar.update_folder_list()
            settings = QSettings("MyCompany", "CodeCapsule")
            settings.setValue("code_dir", folder)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('logo.svg'))
    window = CodeCapsule()
    window.show()
    sys.exit(app.exec())