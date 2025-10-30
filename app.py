# app.py
import streamlit as st
from PyPDF2 import PdfMerger
import io

st.set_page_config(page_title="Unir PDF", page_icon="📄", layout="centered")

st.title("📄 Unir Archivos PDF")
st.write("Sube varios archivos PDF y únelos en uno solo fácilmente.")

# Inicializar estado si no existe
if "merged_pdf_bytes" not in st.session_state:
    st.session_state.merged_pdf_bytes = None

# Colocamos uploader en una columna y botones en la otra para mejor UI
col1, col2 = st.columns([3, 1])

with col1:
    uploaded_files = st.file_uploader(
        "Selecciona los archivos PDF para unir",
        type=["pdf"],
        accept_multiple_files=True,
        key="uploader"  # clave para poder reiniciar desde session_state
    )

with col2:
    if st.button("🔄 Limpiar"):
        # Limpiamos el uploader (reiniciando su clave en session_state) y cualquier PDF generado
        # Establecemos None en la clave del uploader y re-ejecutamos la app
        st.session_state.uploader = None
        st.session_state.merged_pdf_bytes = None
        st.experimental_rerun()

# Botón para unir (se separa la acción de la carga para más control)
if st.button("📎 Unir PDFs"):
    if not uploaded_files:
        st.warning("No has subido archivos. Por favor sube uno o varios PDFs.")
    else:
        merger = PdfMerger()
        try:
            for pdf in uploaded_files:
                # pdf es un UploadedFile; PdfMerger acepta file-like
                merger.append(pdf)
            merged_pdf = io.BytesIO()
            merger.write(merged_pdf)
            merger.close()
            merged_pdf.seek(0)
            st.session_state.merged_pdf_bytes = merged_pdf.read()  # guardamos bytes en session_state
            st.success("✅ ¡PDFs unidos correctamente!")
        except Exception as e:
            st.error(f"Error al unir los PDFs: {e}")
            st.session_state.merged_pdf_bytes = None

# Si ya tenemos el PDF unido en session_state, mostramos opciones de descarga y previsualización
if st.session_state.merged_pdf_bytes:
    # Reconstruimos el BytesIO para la descarga (pointer al inicio)
    merged_bytes_io = io.BytesIO(st.session_state.merged_pdf_bytes)
    st.download_button(
        label="📥 Descargar PDF unido",
        data=merged_bytes_io,
        file_name="pdf_unido.pdf",
        mime="application/pdf"
    )

    # Opción extra: mostrar el PDF embebido en la app (si Streamlit lo permite en tu entorno)
    try:
        st.write("Previsualización (si tu navegador lo soporta):")
        st.components.v1.html(
            f'<iframe src="data:application/pdf;base64,{st.session_state.merged_pdf_bytes.encode("base64").decode()}" width="700" height="900" type="application/pdf"></iframe>',
            height=900,
        )
    except Exception:
        # fallback simple: indicar que la previsualización no está disponible
        st.info("Previsualización no disponible en este entorno. Descarga el archivo para verlo.")
