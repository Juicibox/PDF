import streamlit as st
from PyPDF2 import PdfMerger
import io

st.set_page_config(page_title="Unir PDF", page_icon="📄", layout="centered")

st.title("📄 Unir Archivos PDF")
st.write("Sube varios archivos PDF y únelos en uno solo fácilmente.")

# Subir archivos PDF
uploaded_files = st.file_uploader(
    "Selecciona los archivos PDF para unir",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    merger = PdfMerger()

    for pdf in uploaded_files:
        merger.append(pdf)

    # Guardar el resultado en memoria (sin crear archivos temporales)
    merged_pdf = io.BytesIO()
    merger.write(merged_pdf)
    merger.close()
    merged_pdf.seek(0)

    st.success("✅ ¡PDFs unidos correctamente!")

    # Botón para descargar
    st.download_button(
        label="📥 Descargar PDF unido",
        data=merged_pdf,
        file_name="pdf_unido.pdf",
        mime="application/pdf"
    )
