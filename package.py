# package.py
import os
import shutil
import hashlib
from datetime import datetime

def create_package():
    # Create package folder
    package_name = f"DallE3_ImageGenerator_{datetime.now().strftime('%Y%m%d')}"
    if os.path.exists(package_name):
        shutil.rmtree(package_name)
    os.makedirs(package_name)
    
    # Copy files
    shutil.copy2('dist/DallE3_ImageGenerator.exe', package_name)
    
    # Create README
    with open(f'{package_name}/README.txt', 'w') as f:
        f.write('''DALL-E Image Generator
Version 1.0.0
Created by Dipankar Boruah

Installation:
1. Extract all files to a folder
2. Run DallE3_ImageGenerator.exe
3. If you get a Windows Defender warning:
   - Click "More info"
   - Click "Run anyway"

For support, contact: [Your Contact Info]
''')
    
    # Create ZIP
    shutil.make_archive(package_name, 'zip', package_name)
    print(f"Package created: {package_name}.zip")

if __name__ == '__main__':
    create_package()
