from django.db import models
import datetime

color_list = ['ffeedd','d9e9ff','f9aa9f','cceeee','9fefba']

class Tag(models.Model):
    '''Model for all tags on todos'''
    name = models.CharField(max_length=100, unique=True)
    
    @staticmethod
    def clean():
        '''checks if any issue out there is using the tag--if not, it deletes itself'''
        for tag in Tag.objects.all():
            if not tag.todo_set.all():
                tag.delete()
    
    def __unicode__(self):
        return self.name
        
    class Meta:
        ordering = ['name']
        
class Context(models.Model):
    '''Model for contexts in which todos can reside'''
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=6,default='e9e9e9')
    
    def select_color(self):
        color = ''
        try:
            color = color_list[self.pk-1]
        except IndexError:
            # if we're out of colors in the list
            color = 'cadaff'
        self.color = color
        
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        
class Todo(models.Model):
    '''Model for todos'''
    name = models.CharField(max_length=200)
    context = models.ForeignKey('Context',blank=True,null=True)
    is_done = models.BooleanField(default=False)
    due_date = models.DateField(blank=True,null=True)
    tags = models.ManyToManyField('Tag', blank=True, null=True)
    bin_choices = (
        ('today','today'),
        ('soon','soon'),
        ('someday','someday'),
    )
    bin = models.CharField(max_length="10",choices=bin_choices,default='someday')
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['due_date','context','name']
    
    def is_due_today(self):
        now = datetime.date.today()
        return now == self.due_date
    
    def is_overdue(self):
        now = datetime.date.today()
        return now > self.due_date