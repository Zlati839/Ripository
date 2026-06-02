import streamlit as st
from openai import OpenAI
import base64

st.title("Food Label Analyzer")

api_key = st.text_input("OpenAI API Key", type="password")

uploaded_file = st.file_uploader(
    "Upload a food label image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file and api_key:

    image_bytes = uploaded_file.read()

    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    client = OpenAI(api_key=api_key)

    with st.spinner("Reading label..."):

        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """
Read this food label.

1. Print ALL text found on the label.
2. List potentially unhealthy ingredients.
3. Flag high sugar, sodium, saturated fat, or trans fat.
4. Give a simple health score from 1-10.
"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
        )

    st.subheader("Results")
    st.write(response.choices[0].message.content)
