# import requests module
import requests

# Making a get request
response = requests.get('https://jsonplaceholder.typicode.com/posts/5')

# Store JSON data in API_Data
API_Data = response.json()

# Print json data using loop
for key in API_Data:
    print(key,":", API_Data[key])
