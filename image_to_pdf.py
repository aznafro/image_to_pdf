import streamlit as st
from PIL import Image
import io

st.set_page_config(page_title="Image to PDF Converter", page_icon="🖼️")
st.title("🖼️ Image to PDF Converter")
st.write("Upload one or more images and download them as a single PDF.")

uploaded_files = st.file_uploader(
    "Choose image(s)",
    type=["png", "jpg", "jpeg", "bmp", "gif", "tiff", "webp"],
    accept_multiple_files=True,
)

if uploaded_files:
    images = []
    for file in uploaded_files:
        img = Image.open(file)
        # PDF export requires RGB (no alpha channel)
        if img.mode in ("RGBA", "P", "LA"):
            img = img.convert("RGB")
        images.append(img)

    st.subheader("Preview")
    cols = st.columns(min(len(images), 4))
    for i, img in enumerate(images):
        cols[i % len(cols)].image(img, caption=uploaded_files[i].name, use_container_width=True)

    # Build PDF in memory
    pdf_buffer = io.BytesIO()
    if len(images) == 1:
        images[0].save(pdf_buffer, format="PDF")
    else:
        images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=images[1:])
    pdf_buffer.seek(0)

    st.success(f"Converted {len(images)} image(s) into a PDF.")
    st.download_button(
        label="📥 Download PDF",
        data=pdf_buffer,
        file_name="converted.pdf",
        mime="application/pdf",
    )
else:
    st.info("Upload at least one image to get started.")