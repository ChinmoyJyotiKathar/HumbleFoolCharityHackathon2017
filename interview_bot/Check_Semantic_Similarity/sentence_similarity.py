import spacy


def imp_words(doc,nlp):
    tags = ['NOUN', 'PROPN', 'VERB']
    doc_nouns = nlp(" ".join([str(t) for t in doc if t.pos_ in tags]))
    return doc_nouns

def find_similarity(sent1,sent2,nlp):

	# print(sent1," -> ",type(sent1))
	# print(sent2," -> ",type(sent2))
	sent1 = nlp(sent1)
	sent2 = nlp(sent2[0])
	sent1_no_stop_words = imp_words(nlp(' '.join([str(t) for t in sent1 if not t.is_stop])),nlp)
	sent2_no_stop_words = imp_words(nlp(' '.join([str(t) for t in sent2 if not t.is_stop])),nlp)

	return(sent1_no_stop_words.similarity(sent2_no_stop_words))