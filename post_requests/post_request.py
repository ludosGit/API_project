import requests
import os
print(os.getcwd())

url = "http://127.0.0.1:5000/mymovies"
data = {
    "genre": "drama",
    "title": "Inception",
    "rating": 4,
    "comment": "Good Nolan",
    "director": "Christopher Nolan",
    "year": 2010,
    "image": "post_requests\inception.jpg",
    "views": ["2021-10-15"]
}
files = {'image': open(data["image"], 'rb')}

response = requests.post(url, data=data, files=files)
print(response.json())