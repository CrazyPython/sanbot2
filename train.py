import nltk

emma_sents = []

f = open('train.txt', 'w')

for fileid in ['humor', 'news', 'adventure', 'science_fiction', 'fiction']:
    emma_sents.extend(nltk.corpus.brown.sents(categories=fileid))


def join(array):
    result = ''
    for i in array:
        if i not in ', .,"/[]\+-)(*&^%$#@!~`<>:;{}|-_?' + "'":
            result += ' ' + i
        else:
            result += i
    result = result.strip()
    return result


for i in emma_sents:
    f.write(join(i) + '\n\n')

f.close()
