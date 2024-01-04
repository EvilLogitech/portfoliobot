from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
imgdir = BASE_DIR / 'images'


def get_pictures_filenames(dirname):
    filepath = imgdir / dirname
    images = sorted([x for x in filepath.iterdir() if x.is_file()])
    return images


def get_all_pictures():

    def walk(filepath):
        images = []
        for filename in filepath.iterdir():
            if filename.is_file():
                images.append(filename)
            else:
                images.extend(walk(filename))
        return images
    return walk(imgdir)


def split_list(list_, length=2):

    def inner(arr, n):
        for i in range(0, len(arr), n):
            yield list_[i: i + n]
    return list(inner(list_, length))
