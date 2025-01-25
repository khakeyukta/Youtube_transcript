import streamlit as st 
from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import GoogleGenerativeAI
import os

from youtube_transcript_api import YouTubeTranscriptApi


prompt="""You are Youtube video summarizer.You will be taking the transcript text and summarizing the entire video and providing the important summary in form of points within 250 words"""



def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript=""
        for i in transcript_text:
            transcript +=" "+i["text"]
        return transcript
        
    except Exception as e:
        raise e
def generate_gemini_content(transcript_text,prompt):
    model=GoogleGenerativeAI(model="gemini-pro")
    full_prompt=prompt+" "+transcript_text
    response=model.generate([full_prompt])
    if hasattr(response,'generations')and response.generations:
        generated_text=response.generations[0][0].text
        return generated_text
    else:
        return "No response generated."

st.title("YOUTUBE TRANSCRIPT TO DETAILED NOTES CONVERTER")
youtube_link=st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id=youtube_link.split("=")[1]
    st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg",use_column_width=True)

if st.button("Get details"):
    transcript=extract_transcript_details(youtube_link)
    if transcript:
        response=generate_gemini_content(transcript,prompt)
    st.markdown("Details")
    st.write(response)