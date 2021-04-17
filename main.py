import spacy

def extractDependecyRelFromRoot(sentence):

    doc = nlp(sentence)
    for sent in doc.sents:
        for token in sent:
            dependencyRelList = []
            tmp = token
            while(tmp.dep_ != 'ROOT'):
                dependencyRelList.insert(0, tmp.text)
                dependencyRelList.insert(0, "--{}-->".format(tmp.dep_))
                tmp = tmp.head
            dependencyRelList.insert(0, tmp.text)
            dependencyRelList.insert(0, "--root-->")
            print(dependencyRelList)


# from wikipedia: A subtree of a tree T is a tree consisting of a node in T and all of its descendants in T.

def extractSubtree(sentence, inputWord):
    subtreeList = []
    doc = nlp(sentence)
    for sent in doc.sents:
        subtreeRoot = [token for token in doc if token.text == inputWord][0]
        for descendant in subtreeRoot.subtree:
            subtreeList.append(descendant.text)

    return subtreeList


def checkSubtree(sentence, listOfWords):
    listOfWords.sort()
    for word in listOfWords:
        subtree = extractSubtree(sentence, word)
        subtree.sort()
        if subtree == listOfWords:
            return True
    return False


def headOfSpan(sequenceOfWords):
    doc = nlp(sequenceOfWords)
    span = doc[0:len(doc)]
    return span.root.text


def extractInfo(sentence):
    infoDict = {}
    doc = nlp(sentence)
    for sent in doc.sents:
        for token in sent:
            spanList = []
            if token.dep_ == 'nsubj' or token.dep_ == 'dobj' or token.dep_ == 'iobj':
                for descendant in token.subtree:
                    spanList.append(descendant.text)
                spanList = ' '.join(spanList)
                infoDict[token.dep_] = spanList

    return infoDict


sentence = 'I saw the man with a telescope.'

nlp = spacy.load('en_core_web_sm')
doc = nlp(sentence)

extractDependecyRelFromRoot(sentence)
print("\n")
for token in doc:
    print(extractSubtree(sentence, token.text))
print("\n")

isSubtree = checkSubtree(sentence, ["saw", "the", "man", "with", "a", "telescope"])
print(isSubtree)
print("\n")

print(headOfSpan('man with a telescope.'))
print("\n")

print(extractInfo(sentence))
