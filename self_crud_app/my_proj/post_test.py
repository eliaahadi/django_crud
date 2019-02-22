
import requests

url ="http://localhost:8000/books_fbv/api/"

data = 
[
  {
    "model": "books_fbv.book", "pk": 100, "fields": {"name": "Catch 22", "pages": 300}
  }
]

headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
r = requests.post(url, headers=headers, json=data, timeout=5.0)

print(r)
print(r.content)