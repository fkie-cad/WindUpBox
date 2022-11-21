from pathlib import Path
import os




if __name__ == '__main__':
    appdata_path = Path(os.getenv('APPDATA'))
    print(appdata_path.is_dir())
    print(appdata_path.absolute().as_posix())



