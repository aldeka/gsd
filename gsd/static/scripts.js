$("#clear-link").live('click', function(event) {
    var checkSet = $('.checked');
    checkSet.each(function() {
        var pk = $(this).attr('id').slice(5);
        $.post("/", { 
            operation: "deletion",
            todo: pk,
        },
            function(data) {
                console.log(data);
            }
        );
        $(this).remove();
    });
    event.preventDefault();
});

$(".delete-link").live('click', function(event) {
    $(this).parent().remove();
    var pk = $(this).parent().attr('id').slice(5);
    $.post("/", { 
        operation: "deletion",
        todo: pk,
    },
        function(data) {
            console.log(data);
        }
    );
    event.preventDefault();
});

$(".check-link").live('click', function(event) {
    $(this).parent().toggleClass("checked");
    var pk = $(this).parent().attr('id').slice(5);
    var change = '';
    
    if ($(this).parent().hasClass('checked')) {
        change = 'check';
    }
    else {
        change = 'uncheck';
    }
    
    $.post("/", { 
        operation: "checkoff",
        todo: pk,
        change: change,
    },
        function(data) {
            console.log(data);
        }
    );
    return false;
});

function todoGeneratorOld(pk, todoText) {
    return '<li id="todo-' + pk.toString() + '" class="todo"><span contenteditable="true">' + todoText + '</span> -- <a href="" class="check-link">check</a> -- <a href="" class="delete-link">X</a></li>';
};

function todoGenerator(pk, todoText, todoDueDate, todoOverdue, todoContext, todoContextColor, todoTagsList) {
    // le default values setup
    if (!todoDueDate) {
        todoDueDate = '--';
    }
    if (!todoOverdue) {
        todoOverdue = '';
    }
    if (!todoContext) {
        todoContext = '--';
        todoContextColor='e9e9e9';
    }
    if (!todoTagsList) {
        todoTagsList = [];
    }
    
    var tags = '';
    var tagClasses = '';
    _.each(todoTagsList,function(tag){
        tags = tags + tag + ' ';
        tagClasses = tags + 'tag-' + tag + ' ';
    });
    
    if (tags == '') {
        tags = '--';
    }

    return '<li id="todo-' + pk.toString() + '" class="todo ' + tagClasses + '" style="background-color: #' + todoContextColor + ';"><a href="" class="check-link">&nbsp;</a> <span class="todo-name">' + todoText + '</span> <a href="" class="delete-link">x</a><div class="todo-metadata"><span class="todo-meta-item duedate ' + todoOverdue + '"><span class="icon duedate-icon">Due</span> ' + todoDueDate + ' </span> <span class="todo-meta-item context"><span class="icon context-icon">C</span> ' + todoContext + '</span> <span class="todo-meta-item tags"><span class="icon tags-icon">T</span> ' + tags + ' </span></div></li>';
        
}

$("#add-new-form").live('submit', function(event) {
    event.preventDefault();
    console.log('clicked submit');
    var newTodoName = $("#new-todo-name").val();
    var newTodoContext = $("#new-todo-context").val();
    var newTodoDeadline = $("#new-todo-deadline").val();

    // the tags still need to be trimmed / cleaned up
    var newTodoTagsRaw = $("#new-todo-tags").val();
    
    var pk = 0;
    
    $.post("/", { 
        operation: "creation",
        todoName: newTodoName,
        todoDueDate: newTodoDeadline,
        todoContext: newTodoContext,
        todoTagList: newTodoTagsRaw,
    },
        function(data) {
            console.log('receiving reply data');
            console.log(data);
            var id = parseInt(data['pk']);
            var name = data['name'];
            
            $("#someday-todos").append(todoGenerator(id, name));
            $(".new-todo").val("");
        }
    );
    
    
});

$(document).ready(function() {
    $(function() {
        $( "#new-todo-duedate" ).datepicker();
    });
    $( "#upcoming-todos, #todays-todos, #someday-todos" ).sortable({
            connectWith: ".todo-list",
            beforeStop: function(event, ui) { 
                // get the pk of the moved todo
                var pk = ui.item.attr('id').slice(5);
                // get where the todo was moved to
                var newList = ui.item.parent('ul').attr('id');
                
                // converts id names to model's bin choices
                var list = ''
                if (newList == 'todays-todos') {
                    list = "today";
                }
                else if (newList == 'upcoming-todos') {
                    list = "soon";
                }
                else if (newList == 'someday-todos') {
                    list = "someday";
                }
                
                // check that this is a real todo, not a fake one that wasn't saved properly
                if (!(pk == 0))
                {
                    // let's send the change to the server                
                    $.post("/", { 
                        operation: "bin change",
                        todo: pk,
                        list: list,
                    },
                        function(data) {
                            console.log(data);
                        }
                    );
                }
            }
        }).disableSelection();
});


/* giant ajax-and-django handling function of doom */
$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});
