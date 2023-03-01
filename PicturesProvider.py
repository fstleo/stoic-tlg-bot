import os


class PicturesProvider:

    def __init__(self, picture_name_template, path):
        self.path = path
        self.picture_name_template = picture_name_template

    def get(self, day):
        return open(os.path.join(self.path,
                                 self.picture_name_template.format(day.month,
                                                                   day.day)), 'rb')
