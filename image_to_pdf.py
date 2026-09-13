import streamlit as st
from PIL import Image
import img2pdf
import io

st.set_page_config(page_title="Image to PDF Converter", page_icon="🖼️", layout="centered")

# ---------- Language text ----------
TEXT = {
    "English": {
        "title": "🖼️ Photo to PDF",
        "lang_label": "Language / 언어",
        "upload_label": "📁 Choose Photo(s)",
        "preview_header": "Your Photos",
        "success": "✅ Your PDF is ready!",
        "download": "⬇️ Download PDF",
        "empty": "👆 Tap the button above to choose a photo",
    },
    "한국어": {
        "title": "🖼️ 사진을 PDF로",
        "lang_label": "Language / 언어",
        "upload_label": "📁 사진 선택하기",
        "preview_header": "내 사진",
        "success": "✅ PDF가 준비되었습니다!",
        "download": "⬇️ PDF 다운로드",
        "empty": "👆 위 버튼을 눌러 사진을 선택하세요",
    },
}

# ---------- Big, simple styling ----------
st.markdown(
    """
    <style>
    html, body, [class*="css"]  {
        font-size: 22px !important;
    }
    h1 {
        font-size: 44px !important;
        text-align: center;
    }
    h2 {
        font-size: 32px !important;
    }
    /* Buttons: big, bold, obvious */
    .stButton>button, .stDownloadButton>button {
        font-size: 26px !important;
        padding: 20px 32px !important;
        border-radius: 14px !important;
        font-weight: 700 !important;
        width: 100%;
    }
    /* Radio buttons (language toggle) bigger */
    div[role="radiogroup"] label {
        font-size: 24px !important;
    }
    /* File uploader label bigger */
    [data-testid="stFileUploaderDropzoneInstructions"] {
        font-size: 20px !important;
    }
    /* Hide the tiny "Drag and drop / Limit 200MB" fine print */
    [data-testid="stFileUploaderDropzoneInstructions"] span,
    [data-testid="stFileUploaderDropzoneInstructions"] small {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Language toggle ----------
lang = st.radio("Language / 언어", options=["한국어", "English"], horizontal=True, label_visibility="collapsed")
t = TEXT[lang]

st.title(t["title"])

uploaded_files = st.file_uploader(
    t["upload_label"],
    type=["png", "jpg", "jpeg", "bmp", "tiff", "webp"],
    accept_multiple_files=True,
)

def to_flat_png_bytes(uploaded_file):
    """Load image, flatten transparency, return PNG bytes (lossless, no re-encoding artifacts)."""
    img = Image.open(uploaded_file)
    if img.mode in ("RGBA", "P", "LA"):
        img = img.convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf.read()

if uploaded_files:
    st.header(t["preview_header"])
    for f in uploaded_files:
        st.image(f, use_container_width=True)

    # Build the PDF with img2pdf: page size is taken from each image's
    # actual pixel dimensions, so nothing gets clipped.
    image_bytes_list = [to_flat_png_bytes(f) for f in uploaded_files]
    pdf_bytes = img2pdf.convert(image_bytes_list)

    st.success(t["success"])
    st.download_button(
        label=t["download"],
        data=pdf_bytes,
        file_name="converted.pdf",
        mime="application/pdf",
    )
else:
    st.info(t["empty"])
