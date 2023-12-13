import os


imgdir = 'images'


def get_picture(filename):
    filepath = os.path.join(imgdir, filename)
    with open(filepath, 'rb') as picture:
        return picture
