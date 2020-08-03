import random


class ScrapperObj:
    def __init__(self, name, obj):
        self.name = name
        self.obj = obj


class ScrapperObjectFactory:
    def __init__(self):
        self._builders = []
        self._builders_options = []
        self._builders_historicalquotes = []

    def register_builder(self, key, builder):
        self._builders.append(ScrapperObj(key, builder))

    def register_options_builder(self, key, builder):
        self._builders_options.append(ScrapperObj(key, builder))

    def register_historicalquotes_builder(self, key, builder):
        self._builders_historicalquotes.append(ScrapperObj(key, builder))

    def create(self, key, **kwargs):
        choice = None
        if(key == None):
            choice = random.choice(self._builders)
        else:
            for x in self._builders:
                if x.name == key:
                    choice = x

        if choice == None:
            print("couldnt find a scrapper with key:  " + key)
            choice = random.choice(self._builders)

        return choice.obj, choice.name

    def createOption(self, key, **kwargs):
        choice = random.choice(self._builders_options)
        return choice.obj, choice.name

    def createHistoricalQuote(self, key, **kwargs):
        choice = random.choice(self._builders_historicalquotes)
        return choice.obj, choice.name
