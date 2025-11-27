import streamlit as st
from PIL import Image
from ocr import run_ocr

st.set_page_config(page_title="Image → TEXT", layout="wide")

st.title("Image → TEXT")
st.markdown("Upload a diagram image (photo, screenshot). The app will OCR and return a human-readable Document.")

uploaded = st.file_uploader("Upload image", type=["png", "jpg", "jpeg", "tiff"])

if uploaded:
    img = Image.open(uploaded).convert("RGB")
    st.image(img, caption="Uploaded image", use_container_width=True)
    if st.button("Run pipeline"):
        with st.spinner("Running OCR..."):
            ocr_out = run_ocr(img)
        ocr_text = ocr_out.get("ocr_text", "")
        st.subheader("OCR Text (extracted)")
        st.text_area("OCR Text", value=ocr_text, height=500)
