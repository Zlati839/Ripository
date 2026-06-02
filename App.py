import streamlit as st
import requests
from PIL import Image
import io
import re

st.title("Ingredient Label Checker")

# Get your free API key from https://ocr.space/
API_KEY = st.secrets["OCR_SPACE_API_KEY"]

BAD_INGREDIENTS = {
    "aspartame": "Artificial sweetener",
    "high fructose corn syrup": "Highly processed sweetener",
    "red 40": "Artificial food coloring",
    "yellow 5": "Artificial food coloring",
    "msg": "Flavor enhancer",
    "sodium nitrite": "Common preservative"
}

uploaded_file = st.file_uploader(
    "Upload ingredient label",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image")

    image_bytes = io.BytesIO()
    image.save(image_bytes, format="PNG")
    image_bytes.seek(0)

    with st.spinner("Reading label..."):
        response = requests.post(
            "https://api.ocr.space/parse/image",
            files={"file": image_bytes},
            data={
                "apikey": API_KEY,
                "language": "eng"
            }
        )

    result = response.json()

    text = ""

    if result.get("ParsedResults"):
        text = result["ParsedResults"][0]["ParsedText"]

    st.subheader("Detected Text")
    st.text_area("", text, height=250)

    found = []

    text_lower = text.lower()

    for ingredient, description in BAD_INGREDIENTS.items():
        if ingredient.lower() in text_lower:
            found.append((ingredient, description))

    st.subheader("Ingredient Analysis")

    if found:
        for ingredient, description in found:
            st.warning(
                f"⚠️ {ingredient.title()} - {description}"
            )
    else:
        st.success("No flagged ingredients found.")
    if not found:
        st.success("No common unhealthy ingredients detected.")
