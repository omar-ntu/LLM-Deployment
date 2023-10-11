import streamlit as st
from langchain import HuggingFaceHub
from langchain import PromptTemplate, LLMChain
import os
# from apikey import hf_apikey, openai_apikey
import openai

# os.environ["HUGGINGFACEHUB_API_TOKEN"] = hf_apikey
# openai.api_key = openai_apikey
# st.write("HF:", st.secrets["hf_apikey"])
# st.write("OPENAI:", st.secrets["openai_apikey"])
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

# def userinput():
#     global GPTinput
#     global falconinput
#     GPTinput = st.text_input("Input to GPT")
#     falconinput = st.text_input("Input to falcon")
#     return GPTinput, falconinput

# def main():
#     userinput()
#     if GPTinput:
#         with st.spinner("Generating..."):
#             messages = []
#             messages.append({"role": "user", "content": GPTinput})
#             GPT_response = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo",
#                 messages=messages
#             )
#             text_reply = GPT_response["choices"][0]["message"]["content"]
#             messages.append({"role": "assistant", "content": text_reply})
#         st.success(text_reply)





# creating streamlit app
def main():
    st.set_page_config(layout="wide")

    # TITLE
    st.markdown("<h1 style='text-align: center;'>Talk to ChatGPT and Falcon-7b</h1>", unsafe_allow_html=True)

    user_input = st.text_input("Your input")

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
        falcon_column, gpt_column = st.columns(2)
        with falcon_column:
            st.header("Falcon's response:")
            with st.spinner("Generating..."):
                falcon_reply = llm_chain.run(user_input)
            st.success(falcon_reply)
        with gpt_column:
            st.header("GPT's response:")
            with st.spinner("Generating..."):
                what_falcon_said = "This is what Falcon-40b, another language model, said. Say whether you agree or disagree, followed by your reasoning." + falcon_reply
                messages = []
                messages.append({"role": "user", "content": what_falcon_said})
                GPT_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                )
                gpt_reply = GPT_response["choices"][0]["message"]["content"]
                messages.append({"role": "assistant", "content": gpt_reply})
            st.success(gpt_reply)

    

    # MAKING COLUMNS
    # column1, column2 = st.columns(2)
    # with column1:
    #     st.header('GPT-3.5')
    #     messages = []
    #     GPT_question = st.text_input("input to GPT:")
    #     if GPT_question:
    #         with st.spinner("Generating..."):
    #             messages.append({"role": "user", "content": GPT_question})
    #             GPT_response = openai.ChatCompletion.create(
    #                 model="gpt-3.5-turbo",
    #                 messages=messages
    #             )
    #             text_reply = GPT_response["choices"][0]["message"]["content"]
    #             messages.append({"role": "assistant", "content": text_reply})
    #         st.write('GPT\'s response:')
    #         st.success(text_reply)
    #         input_to_gpt = True
    #         input_to_falcon = False
    #     if input_to_falcon == True:
    #         with st.spinner("Generating..."):
    #             what_falcon_said = "This is what Falcon-7B said. Do you agree? Answer with either saying you agree or disagree, followed by your reasoning." + falcon_response
    #             messages.append({"role": "user", "content": what_falcon_said})
    #             GPT_response = openai.ChatCompletion.create(
    #                 model="gpt-3.5-turbo",
    #                 messages=messages
    #             )
    #             text_reply = GPT_response["choices"][0]["message"]["content"]
    #             messages.append({"role": "assistant", "content": text_reply})
    #         st.write('GPT\'s response to Falcon:')
    #         st.success(text_reply)
    #         input_to_falcon = False
    #         input_to_gpt = False
    
    # with column2:
    #     st.header('Falcon-7B')
    #     falcon_question = st.text_input("input to falcon:")
    #     if falcon_question:
    #         with st.spinner("Generating..."):
    #             falcon_response = llm_chain.run(falcon_question)
    #         st.write('Falcon\'s response:')
    #         st.success(falcon_response)
    #         input_to_falcon = True
    #         input_to_gpt = False
    #     if input_to_gpt == True:
    #         with st.spinner("Generating..."):
    #             what_gpt_said = "This is what ChatGPT said. Do you agree? Answer with either saying you agree or disagree, followed by your reasoning." + text_reply
    #             falcon_response = llm_chain.run(what_gpt_said)
    #         st.write('Falcon\'s response to GPT:')
    #         st.success(falcon_response)
    #         input_to_falcon = False
    #         input_to_gpt = False

    

if __name__ == "__main__":
    main()

