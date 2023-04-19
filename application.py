import streamlit as st
from streamlit_chat import message
from PIL import Image
from decouple import config
import openai


openai.api_key = config("API_KEY")

def ask(question:str) -> str:
    response = openai.Completion.create(model="text-davinci-003",
                                        prompt=question,
                                        temperature=0.7,
                                        max_tokens=1024,
                                        stop=["\\n"],
                                        top_p=1,
                                        frequency_penalty=0,
                                        presence_penalty=0
                                        )
    answer = response.choices[0].text
    return answer

st.set_page_config(page_title="AI Teaching Assistant Bot",
                   layout="centered")

# st.image(image,
#          caption="Teaching Assitant Bot")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def get_text() -> str:
    input_text = st.text_input(label="You:",
                               value="Hello, How are you?",
                               key="input")
    return input_text

user_input = get_text()

if user_input:
    response = ask(user_input)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(response)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i],
                key=str(i))
        message(st.session_state["past"][i],
                is_user=True,
                key=str(i)+"_user")