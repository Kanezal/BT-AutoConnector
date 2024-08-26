from PyQt5.QtWidgets import QPushButton


class Button(QPushButton):
    def __init__(self, *args) -> None:
        super().__init__(*args)

        self.set_style()

    def set_style(self) -> None:
        self.setStyleSheet("""
            QPushButton {
                font-size: 13px;
            }
        """)
