# Self  Created App
- Followed the [tutorial here](https://rayed.com/posts/2018/05/django-crud-create-retrieve-update-delete/)

## Create app
- Follow the commands below
```
$ pip install django
$ django-admin startproject my_proj
$ cd my_proj
my_proj $ python3 manage.py startapp books 
```
- Upate my_proj/settings.py
```
INSTALLED_APPS = (
    :
    'books',
    :
)
```

## Create model
- Update the books/models.py file
```
from django.db import models
from django.urls import reverse

class Book(models.Model):
    name = models.CharField(max_length=200)
    pages = models.IntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('book_edit', kwargs={'pk': self.pk})
```
- Also update the settings to use MYSQL instead of sqlite myproj/settings.py
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.path.join(BASE_DIR, 'db.mysql'),
    }
}
```
- Run the migrations
```
my_proj $ python3 manage.py makemigrations
my_proj $ python3 manage.py migrate 
```
## Admin interface
- Update books/admin.py
```
from django.contrib import admin
from books.models import Book

admin.site.register(Book)
```
## Class based views
- First Django Class-based views to create our app pages, the file books/views.py
```
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from books.models import Book

class BookList(ListView):
    model = Book

class BookView(DetailView):
    model = Book

class BookCreate(CreateView):
    model = Book
    fields = ['name', 'pages']
    success_url = reverse_lazy('book_list')

class BookUpdate(UpdateView):
    model = Book
    fields = ['name', 'pages']
    success_url = reverse_lazy('book_list')

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('book_list')
```
## Define URLs
- Create books/urls.py
```
from django.urls import path

from . import views

urlpatterns = [
    path('', views.BookList.as_view(), name='book_list'),
    path('view/<int:pk>', views.BookView.as_view(), name='book_view'),
    path('new', views.BookCreate.as_view(), name='book_new'),
    path('view/<int:pk>', views.BookView.as_view(), name='book_view'),
    path('edit/<int:pk>', views.BookUpdate.as_view(), name='book_edit'),
    path('delete/<int:pk>', views.BookDelete.as_view(), name='book_delete'),
]
```
- Update my_proj/urls.py
```
# Make sure you import "include" function
from django.urls import include

urlpatterns = [
    :
    path('books/', include('books.urls')),
    :
]
```
## Templates
- Create books/templates/books/book_list.html
```
<h1>Books</h1>

<table border="1">
<thead>
    <tr>
    <th>Name</th>
    <th>Pages</th>
    <th>View</th>
    <th>Edit</th>
    <th>Delete</th>
    </tr>
</thead>
<tbody>
    {% for book in object_list %}
    <tr>
    <td>{{ book.name }}</td>
    <td>{{ book.pages }}</td>
    <td><a href="{% url "book_view" book.id %}">view</a></td>
    <td><a href="{% url "book_edit" book.id %}">edit</a></td>
    <td><a href="{% url "book_delete" book.id %}">delete</a></td>
    </tr>
    {% endfor %}
</tbody>
</table>

<a href="{% url "book_new" %}">New</a>
```
- Create books/templates/books/book_detail.html
```
<h1>Book Details</h1>
<h2>Name: {{object.name}}</h2>
Pages: {{ object.pages }}
```
- Create books/templates/books/book_form.html
```
<h1>Book Edit</h1>
<form method="post">{% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Submit" />
</form>
```
- Create books/templates/books/book_confirm_delete.html
```
<h1>Book Delete</h1>
<form method="post">{% csrf_token %}
    Are you sure you want to delete "{{ object }}" ?
    <input type="submit" value="Submit" />
</form>
```
## Create superuser
```
my_proj $ python3 manage.py createsuperuser
```
## Test it
```
my_proj $ python3 manage.py runserver
```

## CRUD Check
- While doing the CRUD operations on the website, check the SQLite database to see if those changes took place.
```
$ sqlite3
sqlite> .open /Users/eliaahadi/django_crud/self_crud_app/my_proj/db.sqlite3
sqlite> .database
sqlite> .table
sqlite> select * from books_book;
sqlite> INSERT INTO books_book (name, pages) VALUES ('Ryu','500');
```
## Function based views
- Update these two files and run the tests again (this is the preferred method)
- In books/views.py:
```
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm

from books.models import Book

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'pages']

def book_list(request, template_name='books/book_list.html'):
    book = Book.objects.all()
    data = {}
    data['object_list'] = book
    return render(request, template_name, data)

def book_view(request, pk, template_name='books/book_detail.html'):
    book= get_object_or_404(Book, pk=pk)    
    return render(request, template_name, {'object':book})

def book_create(request, template_name='books/book_form.html'):
    form = BookForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request, template_name, {'form':form})

def book_update(request, pk, template_name='books/book_form.html'):
    book= get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request, template_name, {'form':form})

def book_delete(request, pk, template_name='books/book_confirm_delete.html'):
    book= get_object_or_404(Book, pk=pk)    
    if request.method=='POST':
        book.delete()
        return redirect('book_list')
    return render(request, template_name, {'object':book})
```
And this file books/urls.py:
```
from django.urls import path

from books import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('view/<int:pk>', views.book_view, name='book_view'),
    path('new', views.book_create, name='book_new'),
    path('edit/<int:pk>', views.book_update, name='book_edit'),
    path('delete/<int:pk>', views.book_delete, name='book_delete'),
]
```