import os


def getProjectPath():
    filepath = os.path.abspath(__file__)
    dir_path = os.path.dirname(filepath)
    return dir_path + '/'
