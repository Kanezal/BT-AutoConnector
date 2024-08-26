@echo off

set CODE_PATH=%cd%

call "%CODE_PATH%\.venv\Scripts\activate.bat"

pyinstaller --icon "%CODE_PATH%\img\icon.png" --clean --onefile --noconfirm --noconsole --add-data "%CODE_PATH%\img\icon.ico;img\icon.ico" "%CODE_PATH%\window.py" --name "BT AutoConnector"
echo d | xcopy "%CODE_PATH%\img" "%CODE_PATH%\dist\img" /S /E /d

deactivate