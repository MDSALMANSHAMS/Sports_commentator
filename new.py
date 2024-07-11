import base64
import requests
import os
from openai import OpenAI
import time

# OpenAI API Key
api_key = os.environ['OPENAI_API_KEY']
client = OpenAI(api_key=api_key)

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

image_path = "images/1.png"
base64_image = encode_image(image_path)

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

# Image to text
payload = {
  "model": "gpt-4o",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Discribe the image"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
        }
      ]
    }
  ],
  "max_tokens": 100
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

# Extracting the text response from the API
text_response = response.json()['choices'][0]['message']['content']
print("Text Response from OpenAI:")
print(text_response)

# Text to speech
speech_file_path = "response/speech_eng.mp3"
response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input=text_response
)

response.stream_to_file(speech_file_path)
