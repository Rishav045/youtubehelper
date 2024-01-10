from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
model = genai.GenerativeModel('gemini-pro')
import pathlib
import textwrap
from IPython.display import display
from IPython.display import Markdown
import requests


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

app = FastAPI()

origins =[
    "https://ashishrnx.github.io",
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)

@app.get('/')
def root():
    return {"Message":"Hello World"}
@app.get('/content/')
def getYoutubeScript(code : str = None):
    url = "https://youtube-transcriptor.p.rapidapi.com/transcript"



    headers = {
	"X-RapidAPI-Key": "05f93faddamsh06e8d213053c0f4p13558bjsne63c2384e3ca",
	"X-RapidAPI-Host": "youtube-transcriptor.p.rapidapi.com"
    }
    transcript=""
    querystring = {"video_id":code}

    response = requests.get(url, headers=headers, params=querystring)
    # print(response.json()['transcription'])
    for content in response.json()[0]['transcription']:
        transcript = transcript + content['subtitle']+" "
    return transcript
@app.get('/summary/')
def rishavGemini(code : str = None):
    transcript=""
    url = "https://youtube-transcriptor.p.rapidapi.com/transcript"



    headers = {
	"X-RapidAPI-Key": "05f93faddamsh06e8d213053c0f4p13558bjsne63c2384e3ca",
	"X-RapidAPI-Host": "youtube-transcriptor.p.rapidapi.com"
    }
    transcript=""
    querystring = {"video_id":code}
    response = requests.get(url, headers=headers, params=querystring)
    # print(response.json()['transcription'])
    for content in response.json()[0]['transcription']:
        transcript = transcript + content['subtitle']+" "


    if(transcript==""):
        return {"message":"sorry the subtitles are not available for this video"}
    genai.configure(api_key="AIzaSyBjJkjihTUrVF0JbVEBLUZ5kwZyzzJzROs")
    response = model.generate_content("Explain the following text which is a script of a video :-  "+transcript)
    # response = model.generate_content("Explain the youtube video with video id  "+str(code)+" ")
    # print(response._chunks)
    # print(response.text)
    return {"message":response.text}

@app.get('/askme/')
def askme(code : str = None , ques :str =None):
    transcript=""
    url = "https://youtube-transcriptor.p.rapidapi.com/transcript"



    headers = {
	"X-RapidAPI-Key": "05f93faddamsh06e8d213053c0f4p13558bjsne63c2384e3ca",
	"X-RapidAPI-Host": "youtube-transcriptor.p.rapidapi.com"
    }
    transcript=""
    querystring = {"video_id":code}
    response = requests.get(url, headers=headers, params=querystring)
    # print(response.json()['transcription'])
    for content in response.json()[0]['transcription']:
        transcript = transcript + content['subtitle']+" "
    
    

    genai.configure(api_key="AIzaSyBjJkjihTUrVF0JbVEBLUZ5kwZyzzJzROs")

    response= model.generate_content("Answer the question "+ques+" from the context "+transcript+" of the video :- ")
    print(response.text)
    return {"message":response.text}


@app.get('/question/')
def rishavGemini(q : str='10',code : str = None):
    transcript=""
    url = "https://youtube-transcriptor.p.rapidapi.com/transcript"



    headers = {
	"X-RapidAPI-Key": "05f93faddamsh06e8d213053c0f4p13558bjsne63c2384e3ca",
	"X-RapidAPI-Host": "youtube-transcriptor.p.rapidapi.com"
    }
    transcript=""
    querystring = {"video_id":code}
    response = requests.get(url, headers=headers, params=querystring)
    # print(response.json()['transcription'])
    for content in response.json()[0]['transcription']:
        transcript = transcript + content['subtitle']+" "
    

    print(transcript)
    if(transcript==""):
        return {"message":"sorry the subtitles are not available for this video"}
    
    genai.configure(api_key="AIzaSyBjJkjihTUrVF0JbVEBLUZ5kwZyzzJzROs")
    response = model.generate_content("List out "+q+" questions along with their answers from text :- "+transcript)
    print(response.prompt_feedback)
    # response = model.generate_content("Explain the following text which is a script of a video :-  "+transcript)
    # response = model.generate_content("Create "+str(q)+" questions from the following youtube video id "+str(code))
    
    return {"message":response.text}
