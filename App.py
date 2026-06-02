import streamlit as st
from PIL import Image
import pytesseract
import re

st.set_page_config(page_title="Food Label Analyzer")

st.title("🥫 Food Label Analyzer")
st.write("Upload a food label image and I'll read it and identify potentially unhealthy ingredients.")

uploaded_file = st.file_uploader(
    "Upload a label image",
    type=["jpg", "jpeg", "png"]
)

# Ingredients commonly considered unhealthy
UNHEALTHY_INGREDIENTS = [
    "high fructose corn syrup",
    "corn syrup",
    "hydrogenated oil",
    "partially hydrogenated oil",
    "trans fat",
    "artificial flavor",
    "artificial flavours",
    "artificial color",
    "artificial colour",
    "red 40",
    "yellow 5",
    "yellow 6",
    "blue 1",
    "blue 2",
    "aspartame",
    "sucralose",
    "acesulfame potassium",
    "msg",
    "monosodium glutamate"
]

def analyze_text(text):
    findings = []

    lower_text = text.lower()

    # Ingredient checks
    for ingredient in UNHEALTHY_INGREDIENTS:
        if ingredient in lower_text:
            findings.append(f"⚠ Found: {ingredient}")

    # Sugar check
    sugar_match = re.search(r"sugars?\s*(\d+)", lower_text)
    if sugar_match:
        sugar = int(sugar_match.group(1))
        if sugar >= 15:
            findings.append(
                f"⚠ High sugar content detected ({sugar}g)"
            )

    # Sodium check
    sodium_match = re.search(r"sodium\s*(\d+)", lower_text)
    if sodium_match:
        sodium = int(sodium_match.group(1))
        if sodium >= 400:
            findings.append(
                f"⚠ High sodium content detected ({sodium}mg)"
            )

    # Saturated fat check
    sat_fat_match = re.search(
        r"saturated fat\s*(\d+)",
        lower_text
    )

    if sat_fat_match:
        sat_fat = int(sat_fat_match.group(1))
        if sat_fat >= 5:
            findings.append(
                f"⚠ High saturated fat detected ({sat_fat}g)"
            )

    return findings

if uploaded_file:

    image = Image.open(uploaded_file)

    st.image(image, caption="Uploaded Label", use_container_width=True)

    with st.spinner("Reading label..."):
        extracted_text = pytesseract.image_to_string(image)

    st.subheader("📄 Extracted Text")
    st.text_area(
        "What was read from the label",
        extracted_text,
        height=300
    )

    findings = analyze_text(extracted_text)

    st.subheader("🔍 Health Analysis")

    if findings:
        for item in findings:
            st.warning(item)
    else:
        st.success(
            "No obvious unhealthy ingredients or nutrition concerns detected."
        )
