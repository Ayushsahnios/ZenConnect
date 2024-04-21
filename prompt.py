import requests
import json
import speech_recognition as sr
import pocketsphinx


# Define the API endpoint for generating content
API_ENDPOINT = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=AIzaSyBSdnqYOZI8O5IBS2ZxIp6fEECg-sfyF1o'

# Define the request headers
headers = {
    'Content-Type': 'application/json'
}

# Create a recognizer instance
recognizer = sr.Recognizer()

# Use the default microphone as the audio source
with sr.Microphone() as source:
    print("Listening...")

    # Adjust for ambient noise
    recognizer.adjust_for_ambient_noise(source)

    # Continuous listening loop
    while True:
        try:
            # Listen to the speech
            audio = recognizer.listen(source, timeout=5)
            
            # Recognize speech using CMU Sphinx
            text = recognizer.recognize_sphinx(audio)

            # Define the request body
            data = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": text
                            }
                        ]
                    }
                ]
            }

            # Convert the data dictionary to JSON format
            data_json = json.dumps(data)

            # Make the POST request to the API endpoint
            response = requests.post(API_ENDPOINT, headers=headers, data=data_json)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Print the generated content response
                print("Generated Content:", response.json())
            else:
                # Print an error message if the request failed
                print(f"Error: {response.status_code}")

        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Sphinx service; {e}")
        except KeyboardInterrupt:
            print("Exiting...")
            break
