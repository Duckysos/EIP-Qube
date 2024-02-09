import requests 

  

# Specify the API endpoint URL 

api_url = "https://2393-94-175-61-189.ngrok-free.app/getAllLessons"

  

# Define headers 

headers = { 

    'ngrok-skip-browser-warning': '69420' 

} 

  

# Send a GET request with headers 

response = requests.get(api_url, headers=headers) 

  

# Check if the request was successful (status code 200) 

if response.status_code == 200: 

    print(response.json()) 

else: 

    # Print an error message if the request was not successful 

    print(f"Error: {response.status_code} - {response.text}") 