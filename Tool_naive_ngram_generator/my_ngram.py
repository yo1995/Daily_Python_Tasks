from collections import defaultdict, deque, Counter


# adapted from http://pit-claudel.fr/clement/blog/an-experimental-estimation-of-the-entropy-of-english-in-50-lines-of
# -python-code/ which I used in my ECE 587 course hmwk
def markov_model(stream, model_order):
    model, stats = defaultdict(Counter), Counter()
    circular_buffer = deque(maxlen=model_order)

    for token in stream:
        prefix = tuple(circular_buffer)
        circular_buffer.append(token)
        if len(prefix) == model_order:
            stats[prefix] += 1
            model[prefix][token] += 1

    return model, stats


def finish_sentence(sentence, n, corpus):
    result_sentence = sentence
    model, stats = markov_model(corpus, n)
    curr_char = sentence[-1]
    i = 0
    if n > len(sentence):
        return ""  # just wont happen
    while curr_char != '!' and curr_char != '.' and curr_char != '?':
        temp_search_str = result_sentence[-n:]  # n-gram is n-i to deduct n
        curr_char = model[tuple(temp_search_str)].most_common(1)[0][0]  # should be the most
        # print(curr_char)
        result_sentence.append(curr_char)
        i = i + 1
        if i > 100:  # just ensure it is not a infinite loop!
            break

    # print(result_sentence)
    # print(len(result_sentence))
    return result_sentence
