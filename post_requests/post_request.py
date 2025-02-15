import requests
import os
print(os.getcwd())

url = "http://127.0.0.1:5000/mymovies"
data = {
    "genre": "anime",
    "title": "Ghost in the Shell",
    "rating": 5,
    "comment": "Great classic 90s anime cyberpunk",
    "director": "Mamoru Oshii",
    "year": 1995,
    "image": "post_requests/ghost_in_the_shell.jpg",
    "view_date": "2022-09-15"
}
files = {'image': open(data["image"], 'rb')}

response = requests.post(url, data=data, files=files)
print(response.json())