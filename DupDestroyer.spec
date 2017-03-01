# -*- mode: python -*-

block_cipher = None


a = Analysis(['C:\\Users\\Maste\\_My Stuff\\PycharmProjects\\DupDestroyer\\__init__.py'],
             pathex=['C:\\Users\\Maste\\Python\\Python27', 'C:\\Users\\Maste\\Python\\Python27\\Lib', 'C:\\Users\\Maste\\Python\\Python27\\libs', 'C:\\Users\\Maste\\Python\\Python27\\Scripts', 'C:\\Users\\Maste\\_My Stuff\\PycharmProjects\\DupDestroyer\\venv', 'C:\\Users\\Maste\\_My Stuff\\PycharmProjects\\DupDestroyer\\venv\\Lib', 'C:\\Users\\Maste\\_My Stuff\\PycharmProjects\\DupDestroyer\\venv\\Scripts', 'C:\\Users\\Maste\\_My Stuff\\PycharmProjects\\DupDestroyer\\venv\\Lib\\site-packages', 'C:\\Users\\Maste\\_My Stuff\\PycharmProjects\\DupDestroyer'],
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
          name='DupDestroyer',
          debug=False,
          strip=False,
          upx=True,
          console=True )
