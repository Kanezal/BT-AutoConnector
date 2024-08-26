import socket

from .data_types import *

from threading import Thread
from PyQt5.QtCore import QObject


class Scanner(QObject):
    def __init__(self) -> None:
        super().__init__()
        self.search_device = ""

        self.find = False
        self.connected = False
        self.paired = False
        self.address = ""

        self.processing_connected = False
        self.processing_find = False
        self.processing_pair = False

    def connect_to_device(self) -> None:
        connect_thread = Thread(target=self.connect_thread)
        connect_thread.start()

    def connect_thread(self) -> None:
        try:
            sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            sock.connect((self.address, 5))

            sock.accept()
            sock.listen(1)
        except Exception as e:
            pass

    def start_scanner(self) -> None:
        finding = Thread(target=self.scanner_find)
        pairing = Thread(target=self.scanner_pair)
        connecting = Thread(target=self.scanner_connected)

        self.processing_connected = True
        self.processing_find = True
        self.processing_pair = True

        finding.start()
        pairing.start()
        connecting.start()

    def scanner_find(self) -> None:
        params = BLUETOOTH_DEVICE_SEARCH_PARAMS()
        params.dwSize = sizeof(params)
        params.hRadio = None
        params.fReturnRemembered = True
        params.fReturnConnected = True
        params.fReturnUnknown = True
        params.fIssueInquiry = True
        params.cTimeoutMultiplier = 10

        result = BLUETOOTH_DEVICE_INFO()
        result.dwSize = sizeof(result)

        Handle = BT.BluetoothFindFirstDevice(byref(params), byref(result))

        flg = False
        while Handle:
            if result.szName == self.search_device:
                flg = True
                hex_address = []
                for i in result.Address.rgBytes[::-1]:
                    hex_i = hex(i).strip('0x').upper()
                    hex_address.append(hex_i + '0' if i % 16 == 0 else '0' + hex_i if i < 16 else hex_i)
                self.address = ':'.join(hex_address)
                break

            if not BT.BluetoothFindNextDevice(Handle, byref(result)):
                break

        self.find = flg
        self.processing_find = False

    def scanner_pair(self) -> None:
        params = BLUETOOTH_DEVICE_SEARCH_PARAMS()
        params.dwSize = sizeof(params)
        params.hRadio = None
        params.fReturnRemembered = True
        params.fReturnConnected = False
        params.fReturnUnknown = False
        params.fIssueInquiry = False
        params.cTimeoutMultiplier = 10

        result = BLUETOOTH_DEVICE_INFO()
        result.dwSize = sizeof(result)

        Handle = BT.BluetoothFindFirstDevice(byref(params), byref(result))

        flg = False
        while Handle:
            if result.szName == self.search_device:
                flg = True
                hex_address = []
                for i in result.Address.rgBytes[::-1]:
                    hex_i = hex(i).strip('0x').upper()
                    hex_address.append(hex_i + '0' if i % 16 == 0 else '0' + hex_i if i < 16 else hex_i)
                self.address = ':'.join(hex_address)
                break

            if not BT.BluetoothFindNextDevice(Handle, byref(result)):
                break

        self.paired = flg
        self.processing_pair = False

    def scanner_connected(self) -> None:
        params = BLUETOOTH_DEVICE_SEARCH_PARAMS()
        params.dwSize = sizeof(params)
        params.hRadio = None
        params.fReturnRemembered = False
        params.fReturnConnected = True
        params.fReturnUnknown = False
        params.fIssueInquiry = False
        params.cTimeoutMultiplier = 10

        result = BLUETOOTH_DEVICE_INFO()
        result.dwSize = sizeof(result)

        Handle = BT.BluetoothFindFirstDevice(byref(params), byref(result))

        flg = False
        while Handle:
            if result.szName == self.search_device:
                flg = True
                hex_address = []
                for i in result.Address.rgBytes[::-1]:
                    hex_i = hex(i).strip('0x').upper()
                    hex_address.append(hex_i + '0' if i % 16 == 0 else '0' + hex_i if i < 16 else hex_i)
                self.address = ':'.join(hex_address)
                break

            if not BT.BluetoothFindNextDevice(Handle, byref(result)):
                break

        self.connected = flg
        self.processing_connected = False

scanner = Scanner()