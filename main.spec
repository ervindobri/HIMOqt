# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

#qt5_path = 'C:\\Users\\Legion2\\AppData\\Local\\Programs\\Python\\Python38\\Lib\\site-packages\\PyQt5\\Qt5\\bin\\'
qt5_path = 'C:\\Users\\Legion2\\anaconda3\\envs\\himopy\\Lib\\site-packages\\PyQt5\\Qt5\\bin\\'
#qt6_path = 'C:\\Users\\Legion2\\AppData\\Local\\Programs\\Python\\Python38\\Lib\\site-packages\\PyQt6\\Qt6\\bin\\'
qt6_path = 'C:\\Users\\Legion2\\anaconda3\\envs\\himopy\\Lib\\site-packages\\PyQt6\\Qt6\\bin\\'
added_files = [
    #(qt5_path + 'Qt5Core.dll', 'packages\\qt5'),
    #(qt5_path + 'Qt5Gui.dll', 'packages\\qt5'),
    #(qt5_path + 'Qt5Widgets.dll', 'packages\\qt5'),
    (qt6_path + 'Qt6Core.dll', 'packages\\qt6'),
    (qt6_path + 'Qt6Gui.dll', 'packages\\qt6'),
    (qt6_path + 'Qt6Widgets.dll', 'packages\\qt6'),
    ('C:\\Users\\Legion2\\anaconda3\\envs\\himopy\\Lib\\site-packages\\PyQt6\\Qt6\\plugins\\platforms\\',
     'platforms'),
    ('.\\data' ,'data' ),
    ( '.\\resources', 'resources')
]

added_binaries = ['.\\helpers', '.\\models', '.\\ui' ]

a = Analysis(['main.py'],
             pathex=[
             'D:\\HIMO\\himopy',
             qt5_path, qt6_path,
             'D:\\HIMO\\himopy\helpers',
              'D:\\HIMO\\himopy\\models',
             'D:\\HIMO\\himopy\\ui',
             'D:\\HIMO\\himopy\\bin', 'D:\\HIMO\\himopy\\myo'],
             #binaries=[],
             binaries=[],
             datas=added_files,
             hiddenimports=collect_submodules('tensorflow_core') + [
             'h5py', 'h5py.defs', 'h5py.utils', 'h5py.h5ac', 'h5py._proxy', 'PyQt6.sip',
             'PyQt6.QtPrintSupport'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='HIMO',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='HIMO')
