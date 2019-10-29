import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os", "srsly", "cymem", "murmurhash", "blis", "sqlalchemy", "pathlib", "jsonschema", "spacy", "SQLAlchemy", "urllib3", "SecretStorage", "pymongo"],
                     'include_files': ["requirements.txt", "wppbot.py", "cliente.py", "Pulsar-1.png", "Pulsar-2.png", "Pulsar-3.png", "Pulsar-4.png", "chromedriver1.exe"],
                     "includes": ["jsonschema", "sqlalchemy"],
                     "excludes": [],
                    }

# GUI applications require a different base on Windows (the default is for a
# console application).
#base = None
#if sys.platform == "win32":
base = "Win32GUI"

setup(  name = "Chatbot Pulsar",
        version = "1.0",
        description = "Chatbot para WhatsApp da Clínica Pulsar",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base)])