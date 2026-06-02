import streamlit as st
from PIL import Image
import requests
import base64
import re

st.title("🔍 Smart Food Label Analyzer")

st.write("Upload a nutrition/ingredients label. The app extracts text, cleans it, and analyzes it.")

# -----------------------------
# Risk signals (better than strict keywords)
# -----------------------------
RISK_KEYWORDS = {
    "caffeine": "Stimulant (can affect sleep/heart rate)",
    "preserv": "Preservatives detected",
    "artificial": "Artificial additive detected",
    "flavor": "Artificial flavoring likely",
    "sweetener": "Non-sugar sweetener detected",
    "erythritol": "Sugar alcohol sweetener",
    "sucralose": "Artificial sweetener",
    "aspartame": "Artificial sweetener",
    "color": "Possible food coloring",
    "acid": "Additives or acidity regulators",
    "zero": "Often ultra-processed 'diet' product signal"
}

# -----------------------------
# OCR function (no installs needed)
# -----------------------------
def extract_text(image_bytes):
    img_b64 = base64.b64encode(image_bytes).decode()

    response = requests.post(
        "https://api.ocr.space/parse/image",
        data={
            "apikey": "helloworld",  # free demo key
            "base64Image": f"data:image/png;base64,{img_b64}"
        }
    )

    result = response.json()

    if "ParsedResults" in result:
        return result["ParsedResults"][0]["ParsedText"]
    return ""

# -----------------------------
# Clean OCR text (VERY IMPORTANT for your case)
# -----------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text

# -----------------------------
# Score system
# -----------------------------
def calculate_score(found_items):
    score = 100
    score -= len(found_items) * 10
    return max(score, 0)

# -----------------------------
# Upload image
# -----------------------------
uploaded_file = st.file_uploader("Upload label image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    st.subheader("🔄 Reading image...")

    text = extract_text(uploaded_file.getvalue())

    if not text:
        st.error("Could not read text from image.")
        st.stop()

    st.subheader("📄 Raw OCR Output")
    st.text_area("", text, height=250)

    # -----------------------------
    # Clean text
    # -----------------------------
    cleaned = clean_text(text)

    st.subheader("🧼 Cleaned Text (important for messy labels)")
    st.text_area("", cleaned, height=150)

    # -----------------------------
    # Risk detection
    # -----------------------------
    found = []

    for word, reason in RISK_KEYWORDS.items():
        if word in cleaned:
            found.append((word, reason))

    # -----------------------------
    # Results
    # -----------------------------
    st.subheader("⚠️ Analysis")

    score = calculate_score(found)

    st.metric("Health Score (0–100)", score)

    if found:
        for w, r in found:
            st.warning(f"{w.upper()} → {r}")
    else:
        st.success("No strong risk signals detected.")

    # -----------------------------
    #extra insight
    # -----------------------------
    st.subheader("🧠 Interpretation")

    if score >= 80:
        st.success("Likely low-risk / minimally processed.")
    elif score >= 50:
        st.info("Moderate processing detected.")
    else:
        st.error("Likely ultra-processed product (energy drinks / diet drinks often fall here).")
