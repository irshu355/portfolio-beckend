import random


class ScrapperObj:
    def __init__(self, name, obj):
        self.name = name
        self.obj = obj


class ScrapperObjectFactory:
    def __init__(self):
        self._builders = []
        self._builders_options = []

    def register_builder(self, key, builder):
        self._builders.append(ScrapperObj(key, builder))

    def register_options_builder(self, key, builder):
        self._builders_options.append(ScrapperObj(key, builder))

    def create(self, key, **kwargs):
        choice = random.choice(self._builders)
        return choice.obj, choice.name

    def createOption(self, key, **kwargs):
        choice = random.choice(self._builders_options)
        return choice.obj, choice.name
