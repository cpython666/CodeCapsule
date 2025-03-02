import sys
import os
import json
from pathlib import Path  # 用于跨平台路径处理

from PySide6.QtWidgets import (QMainWindow, QTreeView, QTableView, QTextEdit,
                               QLineEdit, QComboBox, QPushButton, QSplitter,
                               QVBoxLayout, QFormLayout, QWidget, QFileDialog, QApplication)
from PySide6.QtCore import QSettings
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon


class SnippetManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("代码片段管理器")
        self.current_project = None

        # 设置默认主文件夹
        self.default_folder = str(Path.home() / "SnippetVault")  # 默认路径: ~/SnippetVault
        self.code_dir = self.default_folder
        self.setup_default_folder()  # 创建默认文件夹和示例文件

        # GUI 组件
        self.tree_view = QTreeView()
        self.snippet_table = QTableView()
        self.content_edit = QTextEdit()
        self.content_edit.setReadOnly(True)
        self.tags_edit = QLineEdit()
        self.code_type_combo = QComboBox()
        self.code_type_combo.addItems(["txt", "python", "java", "bash"])
        self.save_button = QPushButton("保存")
        self.open_button = QPushButton("打开文件夹")

        # 设置模型
        self.tree_model = QStandardItemModel()
        self.tree_view.setModel(self.tree_model)
        self.table_model = QStandardItemModel()
        self.snippet_table.setModel(self.table_model)

        # 布局
        main_splitter = QSplitter()
        main_splitter.addWidget(self.tree_view)

        right_splitter = QSplitter()
        right_splitter.addWidget(self.snippet_table)

        snippet_view = QWidget()
        snippet_layout = QVBoxLayout()
        metadata_layout = QFormLayout()
        metadata_layout.addRow("标签:", self.tags_edit)
        metadata_layout.addRow("代码类型:", self.code_type_combo)
        snippet_layout.addWidget(self.content_edit)
        snippet_layout.addLayout(metadata_layout)
        snippet_layout.addWidget(self.save_button)
        snippet_layout.addWidget(self.open_button)
        snippet_view.setLayout(snippet_layout)
        right_splitter.addWidget(snippet_view)

        main_splitter.addWidget(right_splitter)
        self.setCentralWidget(main_splitter)

        # 信号连接
        self.tree_view.selectionModel().selectionChanged.connect(self.on_tree_selection_changed)
        self.snippet_table.selectionModel().selectionChanged.connect(self.on_snippet_selection_changed)
        self.save_button.clicked.connect(self.on_save)
        self.open_button.clicked.connect(self.open_folder)

        # 加载默认文件夹或上次保存的文件夹
        settings = QSettings("MyCompany", "SnippetManager")
        folder = settings.value("code_dir", self.default_folder)
        if folder and os.path.exists(folder):
            self.code_dir = folder
        self.populate_tree(self.code_dir)

    def setup_default_folder(self):
        """创建默认文件夹和示例文件"""
        if not os.path.exists(self.default_folder):
            os.makedirs(self.default_folder)
            print(f"Created default folder: {self.default_folder}")

            # 创建 project1
            project1_path = os.path.join(self.default_folder, "project1")
            os.makedirs(project1_path)
            with open(os.path.join(project1_path, "snippet1.py"), "w", encoding="utf-8") as f:
                f.write("print('Hello, World!')\n")
            with open(os.path.join(project1_path, "snippet2.sh"), "w", encoding="utf-8") as f:
                f.write("#!/bin/bash\necho 'Hello from Bash'\n")
            metadata1 = {
                "snippet1.py": {"tags": ["python", "example"], "code_type": "python"},
                "snippet2.sh": {"tags": ["bash", "script"], "code_type": "bash"}
            }
            with open(os.path.join(project1_path, "metadata.json"), "w", encoding="utf-8") as f:
                json.dump(metadata1, f, indent=4)

            # 创建 project2
            project2_path = os.path.join(self.default_folder, "project2")
            os.makedirs(project2_path)
            with open(os.path.join(project2_path, "snippet3.java"), "w", encoding="utf-8") as f:
                f.write("public class Hello {\n    public static void main(String[] args) {\n        System.out.println(\"Hello, Java!\");\n    }\n}\n")
            metadata2 = {
                "snippet3.java": {"tags": ["java", "example"], "code_type": "java"}
            }
            with open(os.path.join(project2_path, "metadata.json"), "w", encoding="utf-8") as f:
                json.dump(metadata2, f, indent=4)
            print("Created example files in default folder")

    def populate_tree(self, code_dir):
        print(f"Populating tree with folder: {code_dir}")
        self.tree_model.clear()
        root_item = self.tree_model.invisibleRootItem()
        projects = os.listdir(code_dir)
        print(f"Found projects: {projects}")
        for project in projects:
            project_path = os.path.join(code_dir, project)
            if os.path.isdir(project_path):
                project_item = QStandardItem(project)
                root_item.appendRow(project_item)
                files = os.listdir(project_path)
                print(f"Files in {project}: {files}")
                for file in files:
                    if file != "metadata.json":
                        snippet_item = QStandardItem(file)
                        project_item.appendRow(snippet_item)
        self.tree_view.expandAll()

    def on_tree_selection_changed(self):
        selected = self.tree_view.selectedIndexes()
        if selected:
            index = selected[0]
            item = self.tree_view.model().itemFromIndex(index)
            if item.hasChildren():  # 项目
                project_path = os.path.join(self.code_dir, item.text())
                self.current_project = project_path
                self.populate_snippet_table(project_path)

    def populate_snippet_table(self, project_path):
        print(f"Populating table with project: {project_path}")
        metadata_path = os.path.join(project_path, "metadata.json")
        metadata = json.load(open(metadata_path, 'r')) if os.path.exists(metadata_path) else {}
        print(f"Metadata: {metadata}")

        self.table_model.clear()
        self.table_model.setHorizontalHeaderLabels(["文件名", "标签", "代码类型"])
        files = os.listdir(project_path)
        print(f"Files in project: {files}")
        for file in files:
            if file != "metadata.json":
                tags = ", ".join(metadata.get(file, {}).get("tags", []))
                code_type = metadata.get(file, {}).get("code_type", "txt")
                self.table_model.appendRow([QStandardItem(file), QStandardItem(tags), QStandardItem(code_type)])

    def on_snippet_selection_changed(self):
        selected = self.snippet_table.selectedIndexes()
        if selected:
            row = selected[0].row()
            filename = self.snippet_table.model().item(row, 0).text()
            file_path = os.path.join(self.current_project, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.content_edit.setText(f.read())
            except FileNotFoundError:
                self.content_edit.setText("文件未找到")
            metadata_path = os.path.join(self.current_project, "metadata.json")
            metadata = json.load(open(metadata_path, 'r')) if os.path.exists(metadata_path) else {}
            snippet_data = metadata.get(filename, {})
            self.tags_edit.setText(", ".join(snippet_data.get("tags", [])))
            self.code_type_combo.setCurrentText(snippet_data.get("code_type", "txt"))
            self.content_edit.setReadOnly(False)

    def on_save(self):
        selected = self.snippet_table.selectedIndexes()
        if selected:
            row = selected[0].row()
            filename = self.snippet_table.model().item(row, 0).text()
            file_path = os.path.join(self.current_project, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.content_edit.toPlainText())
            metadata_path = os.path.join(self.current_project, "metadata.json")
            metadata = json.load(open(metadata_path, 'r')) if os.path.exists(metadata_path) else {}
            tags = [tag.strip() for tag in self.tags_edit.text().split(",")]
            metadata[filename] = {"tags": tags, "code_type": self.code_type_combo.currentText()}
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=4)
            self.populate_snippet_table(self.current_project)

    def open_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择主文件夹")
        if folder:
            self.code_dir = folder
            self.populate_tree(folder)
            settings = QSettings("MyCompany", "SnippetManager")
            settings.setValue("code_dir", folder)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('docs/imgs/logo.svg'))  # 确保 logo.png 存在，否则注释掉
    window = SnippetManager()
    window.show()
    sys.exit(app.exec())