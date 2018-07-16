from collections import Counter

SPECIAL_CHARS = '!"#$%&()*+,-./:;<=>?@[\]^_`─{|}~！，。 「」？、～12345678:《》：】【）『』'

def ngrams(article, n):
    output = []
    for i in range(len(article)-n+1):
        CLEAN = True
        for c in article[i:i+n]:
            if c in SPECIAL_CHARS:
                CLEAN = False
                break
        if CLEAN:
            output.append(article[i:i+n])
    return output


def get_new_words_new(article, maxlength=5):
    maxlength += 1
    ngram = []
    for i in range(maxlength+1):
        ngram.append(ngrams(article, i+1))

    article_length = len(ngram[0])
    min_count = max(article_length*5/1000, 3)

    ngram_counter = []
    for i in range(maxlength+1):
        ngram_counter.append(Counter(ngram[i]))

    ngram_counter_f = []
    threshold_array_ratio = [1.3] + [1]*maxlength
    for i in range(maxlength+1):
        ngram_counter_f.append({x : ngram_counter[i][x] for x in ngram_counter[i] if ngram_counter[i][x] >= min_count*threshold_array_ratio[i]})

    new_words = []
    n_m_gram_ratio = [0.75, 0.9] + [0.9]*(maxlength-1)
    for i in range(1, maxlength):
        # i+1 gram
        for word, count in ngram_counter_f[i].items():
            is_new = False
            for gram in ngrams(word, i):
                if ngram_counter_f[i][word] /ngram_counter[i-1][gram] > n_m_gram_ratio[i-1]:
                    is_new = True
                    if gram in new_words:
                        new_words.remove(gram)

            if is_new and len(word) < maxlength:
                new_words.append(word)

    return new_words
