import os

paths = {  # Почему-то именно в _default_paths отправляет, вместо root directory ¯\_(ツ)_/¯
    'screenshots': str(os.path.dirname(os.path.abspath(__file__))) + "\\..\\reports\\screenshots\\",
    'reports': str(os.path.dirname(os.path.abspath(__file__))) + "\\..\\reports\\logs\\",
    'root': str(os.path.dirname(os.path.abspath(__file__))) + "\\..\\",
    'config': str(os.path.dirname(os.path.abspath(__file__))) + "\\..\\config\\"
}


def create_paths():
    for path in paths:
        if not os.path.exists(paths[path]):
            os.makedirs(paths[path])


create_paths()
