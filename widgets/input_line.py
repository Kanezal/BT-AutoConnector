from PyQt5.QtWidgets import QLineEdit


class InputLine(QLineEdit):
    def __init__(self, *args) -> None:
        super().__init__(*args)

        self.set_style()

    def set_style(self) -> None:
        self.setStyleSheet("""
            QLineEdit {
                font-size: 13px;
            }
        """)
