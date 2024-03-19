from django.shortcuts import render
from django.http import HttpResponse
from .models import Todo
from django.template import loader
from django.shortcuts import get_list_or_404, get_object_or_404
from django.shortcuts import redirect
from .forms import TodoForm
from .forms import Ajout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def index(request):
    taches = Todo.objects.all().order_by('id')

    return render(request, "todo/index.html",  {"taches":taches})


def record(request, pk):

    return HttpResponse(f'Page {pk}')


def affich_details(request,id):
    todo=get_object_or_404(Todo, id=id)
    return render(request,"todo/affich_details.html", {"todo":todo})


def delete(request, pk):
    tache = Todo.objects.get(id=pk)
    tache.delete()
    return redirect('index') 


def ajout(request):
    if request.method == "POST":
        form=Ajout(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ajout reussie")
            return redirect ('index')
        else:
            messages.error(request, 'error')
            return redirect('index')               
    else:
         
        form=Ajout()
        return render(request, "todo/ajout.html", {"form":form, })

        
    


def update(request, pk):
    todo=Todo.objects.get(id=pk)
    if request.method=="POST": 

        form=TodoForm(data=request.POST, instance=todo)
        if form.is_valid():
          form.save()
          messages.success(request, "Modification reussie")
          return redirect ('index')
        else:
           
           return HttpResponse('error')

    else:
        form=TodoForm(initial={"name":todo.name})
        return render(request, "todo/update.html", {"form":form,"todo":todo})
    

def login_user(request): 
    if request.method == "POST": 
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None: 
                login(request, user)
                messages.success(request, "Connexion reussie")
                return redirect(index)
            else: 
                messages.error(request,"Connexion echoué")
                return redirect('login_user')
        
    else: 
        form = AuthenticationForm()
        return render(request, "todo/login.html", {"form":form})
    
def logout_user(request):
    logout(request)
    return redirect(login_user)



def register_user(request):
    if request.method == 'POST':
        form =  UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('index')  # Redirect to login page after successful registration
    else:
        form =  UserCreationForm()

    return render(request, 'todo/register.html', {'form': form})