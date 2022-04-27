from toiney.core.extensions.abstractextensions import AbstractExtensions
import os


class Photoset:
    def __init__(self, path="", name="", photos=None):
        self.path = path
        self.name = name
        self.photos = list(photos)
        self.abstractext = AbstractExtensions()

    def get_photo(self):
        result = ""
        # VB code: SyncLock obj -- would be here, mark out for now
        if len(self.photos) <= 0:
            result = ""
        else:
            result = self.abstractext.try_take(appender=False, target=self.photos)
        return result

    def is_valid(self) -> bool:
        if os.path.isdir(self.path):
            pic_count = [x for x in os.listdir(self.path) if x.endswith((".jpeg", ".jpg", ".png"))]
            if len(pic_count) > 0:
                print(pic_count)
                return True
            else:
                return False
        else:
            return False

    def importer(self):
        path = self.path
        files = [x for x in os.listdir(path) if x.endswith((".jpeg", "jpg", ".png"))]
        if len(files) < 0:
            return None
        return vars(Photoset(path, os.path.dirname(path), files))


if __name__ == '__main__':
    path = "C:/Users/calib/PycharmProjects/hi5/toiney/photosets"
    print(Photoset(path=path, photos=['Photoset']).importer())


