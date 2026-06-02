import streamlit as st
from PIL import Image
import numpy as np
import re

st.title("🔍 Ingredient Label Checker (No OCR Required)")

st.write("""
Upload a label image. Since no OCR engine is used,
you can either:
1. Try visual reading
2. Or type detected ingredients manually
""")

BAD_INGREDIENTS = {
    "aspartame": "Artificial sweetener",
    "sucralose": "Artificial sweetener",
    "high fructose corn syrup": "Highly processed sweetener",
    "msg": "Flavor enhancer",
    "sodium nitrite": "Preservative in processed meats",
    "red 40": "Artificial dye",
    "yellow 5": "Artificial dye",
    "bht": "Synthetic preservative",
    "bha": "Synthetic preservative",
    "hydrogenated oil": "May contain trans fats"
}

uploaded_file = st.file_uploader(
    "Upload ingredient label image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    st.subheader("✍️ Step 1: Enter ingredients manually")
    user_text = st.text_area(
        "Paste or type what you see on the label:"
    )

    if user_text:
        text_lower = user_text.lower()

        found = []

        for ingredient, description in BAD_INGREDIENTS.items():
            if re.search(r"\b" + re.escape(ingredient) + r"\b", text_lower):
                found.append((ingredient, description))

        st.subheader("⚠️ Analysis Result")

        if found:
            for ing, desc in found:
                st.warning(f"{ing.title()} → {desc}")
        else:
            st.success("No flagged ingredients found.")

    st.divider()

    st.subheader("📌 Optional helper (image preview)")
    st.write("Zoom in on the image and manually check ingredients above.")
