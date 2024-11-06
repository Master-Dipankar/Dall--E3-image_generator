# Save as build_steps.bat

@echo off
echo Installing required packages...
pip install pyinstaller
pip install pywin32-ctypes
pip install openai pillow requests customtkinter

echo Creating clean build...
python -m PyInstaller --clean ^
    --noconsole ^
    --onefile ^
    --name "DallE3_ImageGenerator" ^
    --icon="app.ico" ^
    --version-file="file_version_info.txt" ^
    --uac-admin ^
    --clean ^
    image_generator.py

echo Build complete! Check the dist folder.
pause