@echo off
echo ============================
echo   桌面宠物 打包脚本
echo ============================
echo.

REM 检查 PyInstaller 是否安装
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo 正在安装 PyInstaller...
    pip install pyinstaller
    echo.
)

echo 开始打包...
echo.

pyinstaller --onefile --noconsole --name "DesktopPet" main.py

echo.
if exist dist\DesktopPet.exe (
    echo ============================
    echo   打包成功！
    echo   输出文件: dist\DesktopPet.exe
    echo ============================
) else (
    echo 打包失败，请检查错误信息。
)

pause
