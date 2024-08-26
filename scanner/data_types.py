from ctypes import CDLL, windll, Structure, Union, POINTER, byref, sizeof, c_ulong, c_ulonglong, c_int, c_char
from ctypes.wintypes import DWORD, WORD, BOOL, BYTE, WCHAR, HANDLE

BTH_ADDR = c_ulonglong
HDEVINFO = c_int
LPTSTR = POINTER(c_char)

PBYTE = POINTER(BYTE)

SPDRP_FRIENDLYNAME = 0x0C

ERROR_INSUFFICIENT_BUFFER = 0x7A

def new(structure, **kwargs):
    s = structure()
    for k, v in kwargs.items():
        setattr(s, k, v)
    return s


class GUID(Structure):
    _fields_ = [
        ("Data1", DWORD),
        ("Data2", WORD),
        ("Data3", WORD),
        ("Data4", BYTE * 8)
        ]

GUID_DEVCLASS_BLUETOOTH = new(GUID,
                              Data1=0xE0CBF06C,
                              Data2=0xCD8B,
                              Data3=0x4647,
                              Data4=(BYTE * 8).from_buffer_copy(
                                  bytearray([0xBB, 0x8A, 0x26, 0x3B, 0x43, 0xF0, 0xF9, 0x74])))
DIGCF_DEFAULT = 0x01
DIGCF_PRESENT = 0x02
DIGCF_ALLCLASSES = 0x04
DIGCF_PROFILE = 0x08
DIGCF_DEVINTERFACE = 0x10

class SP_DEVINFO_DATA(Structure):
    _fields_ = [
        ("cbSize", DWORD),
        ("ClassGUID", GUID),
        ("DevInst", DWORD),
        ("Reserved", POINTER(c_ulong))]

class SYSTEMTIME(Structure):
    _fields_ = [
        ("wYear", WORD),
        ("wMonth", WORD),
        ("wDayOfWeek", WORD),
        ("wDay", WORD),
        ("wHour", WORD),
        ("wMinute", WORD),
        ("wSecond", WORD),
        ("wMilliseconds", WORD)]

class BLUETOOTH_ADDRESS(Union):
    _fields_ = [
        ("ullLong", BTH_ADDR),
        ("rgBytes", BYTE * 6)]

class BLUETOOTH_FIND_RADIO_PARAMS(Structure):
    _fields_ = [
        ("dwSize", DWORD)]

class BLUETOOTH_DEVICE_SEARCH_PARAMS(Structure):
    _fields_ = [
        ("dwSize", DWORD),
        ("fReturnAuthenticated", BOOL),
        ("fReturnRemembered", BOOL),
        ("fReturnUnknown", BOOL),
        ("fReturnConnected", BOOL),
        ("fIssueInquiry", BOOL),
        ("cTimeoutMultiplier", c_ulong),
        ("hRadio", HANDLE)]

class BLUETOOTH_DEVICE_INFO(Structure):
    _fields_ = [
        ("dwSize", DWORD),
        ("Address", BLUETOOTH_ADDRESS),
        ("ulClassofDevice", c_ulong),
        ("fConnected", BOOL),
        ("fRemembered", BOOL),
        ("fAuthenticated", BOOL),
        ("stLastSeen", SYSTEMTIME),
        ("stLastUsed", SYSTEMTIME),
        ("szName", WCHAR * 248)]


BT = windll.BluetoothAPIs
SAPI = windll.Setupapi
WBAse = windll.Kernel32

GetLastError = WBAse.GetLastError

BT.BluetoothFindFirstDevice.restype = HANDLE

BT.BluetoothFindNextDevice.argtypes = [HANDLE, POINTER(BLUETOOTH_DEVICE_INFO)]

BT.BluetoothFindRadioClose.argtypes = [HANDLE]

