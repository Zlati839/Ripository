import streamlit as st
import numpy as np
from PIL import Image
import subprocess
import tempfile
import re

st.title("🔍 Ingredient Scanner (Auto OCR, No API Key)")

st.write("Upload a food label image and the app will extract and analyze ingredients automatically.")

BAD_INGREDIENTS = {
    "aspartame": "Artificial sweetener",
    "sucralose": "Artificial sweetener",
    "high fructose corn syrup": "Highly processed sweetener",
    "msg": "Flavor enhancer (monosodium glutamate)",
    "sodium nitrite": "Preservative in processed meats",
    "red 40": "Artificial dye",
    "yellow 5": "Artificial dye",
    "bht": "Synthetic preservative",
    "bha": "Synthetic preservative",
    "hydrogenated oil": "May contain trans fats"
}

uploaded_file = st.file_uploader("Upload label image", type=["jpg", "jpeg", "png"])


def run_tesseract(image_path):
    """Call system tesseract directly (NO pytesseract library needed)"""
    result = subprocess.run(
        ["tesseract", image_path, "stdout"],
        capture_output=True,
        text=True
    )
    return result.stdout


if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Save image temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        image.save(tmp.name)
        temp_path = tmp.name

    st.subheader("🔄 Reading text from image...")

    try:
        text = run_tesseract(temp_path)
    except Exception as e:
        st.error("Tesseract is not installed on this system.")
        st.stop()

    st.subheader("📄 What the app read:")

    st.text_area("OCR Output", text, height=250)

    # Ingredient check
    text_lower = text.lower()
    found = []

    for ingredient, reason in BAD_INGREDIENTS.items():
        if re.search(r"\b" + re.escape(ingredient) + r"\b", text_lower):
            found.append((ingredient, reason))

    st.subheader("⚠️ Ingredient Analysis")

    if found:
        for ing, reason in found:
            st.warning(f"{ing.title()} → {reason}")
    else:
        st.success("No flagged ingredients found.")
