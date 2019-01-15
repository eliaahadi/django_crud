from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.forms import ModelForm
from django.http import JsonResponse
from books_fbv.models import Book
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, YourCustomType):
            return str(obj)
        return super().default(obj)

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'pages']

def book_list(request, template_name='books_fbv/book_list.html'):
    book = Book.objects.all()
    data = {}
    data['object_list'] = book
    return render(request, template_name, data)

def book_create(request, template_name='books_fbv/book_form.html'):
    print('Raw Data: ')   
    form = BookForm(request.POST or None)
    if request.method == 'POST':
      jsondata = serialize('json', Book.objects.all(), cls=LazyEncoder) 
      print('Raw Data: ', request.body, request.body.decode("utf-8"), jsondata)  
    if form.is_valid():
        form.save()
        return redirect('books_fbv:book_list')
    return render(request, template_name, {'form':form})

def book_update(request, pk, template_name='books_fbv/book_form.html'):
    book= get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('books_fbv:book_list')
    return render(request, template_name, {'form':form})

def book_delete(request, pk, template_name='books_fbv/book_confirm_delete.html'):
    book= get_object_or_404(Book, pk=pk)    
    if request.method=='POST':
        book.delete()
        return redirect('books_fbv:book_list')
    return render(request, template_name, {'object':book})

def book_view(request, pk, template_name='books_fbv/book_detail.html'):
    book= get_object_or_404(Book, pk=pk)    
    return render(request, template_name, {'object':book})

def book_json_list(request,format=None):
    #  if request.method=='POST':
      # insert into databases
    book_data_list = serialize('json', Book.objects.all(), cls=LazyEncoder)
    return HttpResponse(book_data_list, content_type='application/json')
    # return JsonResponse(book_data, {'object':book_data},  safe=False)

def book_json_detail(request, pk, format=None):
    book_data_detail = serialize('json', Book.objects.filter(pk=pk),  cls=LazyEncoder)
    return HttpResponse(book_data_detail, content_type='application/json')