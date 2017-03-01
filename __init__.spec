# -*- mode: python -*-

block_cipher = None


a = Analysis(['C:\\Users\\Maste\\_My Stuff\\PycharmProjects\\DupDestroyer\\__init__.py'],
             pathex=[ r'C:\Users\Maste\Python\Python27\libs\', r'C:\Users\Maste\Python\Python27\Lib\site-packages', r'C:\\Users\\Maste\\_My Stuff\\PycharmProjects\\DupDestroyer'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='__init__',
          debug=False,
          strip=False,
          upx=True,
          console=True )
