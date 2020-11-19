# Content and tags into dict

def dicts(contents, tags):
    tag2idx = {}
    idx2tag = {}
    word2idx = {}
    idx2word = {}
    for tag_content in tags:
        for tag in tag_content:
            if tag not in tag2idx:
                tag2idx[tag] = len(tag2idx)
                idx2tag[len(idx2tag)] = tag
    for content in contents:
        for word in content:
            if word not in word2idx:
                word2idx[word] = len(word2idx)
                idx2word[len(idx2word)] = word
    word2idx['END'] = len(word2idx)
    idx2word[len(idx2word)] = 'END'
    tag2idx['END'] = len(tag2idx)
    idx2tag[len(idx2tag)] = 'END'
    return tag2idx, idx2tag, word2idx, idx2word