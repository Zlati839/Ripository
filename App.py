import streamlit as st
import easyocr
import numpy as np
from PIL import Image

st.set_page_config(page_title="Food Label Reader")

st.title("🥫 Food Label Reader")

uploaded_file = st.file_uploader(
    "Upload a food label image",
    type=["jpg", "jpeg", "png"]
)

UNHEALTHY = [
    "high fructose corn syrup",
    "corn syrup",
    "hydrogenated oil",
    "partially hydrogenated oil",
    "trans fat",
    "aspartame",
    "sucralose",
    "msg",
    "artificial flavor",
    "artificial colour",
    "red 40",
    "yellow 5",
    "yellow 6"
]

if uploaded_file:

    image = Image.open(uploaded_file)

    st.image(image, caption="Uploaded Label")

    with st.spinner("Reading label..."):

        reader = easyocr.Reader(['en'])

        results = reader.readtext(np.array(image))

        extracted_text = "\n".join(
            [item[1] for item in results]
        )

    st.subheader("📄 Everything Read From The Label")

    st.text_area(
        "Detected Text",
        extracted_text,
        height=300
    )

    st.subheader("⚠ Potential Concerns")

    found = False

    lower_text = extracted_text.lower()

    for ingredient in UNHEALTHY:
        if ingredient in lower_text:
            st.warning(f"Found: {ingredient}")
            found = True

    if not found:
        st.success("No common unhealthy ingredients detected.")
