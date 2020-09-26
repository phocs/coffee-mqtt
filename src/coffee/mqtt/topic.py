from .pattern import TopicPattern

class Topic:
    def __init__(self, pattern: str=""):
        self.pattern = pattern

    @property
    def topic(self):
        return self.__topic

    @topic.setter
    def topic(self, topic: str):
        pass

    @property
    def pattern(self):
        return self.__pattern

    @pattern.setter
    def pattern(self, pattern):
        self.__pattern = pattern
        self.__topic = TopicPattern.clean(pattern)

    def match(self, topic: str):
        return TopicPattern.matches(self.pattern, topic)

    def extract(self, topic: str):
        return TopicPattern.extract(self.pattern, topic)

    def build(self, params):
        return TopicPattern.fill(self.pattern, params)
