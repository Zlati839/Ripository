import streamlit as st
from PIL import Image
import base64
import requests

st.title("🔍 Ingredient Scanner (No OCR Install Needed)")

st.write("Upload a food label image. The AI will read it automatically.")

BAD_INGREDIENTS = {
    "aspartame": "Artificial sweetener",
    "sucralose": "Artificial sweetener",
    "high fructose corn syrup": "Highly processed sweetener",
    "msg": "Flavor enhancer",
    "sodium nitrite": "Preservative",
    "red 40": "Artificial dye",
    "yellow 5": "Artificial dye"
}

uploaded_file = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])

def image_to_base64(img):
    return base64.b64encode(img.read()).decode()

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    st.subheader("📄 Reading text from image...")

    # Convert image to base64
    img_bytes = uploaded_file.getvalue()
    img_b64 = base64.b64encode(img_bytes).decode()

    # Use OCR API alternative (free endpoint style)
    response = requests.post(
        "https://api.ocr.space/parse/image",
        data={
            "apikey": "helloworld",
            "base64Image": f"data:image/png;base64,{img_b64}"
        }
    )

    result = response.json()

    text = ""
    if "ParsedResults" in result:
        text = result["ParsedResults"][0]["ParsedText"]

    st.subheader("📝 What was read:")
    st.text_area("OCR Output", text, height=250)

    # Ingredient check
    text_lower = text.lower()
    found = []

    for ing, reason in BAD_INGREDIENTS.items():
        if ing in text_lower:
            found.append((ing, reason))

    st.subheader("⚠️ Ingredient Analysis")

    if found:
        for ing, reason in found:
            st.warning(f"{ing.title()} → {reason}")
    else:
        st.success("No flagged ingredients found.")
