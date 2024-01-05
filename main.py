from typing import Union
from fastapi import FastAPI
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
model = genai.GenerativeModel('gemini-pro')
import pathlib
import textwrap
from IPython.display import display
from IPython.display import Markdown


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

app = FastAPI()

@app.get('/')
def root():
    return {"Message":"Hello World"}
@app.get('/content/')
def getYoutubeScript(code : str = None):
    transcript=""
    video_url=code
    try:
        transcript= YouTubeTranscriptApi.get_transcript(video_url)
    except Exception as e :
        print(f"Error retrieving subtitles: {str(e)}")
    result =""
    for entry in transcript:
        result = result + entry['text']
    return result

@app.get('/summary/')
def rishavGemini(code : str = None):
    transcript=""
    video_url=code
    try:
        transcript= YouTubeTranscriptApi.get_transcript(video_url)
    except Exception as e :
        print(f"Error retrieving subtitles: {str(e)}")
    result =""
    for entry in transcript:
        result = result + entry['text']
    



    genai.configure(api_key="AIzaSyBjJkjihTUrVF0JbVEBLUZ5kwZyzzJzROs")
    # response = model.generate_content("Summarize the following text:-  "+result)
    # response = model.generate_content("Explain the following text    "+result)
    response = model.generate_content("Explain the youtube video with video id  "+str(code)+" ")

  # "Explain the youtube video with video id  "+str(code)+" "
    print(response.text)
    return {"message":response.text}

@app.get('/question/')
def rishavGemini(q : int,code : str = None):
    transcript=""
    video_url=code
    try:
        transcript= YouTubeTranscriptApi.get_transcript(video_url)
    except Exception as e :
        print(f"Error retrieving subtitles: {str(e)}")
    result =""
    for entry in transcript:
        result = result + entry['text']
    



    genai.configure(api_key="AIzaSyBjJkjihTUrVF0JbVEBLUZ5kwZyzzJzROs")
    # response = model.generate_content("Summarize the following text:-  "+result)
    response = model.generate_content("Create "+str(q)+" questions from the following context "+result)
    print(response.text)
    return {"message":response.text}
