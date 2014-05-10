from QuestionFeatureFactory import QuestionFeatureFactory
from SystemEvaluator import GetAllQuestions
from nltk.classify import SklearnClassifier
from sklearn.svm import SVC
import sys, pickle

class SimpleQuestion(object):
    def __init__(self, id, text):
        self.id = id
        self.text = text
    def GetWordList(self):
        return self.text.split()

# Use UIUC data to train a classifier
def GenerateClassifier():
    label = {}
    with open("../processed/gold_uiuc.txt") as uiucLabelFile:
        for line in uiucLabelFile:
            line = line.split()
            label[line[0]] = line[1] + ":" + line[2]

    trainData = []    
    ii = 0
    factory = QuestionFeatureFactory()
    factory.setMode("UIUC")
    with open("../processed/tokenized_uiuc.txt") as uiucFile:
        for line in uiucFile:
            ii += 1
            qid = '{0:04}'.format(ii)
            question = SimpleQuestion(qid, line.strip())
            features = factory.GetAllFeatures(question)
            trainData.append( (features, label[qid]) )

    classifier = SklearnClassifier(SVC(kernel="linear")).train(trainData)
    with open("QuestionClassifier.svm", "wb") as classiFile:
        pickle.dump(classifier, classiFile)


# Test the classifier on TREC data
def TestClassifier(TRECYear):
    label = {}
    with open("../processed/gold_" + TRECYear + ".txt") as trecLabelFile:
        for line in trecLabelFile:
            line = line.split()
            label[line[0]] = line[1]

    xmlPath = "/opt/dropbox/13-14/573/Data/Questions/training/TREC-" + TRECYear + ".xml"
    questions = GetAllQuestions(xmlPath)

    factory = QuestionFeatureFactory()
    factory.setMode("TREC")
    with open("QuestionClassifier.svm", "rb") as classiFile:
        classifier = pickle.load(classiFile)
        hit = 0
        for question in questions:
            features = factory.GetAllFeatures(question)
            prediction = classifier.classify(features)
            if prediction.split(":")[0] == label[question.id]:
                hit += 1
        return hit / float(len(questions))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        GenerateClassifier()
        print "Finish Training."
    else:
        acc = TestClassifier(sys.argv[1])
        print "Accuracy:", acc
