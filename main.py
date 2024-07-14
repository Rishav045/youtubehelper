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

def url_to_code(url):
    code=""
    if(url.find("www.youtube.com")!=-1):
  # print("running")
        for i in range(url.find('v=')+2,len(url)):
            if(url[i]=='&'):
                break
            else:
                code = code+url[i]
    elif(url.find("youtu.be")!=-1):
  # print(url.find("youtu.be"))
        for i in range(url.find("youtu.be")+9,len(url)):
            if(url[i]=='?'):
                break
            else:
                code = code + url[i]
    else:
        return("blank")
    return(code)
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
	# "X-RapidAPI-Key": "05f93faddamsh06e8d213053c0f4p13558bjsne63c2384e3ca",
    "X-RapidAPI-Key":"263a07c313msh5ca70463c5264bcp191e3ajsne9b0d563c2dd",
	"X-RapidAPI-Host": "youtube-transcriptor.p.rapidapi.com"
    }
    transcript=""
    code=url_to_code(code)
    if(code=="blank"):
        return {"message":"Please enter correct URL "}
    querystring = {"video_id":code}

    response = requests.get(url, headers=headers, params=querystring)
    print(response.json())
    try:
        for content in response.json()[0]['transcription']:
            transcript = transcript + str(content['subtitle'])+" "
    except KeyError as Ie:
        print(f"Index error {Ie}")
        return {"message":"No Script available for this video"}
    return transcript
@app.get('/summary/')
def rishavGemini(code : str = None):
    transcript=""
    url = "https://youtube-transcriptor.p.rapidapi.com/transcript"



    headers = {
	# "X-RapidAPI-Key": "05f93faddamsh06e8d213053c0f4p13558bjsne63c2384e3ca",
    "X-RapidAPI-Key":"263a07c313msh5ca70463c5264bcp191e3ajsne9b0d563c2dd",
	"X-RapidAPI-Host": "youtube-transcriptor.p.rapidapi.com"
    }
    transcript=""
    code=url_to_code(code)
    if(code=="blank"):
        return {"message":"Please enter correct URL "}
    querystring = {"video_id":code}
    response = requests.get(url, headers=headers, params=querystring)
    print(response.json())
    try:
        for content in response.json()[0]['transcription']:
            transcript = transcript + str(content['subtitle'])+" "
    except KeyError as Ie:
        print(f"Index error {Ie}")
        return {"message":"No Script available for this video"}
    
    if(int(response.json()[0]['lengthInSeconds'])>5400):
        return {"message":"Please provide the video's code length less than 90 minutes."}

    if(transcript==""):
        return {"message":"sorry the subtitles are not available for this video"}
    genai.configure(api_key="AIzaSyDfBUXvWleeus9K2s0zCXHqsQMnQgdmAak")
    response = model.generate_content("Prepare a report or article over the script of a video in english:-  "+transcript)
    # response = model.generate_content("Briefly describe the youtube video with video id  "+str(code)+" ")
    # print(response._chunks)
    # print(response.text)
    print(f"summary response {response}")
    print(response.prompt_feedback)
    return {"message":response.text}

@app.get('/askme/')
def askme(code : str = None , ques :str =None):
    transcript=""
    url = "https://youtube-transcriptor.p.rapidapi.com/transcript"



    headers = {
	# "X-RapidAPI-Key": "05f93faddamsh06e8d213053c0f4p13558bjsne63c2384e3ca",
    "X-RapidAPI-Key":"263a07c313msh5ca70463c5264bcp191e3ajsne9b0d563c2dd",
	"X-RapidAPI-Host": "youtube-transcriptor.p.rapidapi.com"
    }
    transcript=""
    code=url_to_code(code)
    if(code=="blank"):
        return {"message":"Please enter correct URL "}
    querystring = {"video_id":code}
    response = requests.get(url, headers=headers, params=querystring)
    try:
        for content in response.json()[0]['transcription']:
            transcript = transcript + str(content['subtitle'])+" "
    except KeyError as Ie:
        print(f"Index error {Ie}")
        return {"message":"No Script available for this video"}
    
    if(int(response.json()[0]['lengthInSeconds'])>5400):
        return {"message":"Please provide the video's code length less than 90 minutes."}
    

    genai.configure(api_key="AIzaSyDfBUXvWleeus9K2s0zCXHqsQMnQgdmAak")

    response= model.generate_content("Answer the question "+ques+" from the context "+transcript+" of the video in English:- ")
    print(response.text)
    return {"message":response.text}


@app.get('/question/')
def rishavGemini(q : str='10',code : str = None):
    transcript=""
    url = "https://youtube-transcriptor.p.rapidapi.com/transcript"



    headers = {
	# "X-RapidAPI-Key": "05f93faddamsh06e8d213053c0f4p13558bjsne63c2384e3ca",
    "X-RapidAPI-Key":"263a07c313msh5ca70463c5264bcp191e3ajsne9b0d563c2dd",
	"X-RapidAPI-Host": "youtube-transcriptor.p.rapidapi.com"
    }
    transcript=""
    code=url_to_code(code)
    if(code=="blank"):
        return {"message":"Please enter correct URL "}
    querystring = {"video_id":code}
    response = requests.get(url, headers=headers, params=querystring)
    try:
        for content in response.json()[0]['transcription']:
            transcript = transcript + str(content['subtitle'])+" "
    except KeyError as Ie:
        print(f"Index error {Ie}")
        return {"message":"No Script available for this video"}
    
    if(int(response.json()[0]['lengthInSeconds'])>5400):
        return {"message":"Please provide the video's code length less than 90 minutes."}

    print(transcript)
    if(transcript==""):
        return {"message":"sorry the subtitles are not available for this video"}
    
    genai.configure(api_key="AIzaSyDfBUXvWleeus9K2s0zCXHqsQMnQgdmAak")
    response = model.generate_content("List out "+q+" questions along with their answers from text in English:- "+transcript)
    print(response.prompt_feedback)
    # response = model.generate_content("Explain the following text which is a script of a video :-  "+transcript)
    # response = model.generate_content("Create "+str(q)+" questions from the following youtube video id "+str(code))
    
    return {"message":response.text}
