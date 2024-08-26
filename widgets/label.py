from PyQt5.QtWidgets import QLabel


class Label(QLabel):
    def __init__(self, *args) -> None:
        super().__init__(*args)

        self.set_style()

    def set_style(self) -> None:
        self.setStyleSheet("""
            QLabel {
                font-size: 13px;
            }
        """)
