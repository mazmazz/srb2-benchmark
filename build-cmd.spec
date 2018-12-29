# -*- mode: python -*-

# NOTE: IN srb2benchmark.py, COMMENT OUT THIS LINE, OR ELSE YOUR EXE WILL INCLUDE GOOEY RESOURCES
# from gooey import Gooey, GooeyParser

#import gooey
#gooey_root = os.path.dirname(gooey.__file__)
#gooey_languages = Tree(os.path.join(gooey_root, 'languages'), prefix = 'gooey/languages')
#gooey_images = Tree(os.path.join(gooey_root, 'images'), prefix = 'gooey/images')

block_cipher = None


a = Analysis(['srb2benchmark.py'],
             binaries=[],
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
#          gooey_languages, # Add them in to collected files
#          gooey_images, # Same here.
          name='srb2benchmark_cmd',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True ) # False for no window, but no console commands
