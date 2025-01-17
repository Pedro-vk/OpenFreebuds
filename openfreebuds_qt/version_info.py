VERSION = '0.99.1'
LIBRARIES = [
    'aiocmd==0.1.5 ; python_version >= "3.10" and python_version < "3.13"',
    'aiohappyeyeballs==2.4.0 ; python_version >= "3.10" and python_version < "3.13"',
    'aiohttp==3.10.5 ; python_version >= "3.10" and python_version < "3.13"',
    'aiosignal==1.3.1 ; python_version >= "3.10" and python_version < "3.13"',
    'altgraph==0.17.4 ; python_version >= "3.10" and python_version < "3.13"',
    'async-timeout==4.0.3 ; python_version >= "3.10" and python_version < "3.11"',
    'attrs==24.2.0 ; python_version >= "3.10" and python_version < "3.13"',
    'build==1.2.1 ; python_version >= "3.10" and python_version < "3.13"',
    'cachecontrol[filecache]==0.14.0 ; python_version >= "3.10" and python_version < "3.13"',
    'certifi==2024.8.30 ; python_version >= "3.10" and python_version < "3.13"',
    'cffi==1.17.0 ; python_version >= "3.10" and python_version < "3.13" and (sys_platform == "darwin" or sys_platform == "linux") and (sys_platform == "darwin" or platform_python_implementation != "PyPy")',
    'charset-normalizer==3.3.2 ; python_version >= "3.10" and python_version < "3.13"',
    'cleo==2.1.0 ; python_version >= "3.10" and python_version < "3.13"',
    'colorama==0.4.6 ; python_version >= "3.10" and python_version < "3.13" and os_name == "nt"',
    'crashtest==0.4.1 ; python_version >= "3.10" and python_version < "3.13"',
    'cryptography==43.0.0 ; python_version >= "3.10" and python_version < "3.13" and sys_platform == "linux"',
    'distlib==0.3.8 ; python_version >= "3.10" and python_version < "3.13"',
    'dulwich==0.21.7 ; python_version >= "3.10" and python_version < "3.13"',
    'evdev==1.7.1 ; python_version >= "3.10" and python_version < "3.13" and sys_platform in "linux"',
    'fastjsonschema==2.20.0 ; python_version >= "3.10" and python_version < "3.13"',
    'filelock==3.15.4 ; python_version >= "3.10" and python_version < "3.13"',
    'frozenlist==1.4.1 ; python_version >= "3.10" and python_version < "3.13"',
    'idna==3.8 ; python_version >= "3.10" and python_version < "3.13"',
    'importlib-metadata==8.4.0 ; python_version >= "3.10" and python_version < "3.12"',
    'installer==0.7.0 ; python_version >= "3.10" and python_version < "3.13"',
    'jaraco-classes==3.4.0 ; python_version >= "3.10" and python_version < "3.13"',
    'jeepney==0.8.0 ; python_version >= "3.10" and python_version < "3.13" and sys_platform == "linux"',
    'keyring==24.3.1 ; python_version >= "3.10" and python_version < "3.13"',
    'macholib==1.16.3 ; python_version >= "3.10" and python_version < "3.13" and sys_platform == "darwin"',
    'more-itertools==10.4.0 ; python_version >= "3.10" and python_version < "3.13"',
    'msgpack==1.0.8 ; python_version >= "3.10" and python_version < "3.13"',
    'multidict==6.0.5 ; python_version >= "3.10" and python_version < "3.13"',
    'packaging==24.1 ; python_version >= "3.10" and python_version < "3.13"',
    'pefile==2024.8.26 ; python_version >= "3.10" and python_version < "3.13" and sys_platform == "win32"',
    'pexpect==4.9.0 ; python_version >= "3.10" and python_version < "3.13"',
    'pillow==10.4.0 ; python_version >= "3.10" and python_version < "3.13"',
    'pkginfo==1.11.1 ; python_version >= "3.10" and python_version < "3.13"',
    'platformdirs==4.2.2 ; python_version >= "3.10" and python_version < "3.13"',
    'poetry-core==1.9.0 ; python_version >= "3.10" and python_version < "3.13"',
    'poetry-plugin-export==1.8.0 ; python_version >= "3.10" and python_version < "3.13"',
    'poetry==1.8.3 ; python_version >= "3.10" and python_version < "3.13"',
    'prompt-toolkit==3.0.47 ; python_version >= "3.10" and python_version < "3.13"',
    'psutil==6.0.0 ; python_version >= "3.10" and python_version < "3.13"',
    'ptyprocess==0.7.0 ; python_version >= "3.10" and python_version < "3.13"',
    'pycairo==1.26.1 ; python_version >= "3.10" and python_version < "3.13" and sys_platform == "linux"',
    'pycparser==2.22 ; python_version >= "3.10" and python_version < "3.13" and (sys_platform == "darwin" or sys_platform == "linux") and (sys_platform == "darwin" or platform_python_implementation != "PyPy")',
    'pygobject==3.48.2 ; python_version >= "3.10" and python_version < "3.13" and sys_platform == "linux"',
    'pyinstaller-hooks-contrib==2024.8 ; python_version >= "3.10" and python_version < "3.13"',
    'pyinstaller==6.10.0 ; python_version >= "3.10" and python_version < "3.13"',
    'pynput==1.7.7 ; python_version >= "3.10" and python_version < "3.13"',
    'pyobjc-core==10.3.1 ; python_version >= "3.10" and python_version < "3.13" and sys_platform == "darwin"',
    'pyobjc-framework-applicationservices==10.3.1 ; python_version >= "3.10" and python_version < "3.13" and sys_platform == "darwin"',
    'pyobjc-framework-cocoa==10.3.1 ; python_version >= "3.10" and python_version < "3.13" and sys_platform == "darwin"',
    'pyobjc-framework-coretext==10.3.1 ; python_version >= "3.10" and python_version < "3.13" and sys_platform == "darwin"',
    'pyobjc-framework-quartz==10.3.1 ; python_version >= "3.10" and python_version < "3.13" and sys_platform == "darwin"',
    'pyproject-hooks==1.1.0 ; python_version >= "3.10" and python_version < "3.13"',
    'pyqt6-qt6==6.7.2 ; python_version >= "3.10" and python_version < "3.13"',
    'pyqt6-sip==13.8.0 ; python_version >= "3.10" and python_version < "3.13"',
    'pyqt6==6.7.1 ; python_version >= "3.10" and python_version < "3.13"',
    'python-xlib==0.33 ; python_version >= "3.10" and python_version < "3.13" and sys_platform in "linux"',
    'pywin32-ctypes==0.2.3 ; python_version >= "3.10" and python_version < "3.13" and sys_platform == "win32"',
    'qasync==0.27.1 ; python_version >= "3.10" and python_version < "3.13"',
    'rapidfuzz==3.9.6 ; python_version >= "3.10" and python_version < "3.13"',
    'requests-toolbelt==1.0.0 ; python_version >= "3.10" and python_version < "3.13"',
    'requests==2.32.3 ; python_version >= "3.10" and python_version < "3.13"',
    'sdbus==0.12.0 ; python_version >= "3.10" and python_version < "3.13" and sys_platform == "linux"',
    'secretstorage==3.3.3 ; python_version >= "3.10" and python_version < "3.13" and sys_platform == "linux"',
    'setuptools==74.0.0 ; python_version >= "3.10" and python_version < "3.13"',
    'shellingham==1.5.4 ; python_version >= "3.10" and python_version < "3.13"',
    'six==1.16.0 ; python_version >= "3.10" and python_version < "3.13"',
    'tomli==2.0.1 ; python_version >= "3.10" and python_version < "3.11"',
    'tomlkit==0.13.2 ; python_version >= "3.10" and python_version < "3.13"',
    'trove-classifiers==2024.7.2 ; python_version >= "3.10" and python_version < "3.13"',
    'urllib3==2.2.2 ; python_version >= "3.10" and python_version < "3.13"',
    'virtualenv==20.26.3 ; python_version >= "3.10" and python_version < "3.13"',
    'wcwidth==0.2.13 ; python_version >= "3.10" and python_version < "3.13"',
    'winsdk==1.0.0b10 ; python_version >= "3.10" and python_version < "3.13" and sys_platform == "win32"',
    'xattr==1.1.0 ; python_version >= "3.10" and python_version < "3.13" and sys_platform == "darwin"',
    'yarl==1.9.5 ; python_version >= "3.10" and python_version < "3.13"',
    'zipp==3.20.1 ; python_version >= "3.10" and python_version < "3.12"',
]
