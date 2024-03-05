import requests 

  

# Specify the API endpoint URL 

api_url = "https://5fd3-92-237-138-59.ngrok-free.app/audio_to_audio" 
file_path = "C:/Users/iankh/Documents/GitHub/EIP-Qube/audio.wav"
download_path = "C:/Users/iankh/Documents/GitHub/EIP-Qube/Qube/downloaded_audio.wav"

# Define headers 

headers = { 

    'ngrok-skip-browser-warning': '69420' 

} 

  

with open (file_path, 'rb') as f:

    files = {'file': ('audio.wav', f, 'audio/wav')}

    response = requests.post(api_url, headers=headers, files=files) 

    # Check if the request was successful (status code 200) 

    if response.status_code == 200:
        audio_content = response.content 
        with open (download_path,'wb') as f:
            f.write(audio_content)
        print("File upload successfully.")

    else: 

    # Print an error message if the request was not successful 
        print(f"Error: {response.status_code} - {response.text}")