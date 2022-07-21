from django.shortcuts import render, redirect 
from django.contrib import messages
from django.utils import timezone
from datetime import date, datetime, timedelta

from .forms import TodoForm #local files
from .models import Todo
 
###############################################
 
def index(request):
    item_list = Todo.objects.order_by("date")
    my_item_list = item_list
    for point in my_item_list:
        point.date += timedelta(hours=2)

        timeDelta = timezone.now() + timedelta(hours=2) - point.date 
        hours, remainder = divmod(timeDelta.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours <-3 or hours >3:
            point.until = str(int(-hours)) + "h"
        elif hours == 0:
            point.until = str(int(-minutes)) + "min"
        else:
            point.until = "{:02}h {:02}min".format(int(hours), int(minutes))
            
        if hours < 0 or minutes < 0:
            point.stat = "left"
            point.style = "background: white;"
        else:
            point.stat = "OVER"
            point.style = "background: red;"

        point.date = point.date.strftime("%H:%M // %d.%m")

    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todo')
    form = TodoForm()
 
    page = {
             "forms" : form,
             "todo_list_elements" : my_item_list,
             "title" : "ToDo",
           }
    return render(request, 'todo/index.html', page)
 
 
 
### function to remove item, it receive todo item_id as primary key from url ##
def remove(request, item_id):
    item = Todo.objects.get(id=item_id)
    item.delete()
    messages.info(request, "item removed")
    return redirect('todo')