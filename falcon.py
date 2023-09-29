import streamlit as st
from langchain import HuggingFaceHub
from langchain import PromptTemplate, LLMChain
import os
from apikey import apikey

os.environ["HUGGINGFACEHUB_API_TOKEN"] = apikey

# LLM
repo_id = "tiiuae/falcon-7b-instruct"

llm = HuggingFaceHub(repo_id=repo_id, model_kwargs={"temperature": 0.5, "max_new_tokens": 2000, "max_length": 2000})

template = """
You are an artificial intelligence chatbot.
The chatbot holds meaningful conversations with the user.
Question: {question}\n\n
Answer: Let's think step by step."""
prompt = PromptTemplate(template=template, input_variables=["question"])
llm_chain = LLMChain(prompt=prompt, llm=llm)

# stable diffusion
from diffusers import (
    StableDiffusionPipeline,
    StableDiffusionImg2ImgPipeline,
)
text2img = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
img2img = StableDiffusionImg2ImgPipeline(**text2img.components)
import torch
from PIL import Image
import random

# torch.cuda.empty_cache()

device = "cuda" if torch.cuda.is_available() else "cpu"

# Text-to-speech
# import pyttsx3
# engine = pyttsx3.init()

# creating streamlit app
def main():
    st.set_page_config(layout="wide")
    # TITLE
    st.markdown("<h1 style='text-align: center;'>OMar's AI chatbot, made using Falcon-7b</h1>", unsafe_allow_html=True)

    # MAKING COLUMNS
    column1, column2, column3 = st.columns(3)

    # LLM CHATBOT
    with column1:
        st.header('Input to LLM bot')
        question = st.text_input("Your input:")
        if st.button("Generate") or question:
            with st.spinner("Generating..."):
                response = llm_chain.run(question)
            st.write('LLM\'s response:')
            st.success(response)
    
    # IMG2IMG SDXL
    with column2:
        st.header('[column 2 header]')
            # engine.say(response)
            # engine.runAndWait()

    with column3:
        st.header('[img2img header]')
        picture = st.camera_input("Take a picture!")
        output_picture = img2img(prompt="animated, cartoon",
                                image=picture,
                                negative_prompt="blur, grainy",
                                num_images_per_prompt=2,)
        st.image(output_picture)

if __name__ == "__main__":
    main()







# ========================= code below is old code using SDXL ====================================================================================
# pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-refiner-1.0",
#                                          torch_dtype=torch.float16) if torch.cuda.is_available() else DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-refiner-1.0")
# pipe = pipe.to(device)

# def resize(value, img):
#     img = Image.open(img)
#     img = img.resize((value,value))
#     return img

# def infer(source_img, prompt, negative_prompt, guide, steps, seed, Strength):
#     generator = torch.Generator(device).manual_seed(seed)     
#     source_image = resize(768, source_img)
#     source_image.save('source.png')
#     image = pipe(prompt,
#                  negative_prompt=negative_prompt,
#                  image=source_image,
#                  strength=Strength,
#                  guidance_scale=guide,
#                  num_inference_steps=steps).images[0]
#     return image



# =========================== code below is for img2img, problem is that it uses too much memory for some reason ==================================
    # (i made all values=1 first to save memory)
    # if st.button("Upload"):
    #     with st.spinner("Generating..."):
    #         output_picture = st.image(infer(picture,
    #                                         "Recreate this picture in anime style. 4khd, highres, high definition",
    #                                         "blue, grainy, badly drawn hands, badly drawn fingers, badly drawn face, ugly",
    #                                         1,
    #                                         1,
    #                                         40, # random.randint(0, 987654321987654321),
    #                                         0.05))
    #         st.success(output_picture)
    # print(torch.cuda.memory_summary())