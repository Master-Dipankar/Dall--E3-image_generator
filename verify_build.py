import os
import hashlib

def calculate_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def verify_build():
    exe_path = os.path.join('dist', 'DallE3_ImageGenerator.exe')
    if not os.path.exists(exe_path):
        print("Build failed: Executable not found!")
        return False
    
    # Calculate and save hash
    file_hash = calculate_hash(exe_path)
    with open('build_hash.txt', 'w') as f:
        f.write(file_hash)
    
    print(f"Build successful!")
    print(f"Executable location: {os.path.abspath(exe_path)}")
    print(f"File hash (SHA-256): {file_hash}")
    print(f"File size: {os.path.getsize(exe_path) / (1024*1024):.2f} MB")
    return True

if __name__ == '__main__':
    verify_build()
