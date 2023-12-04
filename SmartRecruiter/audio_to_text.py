# -*- coding: utf-8 -*-
import streamlit as st
import openai
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk import word_tokenize, pos_tag
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()




nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


def convert_audio_to_text(audio_file):
     transcript = openai.audio.transcriptions.create(
         model="whisper-1",
         file=Path(audio_file),
         response_format="text"
     )
     return transcript

def analyze_sentiment(text):
     sia = SentimentIntensityAnalyzer()
     sentiment_score = sia.polarity_scores(text)['compound']
     return sentiment_score

def extract_keywords(text, pos_tags=['NN', 'VB', 'JJ', 'CD']):
     words = word_tokenize(text)
     tagged_words = pos_tag(words)
     keywords = [word for word, pos in tagged_words if pos in pos_tags]
     return keywords

def rate_aspect(sentiment_score, keywords):
     sentiment_mapping = {
         'Very Negative': 1,
         'Negative': 2,
         'Neutral': 3,
         'Positive': 4,
         'Very Positive': 5
     }

     if sentiment_score >= 0.2:
         sentiment_category = 'Very Positive'
     elif 0.1 <= sentiment_score < 0.2:
         sentiment_category = 'Positive'
     elif -0.1 < sentiment_score <= 0.1:
         sentiment_category = 'Neutral'
     elif -0.2 <= sentiment_score < -0.1:
         sentiment_category = 'Negative'
     else:
         sentiment_category = 'Very Negative'

     keyword_rating = min(len(keywords), 5)
     combined_rating = (sentiment_mapping[sentiment_category] + keyword_rating) / 2

     return combined_rating
 
def generate_summary(audio_text):
    
    prompt = f"""
       Summarize the below paragraph and give the result in 2 lines:
        {audio_text}
    """
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful Assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7,
        )
    summary = response.choices[0].message.content
    st.write(f"FeedBack for the interview: {summary}")

def feedBackAnalysis(uploaded_file):
    if uploaded_file:
         st.audio(uploaded_file, format="audio/wav")
         
         audio_text = convert_audio_to_text(uploaded_file)
         st.subheader("Audio Transcript:")
         st.write(audio_text)
         generate_summary(audio_text)
         conversation_sentiment = analyze_sentiment(audio_text)

         # Extract technical and behavioral keywords
         technical_keywords = extract_keywords(audio_text, pos_tags=['NN', 'VB', 'JJ', 'CD'])
         behavioral_keywords = extract_keywords(audio_text, pos_tags=['NN', 'VB', 'JJ'])

         # Rate technical and behavioral aspects
         technical_rating = rate_aspect(conversation_sentiment, technical_keywords)
         behavioral_rating = rate_aspect(conversation_sentiment, behavioral_keywords)

         st.subheader("Ratings:")
         st.write(f"Technical Rating: {technical_rating}")
         st.write(f"Behavioral Rating: {behavioral_rating}")
    




