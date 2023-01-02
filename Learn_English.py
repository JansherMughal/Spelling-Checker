# Import the required module for text
# to speech conversion
from gtts import gTTS

import os
import re 
import streamlit as st
import numpy as np

def tts(text):
    # Language in which you want to convert
    language = 'en'

    # Passing the text and language to the engine,
    # here we have marked slow=False. Which tells
    # the module that the converted audio should
    # have a high speed
    speech = gTTS(text=text, lang=language, slow=False)

    # Saving the converted audio in a mp3 file named
    # welcome
    speech.save("sample.mp3")

def get_words():
    with open("words.txt", 'r') as f:
        words = f.read()
    # print(words)
    words = re.split('\.|/|:| |,|\n',words)

    words = [word.strip().lower() for word in words if word.strip() != ""]
    # rest = [word for word in words if "." in word]
    # words = [word for word in words if "." not in word]

    # print(len(words))
    return words

def genrate_word(words):
    word = np.random.choice(words, size=1)[0]
    print("genrating ", word)
    with open("word.txt", "w") as f:
        f.write(word)
    tts(word)
    return word

def update_audio():
    audio_file = open('sample.mp3', 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/mp3')

def update_frontend():
    words = get_words()
    genrate_word(words)
    update_audio()

def get_main_word():
    with open("word.txt", "r") as f:
        return f.read()

st.title("Spelling checker for English learning")

if st.sidebar.button("Regenerate"):
    update_frontend()
    user_word = None
    st.session_state["text"] = ""


if st.sidebar.button("Show"):
    update_audio()

user_word = st.text_input("word", value="", key="text")

if st.sidebar.button("check spelling") or user_word:
    main_word  = get_main_word()
    if main_word == user_word.lower():
       st.balloons()
       st.success('Correct spelling! Go get 8/100 score', icon="✅")
    else:
        st.snow()
        st.error('Try harder', icon="🚨")
 
if st.sidebar.button("Show word"):
    main_word  = get_main_word()
    st.info('Word is '+main_word, icon="ℹ️")
    
st.text(str(len(get_words()))+" words are used in this demo, Good luck!")
