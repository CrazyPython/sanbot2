class MarkovEngine(object):
    def __init__(self, corpus):
        raise NotImplementedError

    def reply(self):
        raise NotImplementedError


class Cobe(MarkovEngine):
    def __init__(self, corpus):
        from cobe.brain import Brain
        self._brain = Brain(corpus)
