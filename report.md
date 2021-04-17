# Report

The following functions are tested with `sentence = 'I saw the man with a telescope.' `

## extractDependecyRelFromRoot(sentence)
The function takes in input a sentence and print the relations between each token in the sentence from the root to the token (eg. `['--root-->', 'saw', '--dobj-->', 'man', '--det-->', 'the']`).
To do that the sentence is first parsed and a doc object is obtained. Then two nested for loops are used to access every token. To obtain the dependency relation of the token is enough to access its attribute `token.dep_`.

```python
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
```

## extractSubtree(sentence, inputWord)
The function takes as input a sentence and a string and return the subtree of that word contained in the sentence.
Since: "A subtree of a tree T is a tree consisting of a node in T and all of its descendants in T." the function returns the subtree of the input word in sentence order, input word included.
To do that the sentence is parsed and the root of the subtree corresponding to the `inputWord` is obtained through the function `subtreeRoot = [token for token in doc if token.text == inputWord][0]`. Then it is possible to access at the nodes of the subtree cycling over the `subtreeRoot.subtree`.

```python
def extractSubtree(sentence, inputWord):
    subtreeList = []
    doc = nlp(sentence)
    for sent in doc.sents:
        subtreeRoot = [token for token in doc if token.text == inputWord][0]
        for descendant in subtreeRoot.subtree:
            subtreeList.append(descendant.text)

    return subtreeList
```

An output example is:

```python
>>> print(extractSubtree(sentence, 'with'))
['with', 'a', 'telescope']
```

## checkSubtree(sentence, listOfWords)
The function takes as input a sentence and a list of words. The list is sorted and in order to check if the given list rapresent a tree, a for loop is made cycle over all the possible trees with root as one of the words in the list. Then the subtree is obtained exploiting `extractSubtree()` function by passing it the sentence and the word on which the for loop is cycling over. If the sorted subtree and the list are the same the function will return `True`, `False` otherwise.

```python
def checkSubtree(sentence, listOfWords):
    listOfWords.sort()
    for word in listOfWords:
        subtree = extractSubtree(sentence, word)
        subtree.sort()
        if subtree == listOfWords:
            return True
    return False
```

## headOfSpan(sequenceOfWords)
Takes as input a sequence of word and return the root of that words.
The sequence is passed to the nlp parser which returns a doc element, then a span element can be obtained by selecting the desidered elements as in a list (in this case all elements). The span object has an attribute root that is used to return the root.

```python
def headOfSpan(sequenceOfWords):
    doc = nlp(sequenceOfWords)
    span = doc[0:len(doc)]
    return span.root.text
```

An output example is:

```python
>>> print(headOfSpan('man with a telescope.'))
'man'
```

## extractInfo(sentence)
Takes as input a sentence and returns a dictionary containing as key the relation (`'nsubj'`, `'dobj'`, `'iobj'`) and as value a list containing the words related to the key.
In order to do that the sentence is parsed and for every token, if the dependency relation is one of the key above, a list containing the subtree of the token is populated. Then the list is joined in order to have one single string. Afterwards the list is loaded on the dictionary.

```python
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
```
An output example is:

```python
>>> print(extractInfo(sentence))
{'nsubj': ['I'], 'dobj': ['the', 'man']}
```

Complete output example:
```python
['--root-->', 'saw', '--nsubj-->', 'I']
['--root-->', 'saw']
['--root-->', 'saw', '--dobj-->', 'man', '--det-->', 'the']
['--root-->', 'saw', '--dobj-->', 'man']
['--root-->', 'saw', '--prep-->', 'with']
['--root-->', 'saw', '--prep-->', 'with', '--pobj-->', 'telescope', '--det-->', 'a']
['--root-->', 'saw', '--prep-->', 'with', '--pobj-->', 'telescope']
['--root-->', 'saw', '--punct-->', '.']


['I']
['I', 'saw', 'the', 'man', 'with', 'a', 'telescope', '.']
['the']
['the', 'man']
['with', 'a', 'telescope']
['a']
['a', 'telescope']
['.']


False


man


{'nsubj': 'I', 'dobj': 'the man'}
```