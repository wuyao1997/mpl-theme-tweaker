# hook-_internal_data.py
from PyInstaller.utils.hooks import copy_metadata
import os

# 手动添加任意文件夹到 _internal
source_dir = os.path.abspath("src/mpl_theme_tweaker/assets")
datas = [(source_dir, "mpl_theme_tweaker/assets")]
