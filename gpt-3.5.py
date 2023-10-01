import os
from apikey import apikey
import streamlit as st
# from langchain.llms import OpenAI
import openai

# os.environ['OPENAI_API_KEY'] = apikey
openai.api_key = apikey

# completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Write an essay about penguins"}])
# print(completion.choices[0].message.content)
# llm = OpenAI(temperature=0.9)

messages = []
st.title("Omar's chatbot")
question = st.text_input("Your input:")
if question or st.button("Enter"):
    with st.spinner("Generating..."):
        messages.append({"role": "user", "content": question})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = response["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": reply})
        st.success(reply)

# def main():
#     st.title('Omar\'s AI chatbot friend')
#     question = st.text_input('Your input:')

#     if question or st.button('Enter'):
#         with st.spinner('Generating...'):
#             response = llm(question)
#             st.success(response)

# if __name__ == "__main__":
#     main()


# curl https://api.openai.com/v1/chat/completions -H "Content-Type: application/json" -H "Authorization: Bearer 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" -d '{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "Say this is a test!"}], "temperature": 0.7}'