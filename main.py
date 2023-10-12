import streamlit as st
from langchain import HuggingFaceHub
from langchain import PromptTemplate, LLMChain
import os
# from apikey import hf_apikey, openai_apikey
import openai

# os.environ["HUGGINGFACEHUB_API_TOKEN"] = hf_apikey
# openai.api_key = openai_apikey

os.environ["HUGGINGFACEHUB_API_TOKEN"] = st.secrets["hf_apikey"]
openai.api_key = st.secrets["openai_apikey"]



# Falcon
repo_id = "tiiuae/falcon-7b-instruct"

falcon7b = HuggingFaceHub(repo_id=repo_id, model_kwargs={"temperature": 0.5, "max_new_tokens": 2000, "max_length": 2000})

template = """
You are an artificial intelligence chatbot.
You are having a conversation with a human user and another chatbot called ChatGPT.
Question: {question}\n\n
Answer: Let's think step by step."""
prompt = PromptTemplate(template=template, input_variables=["question"])
llm_chain = LLMChain(prompt=prompt, llm=falcon7b)





# creating streamlit app
def main():
    st.set_page_config(layout="wide")

    # TITLE
    st.markdown("<h1 style='text-align: center;'>Talk to ChatGPT and Falcon-7b</h1>", unsafe_allow_html=True)

    user_input = st.text_input("Your input")
    st.text("Enter your text query then choose to either send it to ChatGPT or Falcon. The other (unchosen) one will say whether they agree or disagree with the generated answer.")
    st.text("Note: I am in the middle of deploying this app on other front-end languages because Streamlit has several limitations which don't allow me to add certain features.")

    input_to_gpt = st.button("Input to ChatGPT")
    input_to_falcon = st.button("Input to Falcon")

    if input_to_gpt:
        gpt_column, falcon_column = st.columns(2)
        with gpt_column:
            st.header("GPT's response:")
            st.text("This may take a while, depending on your question...")
            with st.spinner("Generating..."):
                messages = []
                messages.append({"role": "user", "content": user_input})
                GPT_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                )
                gpt_reply = GPT_response["choices"][0]["message"]["content"]
                messages.append({"role": "assistant", "content": gpt_reply})
            st.success(gpt_reply)
        with falcon_column:
            st.header("Falcon's response:")
            with st.spinner("Generating..."):
                what_gpt_said = "This is what ChatGPT said. Say whether you agree or disagree, followed by your reasoning." + gpt_reply
                falcon_reply = llm_chain.run(what_gpt_said)
            st.success(falcon_reply)
    elif input_to_falcon:
        gpt_column, falcon_column = st.columns(2)
        with falcon_column:
            st.header("Falcon's response:")
            with st.spinner("Generating..."):
                falcon_reply = llm_chain.run(user_input)
            st.success(falcon_reply)
        with gpt_column:
            st.header("GPT's response:")
            st.text("This may take a while, depending on your question...")
            with st.spinner("Generating..."):
                what_falcon_said = "This is what Falcon, another language model, said. Say whether you agree or disagree, followed by your reasoning." + falcon_reply
                messages = []
                messages.append({"role": "user", "content": what_falcon_said})
                GPT_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                )
                gpt_reply = GPT_response["choices"][0]["message"]["content"]
                messages.append({"role": "assistant", "content": gpt_reply})
            st.success(gpt_reply)

if __name__ == "__main__":
    main()