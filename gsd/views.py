from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from gsd.models import Todo, Tag, Context

def index(request):
    if request.is_ajax():
        if request.method == 'GET':
            message = "This is an XHR GET request"
        elif request.method == 'POST':
            message = ''
            if request.POST["operation"] == "checkoff":
                # handles checking and unchecking of todos
                pk = request.POST["todo"]
                change = request.POST["change"]
                try:
                    todo = Todo.objects.get(pk=pk)
                    if change == 'check':
                        todo.is_done = True
                        message = "Todo #" + str(pk) + " has been checked"
                    elif change == 'uncheck':
                        todo.is_done = False
                        message = "Todo #" + str(pk) + " has been unchecked"
                    else:
                        message = "Warning: Todo identified, but unchanged"
                    todo.save()
                except DoesNotExist:
                    message = "Error: moved todo doesn't exist"
                    
            elif request.POST["operation"] == "bin change":
                # handles dragging todos between bins
                pk = request.POST["todo"]
                bin = request.POST["list"]
                try:
                    todo = Todo.objects.get(pk=pk)
                    todo.bin = bin
                    todo.save()
                    message = "Successfully saved bin change for todo #" + str(pk)
                except DoesNotExist:
                    message = "Error: Moved todo doesn't exist"
                    
            elif request.POST["operation"] == "creation":
                # handles making a new Todo
                print "Creating todo"
                data = request.POST
                print request.POST
                name = data["todoName"]
                due_date = data["todoDueDate"]
                raw_context = data["todoContext"]
                
                tags_raw = data["todoTagList"]
                print tags_raw
                # make tags lowercase, remove spaces, 
                # and split on commas into a list
                tag_names = tags_raw.lower().replace(' ','').split(',')
                tags_objects = []
                
                for tag in tag_names:
                    t = Tag.objects.get_or_create(name=tag)
                    tags_objects.append(t)
                
                print "Successfully made tag list"
                
                context = None
                if raw_context != "None":
                    context = Context.objects.get(name=raw_context)
                    
                # let's make the new todo!
                # all new todos start in 'someday'
                todo = Todo(name=name,context=context,bin='someday')
                todo.save()
                # add tags to new todo
                
                if tag_objects:
                    for tag in tag_objects:
                        todo.tags.add(tag)
                    todo.save()
                
                print "Success"
                print "Successfully saved new todo #" + str(todo.pk)
                
                message = str(todo.pk)
                
            elif request.POST["operation"] == "deletion":
                # handles deletion of todos
                pk = request.POST["todo"]
                try:
                    todo = Todo.objects.get(pk=pk)
                    todo.delete()
                    message = "Successfully deleted todo #" + str(pk)
                except DoesNotExist:
                    message = "Error: Deleted todo doesn't exist"
        return HttpResponse(message)
    else:
        todos_today = Todo.objects.filter(bin='today')
        todos_upcoming = Todo.objects.filter(bin='soon')
        todos_someday = Todo.objects.filter(bin='someday')
        
        Tag.clean()
        tags = Tag.objects.all()
        contexts = Context.objects.all()
        
        return render_to_response('index.html', {'tags' : tags, 'todos_today' : todos_today, 'todos_upcoming' : todos_upcoming, 'todos_someday' : todos_someday, 'contexts' : contexts }, context_instance=RequestContext(request))
