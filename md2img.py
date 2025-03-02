import sys
import os
import markdown
import imgkit
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLabel, QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


class MarkdownToImageApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Markdown 转图片工具")
        self.setGeometry(100, 100, 800, 600)  # 设置窗口大小

        # 主部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Markdown 输入区域
        self.markdown_edit = QTextEdit()
        self.markdown_edit.setPlaceholderText("在这里输入 Markdown 内容（支持代码块）...")
        self.markdown_edit.setAcceptRichText(False)  # 确保纯文本输入
        main_layout.addWidget(self.markdown_edit)

        # 按钮区域
        button_layout = QHBoxLayout()
        self.convert_button = QPushButton("转为图片")
        self.convert_button.clicked.connect(self.convert_to_image)
        button_layout.addStretch()  # 居中按钮
        button_layout.addWidget(self.convert_button)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        # 图片预览区域
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setText("图片将在这里显示")
        self.image_scroll_area = QScrollArea()
        self.image_scroll_area.setWidget(self.image_label)
        self.image_scroll_area.setWidgetResizable(True)
        main_layout.addWidget(self.image_scroll_area)

        # 设置布局比例
        main_layout.setStretch(0, 1)  # Markdown 输入区域
        main_layout.setStretch(1, 0)  # 按钮区域
        main_layout.setStretch(2, 1)  # 图片预览区域

    def convert_to_image(self):
        """将 Markdown 内容转换为图片并显示"""
        markdown_text = self.markdown_edit.toPlainText()
        if not markdown_text:
            self.image_label.setText("请输入 Markdown 内容")
            return

        try:
            # 将 Markdown 转换为 HTML
            html = markdown.markdown(markdown_text, extensions=['fenced_code'])

            # 添加简单的 CSS 样式以美化输出
            html_with_style = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5; }}
                    pre, code {{ background-color: #e0e0e0; padding: 5px; border-radius: 3px; }}
                </style>
            </head>
            <body>{html}</body>
            </html>
            """

            # 将 HTML 保存为临时文件
            temp_html_path = "temp.html"
            with open(temp_html_path, "w", encoding="utf-8") as f:
                f.write(html_with_style)

            # 使用 imgkit 将 HTML 转换为图片
            output_image_path = "output.png"
            imgkit.from_file(temp_html_path, output_image_path)

            # 删除临时 HTML 文件
            os.remove(temp_html_path)

            # 在界面中显示图片
            pixmap = QPixmap(output_image_path)
            self.image_label.setPixmap(pixmap.scaled(600, 400, Qt.KeepAspectRatio))
            self.image_label.adjustSize()

        except Exception as e:
            self.image_label.setText(f"转换失败: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MarkdownToImageApp()
    window.show()
    sys.exit(app.exec())