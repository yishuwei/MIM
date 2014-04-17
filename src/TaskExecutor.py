# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# TaskExecutor.py


from QuestionProcessor import *

class TaskExecutor(object):
    def __init__(self, taskName):
        self.taskName = taskName

    def Execute(self, session):
        return True
   
    def LogTaskCompletion(self, session):
        session.logs.append("Executed {0} task successfully.".format(self.taskName)) 


class Session(object):
    def __init__(self, question):
        self.questionProcessor = QuestionProcessor(question) 
        self.relevantDocuments = None
        self.relevantPassages = None
        self.answers = None
        self.maxNumberOfReturnedDocuments = 10
        self.logs = []

    def GetLogs(self):
        return "\n".join(self.logs) 

