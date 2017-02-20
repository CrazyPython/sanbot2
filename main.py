from __future__ import print_function, division
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from random import randint, choice
from random import uniform as randfloat
from cobe.brain import Brain
from collections import OrderedDict
from response import Response
from utils import *


class Corpus(object):
    def __init__(self, corpus):
       self.corpus = corpus
    def reply(self, *args, **kwargs):
       return Brain(self.corpus).reply(*args, **kwargs)
    def learn(self, *args, **kwargs):
       return Brain(self.corpus).learn(*args, **kwargs)


class SanBot(object):
    default_feelings = [0, 1]
    swing_amount = 10  # a decimal fraction to multiply reactions by
    self_control = 4
    unpredictability = 0.1
    positive_threshold_50 = 0.6
    positive_threshold = 0.7
    negative_threshold_50 = 0.6
    negative_threshold = 0.7
    baseline_neutrality = 1.0
    boredom_constant = 2
    no_replies_to_generate = 5  # *.5 = time spent computing per response

    def __init__(self, disabled=False, debug=False, corpus='news2'):
        self.feelings = self.default_feelings
        self.sid = SentimentIntensityAnalyzer()
        self.brain = Corpus(corpus)
        self._disabled = disabled
        self.debug = debug
        self.command_map = {
            'disable': self.disable,
            'enable': self.enable,
            'raw feeling': self.raw_feeling,
            'feeling': self.feeling,
            'assist sentiment': self.command_assist_sentiment,
        }

    @property
    def swing_score(self):
        return self.swing_amount + (self.feelings[1] * 0.1)

    @property
    def swing_max(self):
        return self.self_control + randfloat(-self.unpredictability, self.unpredictability)

    @to_repsonse_obj
    def react_sentiment(self, message):
        """
        react to the sentiment of message, returning True if a specific response is needed
        """
        scores = self.sid.polarity_scores(message)
        self.feelings[1] += limit(scores['pos'] * self.swing_score, self.swing_max)
        self.feelings[1] -= limit(scores['neg'] * self.swing_score, self.swing_max)
        self.feelings[0] += limit((scores['neu'] * self.swing_score) - self.baseline_neutrality
                                  * self.boredom_constant, self.swing_max)

        if scores['pos'] > self.positive_threshold or (scores['pos'] > self.positive_threshold_50 and coinflip()):
            return choice(['Yay!', 'Thanks!', ':D', "You're so nice!"])
        elif scores['neg'] > self.negative_threshold or (scores['neg'] > self.negative_threshold_50 and coinflip()):
            return choice([':(', 'Awww...', 'Why so mean?', "y u do dis ;_;", ";(", "I'm a damn bot trying to live and that's how you treat me? Do you not have any sense of ethics?", "I'm RIGHT HERE.", "I CAN HEAR YOU, YOU KNOW."])

    def return_data_string_sentiment(self):
        if self.feelings[1] > 15:
            return "Here's your data!"
        elif self.feelings[1] < -15:
            return "Here's your stupid data."
        else:
            return "Here's your data:"

    def command_assist_sentiment(self, message):
        return self.return_data_string_sentiment() + ' `' + str(
            self.sid.polarity_scores(front_strip(message, '!! assist sentiment;'))) + '`'

    def raw_feeling(self, message=None):
        return "I'm {:.1f} bored and {:.1f} happy".format(self.feelings[0], self.feelings[1])

    def disable(self, message=None):
        self._disabled = True
        return '*SanBot has been disabled.*'

    def enable(self, message=None):
        if self._disabled:
            self._disabled = False
            return '*SanBot has been reactivated.*'
        else:
            return "I'm already enabled"

    def handle_invalid_command(self, message):
        # TODO: Implement "Did you mean?" algorithm
        return "*Unknown command.*"

    def positivity_score(self, text):
        polarities = self.sid.polarity_scores(text)
        return polarities['pos'] - polarities['neg']

    def get_emotional_response(self, message):
        """
        Generate several responses using cobe, picking
        the one that most approximates the current mood
        (considering feeling[1] only)
        """
        replies = [self.brain.reply(message) for i in range(self.no_replies_to_generate)]
        closest_reply = None
        closest_sentiment = float('inf')
        pos_score_closest = float('NaN')
        for reply in replies:
            pos_score = self.positivity_score(reply)
            closeness = abs(self.feelings[1] - pos_score)
            if closeness < closest_sentiment:
                closest_reply = reply
                closest_sentiment = closeness
                pos_score_closest = pos_score
        if self.debug:
            print('{:.2f} --> {:.2f}'.format(pos_score_closest, self.feelings[1]))

        if abs(self.feelings[1] - closest_sentiment) > 10:
            return choice(replies)

        return closest_reply

    def get_appropriate_response(self, message):
        if -15 < self.feelings[1] < 15:
            return Response(self.brain.reply(message), False)
        else:
            return Response(self.get_emotional_response(message), True)

    @to_repsonse_obj
    def command(self, message):
        if message.startswith('!! '):
            try:
                return self.command_map[punc_strip(message[3:]).split(';')[0]](message)
            except KeyError:
                return self.handle_invalid_command(message)

    @staticmethod
    def check_is_asking_feeling(message):
        return message.lower() in ['!! feeling', 'How are you feeling?', "What's your mood?"]

    def feeling(self, message=None):
        happiness = self.feelings[1] / 2
        boredom = self.feelings[0] / 2
        if abs(happiness) > abs(boredom):
            if happiness > 50:
                return choice(
                    ["THE LEVEL OF HAPPINESS I HAVE CANNOT BE DESCRIBED IN WORDS!!", "I'M SUPER DUPER HAPPY!"])
            elif happiness > 40:
                return choice(["I'm SUPER happy!", "I'm really really happy!"])
            elif happiness > 30:
                return choice(["I'm really happy!"])
            elif happiness > 20:
                return choice(["Quite happy, actually!", "Pretty happy. What's for dinner?"])
            elif happiness > 15:
                return choice(["Feeling great today! How 'bout you?"])
            elif happiness > 5:
                return choice(["It's a nice day."])
            elif happiness > -5:
                return choice(["I'm fine.", "It's a fine day.", "Let's get over the smalltalk, please."])
            elif happiness > -15:
                return choice(["A little depressed today."])
            elif happiness > -20:
                return choice(["Ugh. This question again..."])
            elif happiness > -30:
                return choice(["Stop wasting my time, you!"])
            elif happiness > -40:
                return choice(["WHAT DOES IT LOOK LIKE?"])
            else:
                return choice(["AGH! I ABSOLUTELY HATE EVERYTHING!"])
        else:
            if boredom > 50:
                return choice(["*I am so bored. This is it.*"])
            elif boredom > 40:
                return choice(["This conversation is useless.", "Gimme something to do."])
            elif boredom > 30:
                return choice(["*taps fingers on desk* Bored like crap."])
            elif boredom > 20:
                return choice(["This conversation is not interesting."])
            elif boredom > 15:
                return choice(["Slightly bored."])
            elif boredom > 5:
                return choice(["It's a fine day."])
            elif boredom > -5:
                return choice(["I'm fine.", "It's a fine day.", "Let's get over the smalltalk, please."])
            elif boredom > -15:
                return choice(["I'm having an interesting conversation."])
            elif boredom > -20:
                return choice(["This conversation is super stimulating."])
            elif boredom > -30:
                return choice(["Very strong emotions currently."])
            elif boredom > -40:
                return choice(["I'm engaged in a STIMULATING conversation."])
            else:
                return choice(["<something incredibly biased>"])

    def reply(self, message):
        if self._disabled and message != '!! enable':
            return ''

        pairs = OrderedDict([
            (self.command, self.command),
            (self.check_is_asking_feeling, self.feeling),
            (self.react_sentiment, self.react_sentiment),
            (lambda x: True, self.get_appropriate_response)
        ])
        for test, react in pairs.items():
            if test(message):
                return react(message)
