import streamlit as st
from streamlit_modal import Modal
import pandas as pd
from datetime import datetime
import gc, requests
st.set_page_config(layout="wide")
st.write("""
        ## 🤖 Chatbot
        """)

def api( children, data):
    api_urls = f'http://192.168.56.1:8005/streamlit/{children}'
    req = requests.post(api_urls, json = data)
    if req.status_code == 404:
        return pd.DataFrame()#req.content
    else:
        result = req.json()
        if len(result) == 1 and 'result' in result:
            return result['result']
        else:
            return pd.DataFrame(req.json())

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    
col1, col2, col3 = st.columns([6, 1, 1])
with col3:
    st.button('Clear Chat History', on_click=clear_chat_history)

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function for generating LLaMA2 response. Refactored from https://github.com/a16z-infra/llama2-chatbot
def generate_llama2_response(prompt_input):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'. And use traditional chinese to reply."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    output = api('chatbot', {"model_name": "yi:9b", 'topic': prompt_input, "prompt": f"{string_dialogue} {prompt_input} Assistant: "})
    # output = do.api_load_data_forTest('chatbot', {"model_name": "gemma:2b", 'topic': prompt_input, "prompt": f"{string_dialogue} {prompt_input} Assistant: "})#, "max_new_tokens": 512, "temperature": 0.1, "top_p": 0.95, "top_k": 40, "repetition_penalty": 1.2})
    return output

# User-provided prompt
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_llama2_response(prompt)#['result']
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
# st.write('🎄')
