import getpass
import os, sys

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QSystemTrayIcon, QStyle, QAction, QMenu, qApp
)
from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtGui import QIcon
from datetime import datetime, timedelta

from widgets.button import Button
from widgets.label import Label
from widgets.input_line import InputLine

from scanner.scanner import scanner


app = QApplication([])


StatusCodes = {
    "SEARCH": "поиск устройства",
    "WAIT": "ожидание имени устройства",
    "PAIRED": "устройство сопряжено",
    "FIND": "устройство найдено",
    "ON": "устройство подключено",
    "OFF": "scanner отключен"
}


class Window(QMainWindow):
    def __init__(self, title: str) -> None:
        super().__init__()
        self.time_start = datetime.now()

        self.first_timer = QTimer()
        self.first_timer.timeout.connect(self.scanner_start)
        self.first_timer.start(15000)

        self.timer_update = QTimer()
        self.timer_update.timeout.connect(self.update_cycle)
        self.timer_update.start(1000)

        self.status = ""
        self.device_name = ""

        self.setWindowTitle(title)
        self.setFixedSize(QSize(300, 150))

        self.save_button = Button("Сохранить и продолжить", self)
        self.status_label = Label(f"Статус: {self.status}", self)
        self.bluetooth_name = InputLine(self)

        self.interface_init()

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        self.tray_icon.setIcon(QIcon('img/icon.ico'))
        self.tray_icon.activated.connect(self.tray_avtivate)

        self.tray_show = QAction("Показать", self)
        self.tray_exit = QAction("Закрыть", self)
        self.tray_label = QAction(f"Статус: {self.status}")

        self.tray_init()

        self.setWindowIcon(QIcon('img/icon.ico'))

    def tray_avtivate(self, reason) -> None:
        if reason == QSystemTrayIcon.Trigger and self.isVisible():
            self.hide()
        elif reason == QSystemTrayIcon.Trigger:
            self.show()

    def interface_init(self) -> None:
        widget_layout = QVBoxLayout()

        self.bluetooth_name.setFixedSize(275, 20)
        self.bluetooth_name.setPlaceholderText("Название устройства")
        widget_layout.addWidget(self.bluetooth_name, alignment=Qt.AlignHCenter)

        self.save_button.setFixedSize(175, 20)
        self.save_button.clicked.connect(self.save_btn_pressed)
        widget_layout.addWidget(self.save_button, alignment=Qt.AlignHCenter)

        widget_layout.addWidget(self.status_label, alignment=Qt.AlignHCenter)

        container = QWidget()
        container.setLayout(widget_layout)
        self.setCentralWidget(container)

    def update_cycle(self) -> None:
        if scanner.connected and self.status != StatusCodes["ON"]:
            self.change_status(StatusCodes["ON"])
        elif scanner.paired and self.status != StatusCodes["PAIRED"] and not scanner.connected:
            self.change_status(StatusCodes["PAIRED"])
            scanner.connect_to_device()
        elif scanner.find and self.status != StatusCodes["FIND"] and not scanner.connected and not scanner.paired:
            self.change_status(StatusCodes["FIND"])

    def scanner_start(self) -> None:
        if not scanner.processing_find and not scanner.processing_pair and not scanner.processing_connected:
            scanner.search_device = self.device_name
            scanner.start_scanner()

        if datetime.now() - self.time_start > timedelta(minutes=5):
            self.first_timer.setInterval(60000)

    def tray_init(self) -> None:
        tray_menu = QMenu()

        self.tray_label.setEnabled(False)
        tray_menu.addAction(self.tray_label)

        self.tray_show.triggered.connect(self.tray_show_event)
        tray_menu.addAction(self.tray_show)

        self.tray_exit.triggered.connect(self.tray_exit_event)
        tray_menu.addAction(self.tray_exit)

        self.tray_icon.setContextMenu(tray_menu)

        self.tray_icon.show()

    def tray_exit_event(self) -> None:
        qApp.quit()

    def tray_show_event(self) -> None:
        self.tray_icon.hide()
        self.show()

    def save_btn_pressed(self) -> None:
        with open("save.dat", "w") as file:
            self.device_name = self.bluetooth_name.text()
            file.write(self.device_name)

        self.change_status(StatusCodes["SEARCH"])

        scanner.find = False
        scanner.connected = False
        scanner.paired = False

    def closeEvent(self, event) -> None:
        event.ignore()

        self.hide()

        self.tray_icon.showMessage(self.windowTitle(), "Приложение работает в фоновом режиме",
                         QSystemTrayIcon.Information, 2000)

    def change_status(self, status: str) -> None:
        self.status = status
        self.status_label.setText(f"Статус: {self.status}")
        self.tray_label.setText(f"Статус: {self.status}")

        self.tray_icon.showMessage(self.windowTitle(), status.capitalize(),
                                   QSystemTrayIcon.Information, 2000)

    def set_device_name(self, device_name: str) -> None:
        self.device_name = device_name
        self.bluetooth_name.setText(device_name)


if __name__ == "__main__":
    user_name = getpass.getuser()

    try:
        bat_data = open(
            f'C:/Users/{user_name}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/open_bluetooth.bat',
            "r").read()
    except FileNotFoundError:
        with open(
            f'C:/Users/{user_name}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/open_bluetooth.bat',
            "w") as bat_file:
            path_app = sys.argv[0]
            bat_file.write(f'start "" {path_app}')

    window = Window("Bluetooth")

    try:
        window.set_device_name(open("save.dat", "r").read())
        window.change_status(StatusCodes["SEARCH"])

        scanner.search_device = window.device_name
        scanner.start_scanner()
    except FileNotFoundError:
        window.change_status(StatusCodes["WAIT"])

    window.show()
    app.exec()
