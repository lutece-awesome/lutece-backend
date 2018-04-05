from django.db import models

# Create your models here.

class Problem( models.Model ):
    problemId = models.AutoField( primary_key = True , db_index = True )
    title = models.CharField( max_length = 256 , db_index = True , default = 'Default Title' )
    content = models.CharField( max_length = 58000 , blank = True )
    standardInput = models.CharField( max_length = 1024 , blank = True )
    standardOutput = models.CharField( max_length = 1024 , blank = True )
    constraints = models.CharField( max_length = 1024 , blank = True )
    sampleInput = models.CharField( max_length = 1024 , blank = True )
    sampleOutput = models.CharField( max_length = 1024 , blank = True )
    sampleExplanation = models.CharField( max_length = 1024 , blank = True )
    resource = models.CharField( max_length = 256 , blank = True )
    timeLimit = models.PositiveIntegerField( default = 2000 )
    memoryLimit = models.PositiveIntegerField( default = 128 )
    solvedNumber = models.PositiveIntegerField( default = 0 , editable = False )
    tryNumber = models.PositiveIntegerField( default = 0 , editable = False )
    specialJudge = models.BooleanField( default = False )
    visible = models.BooleanField( default = False )

    def __str__(self):
        return self.title

    def toDict(self):
        return {
            'ProblemId' : self.problemId,
            'title' : self.title,
            'content' : self.content,
            'standardInput' : self.standardInput,
            'standardOutput' : self.standardOutput,
            'constraints' : self.constraints,
            'sampleInput' : self.sampleInput,
            'sampleOutput' : self.sampleOutput,
            'sampleExplanation' : self.sampleExplanation,
            'resource' : self.resource,
            'timeLimit' : self.timeLimit,
            'memoryLimit' : self.memoryLimit,
            'solvedNumber' : self.solvedNumber,
            'tryNumber' : self.tryNumber,
            'specialJudge' : self.specialJudge,
            'visible' : self.visible
        }