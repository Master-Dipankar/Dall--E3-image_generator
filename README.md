#Required files for safe exe file
clean_build.spec 
build.py
file_version_info.txt
Run this command sequence:
        #1. Install required packages
        pip install pyinstaller pywin32-ctypes
        # 2. Create a virtual environment (recommended)
        python -m venv venv
        .\venv\Scripts\activate
        # 3. Install dependencies in virtual environment
        pip install openai pillow requests customtkinter
        # 4. Run the build script
        python build.py
#Add this to your code before the main class:
    import os
    import sys
    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
#installer.iss
app.ico 
build_steps.bat
verify_build.py
  
Step-by-step execution:
        # 1. Open command prompt as administrator
        # 2. Navigate to your project folder
        cd path\to\your\project 
        # 3. Create and activate virtual environment (recommended)
        python -m venv venv
        venv\Scripts\activate
        # 4. Run the build script
        python build.py
        # 5. Verify the build
        python verify_build.py
After build completion:

  Check the dist folder for your executable
  Test the executable by double-clicking it

If you get Defender warning:
    # Run in PowerShell as Administrator
    $exePath = "path\to\your\dist\DallE3_ImageGenerator.exe"
    # Add exclusion
    Add-MpPreference -ExclusionPath $exePath
    # Verify exclusion
    Get-MpPreference | Select-Object -ExpandProperty ExclusionPath
    
For distribution, create a zip package:
    package.py
  
Final checks:
    # Run packaging
    python package.py
    # Test the packaged exe
    # Check file hash
    python verify_build.py
Install required packages:
    pip install pyinstaller
    pip install pywin32-ctypes
    pip install openai pillow requests customtkinter

Create an icon file or use this command to create a spec file without an icon:
    pyinstaller --clean --noconsole --onefile --name "DallE3_ImageGenerator" image_generator.py    

Or, if you want to use the spec file:
    Save both files above and run:
       python build.py
If you still get errors, you can try this direct command:
    pyinstaller --clean --noconsole --onefile --name "DallE3_ImageGenerator" --hidden-import PIL._tkinter_finder --hidden-import tkinter --hidden-import tkinter.ttk --hidden-import customtkinter --hidden-import PIL --hidden-import requests image_generator.py
    
