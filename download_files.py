import os
import subprocess

# Files we need based on imports in app.py
files = {
    'database/__init__.py': '',
    'database/db_manager.py': '',
    'nlp/__init__.py': '',
    'nlp/nlp_pipeline.py': '',
    'reminder/__init__.py': '',
    'reminder/reminder_system.py': '',
    'utils/__init__.py': '',
    'utils/export_import.py': '',
    'utils/constants.py': '',
    'tests/__init__.py': '',
    'tests/test_cases.py': ''
}

base_url = "https://raw.githubusercontent.com/HuynhCongY/dacn2/0233964427b55164ae18b0260bf8267f5fccf50a/"

for file_path in files.keys():
    dir_name = os.path.dirname(file_path)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name, exist_ok=True)
    
    url = base_url + file_path
    print(f"Downloading {file_path}...")
    result = subprocess.run(['curl', '-s', '-L', url, '-o', file_path], capture_output=True)
    
    # Check if file was downloaded successfully
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r') as f:
            content = f.read()
            if '404: Not Found' in content:
                print(f"  Failed: 404 Not Found")
            else:
                print(f"  Success: {os.path.getsize(file_path)} bytes")
    else:
        print(f"  Failed: Empty or not created")

print("\nDone!")
