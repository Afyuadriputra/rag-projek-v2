import pdfplumber
import pandas as pd
import logging # 1. Import Logging
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .config import get_vectorstore

# 2. Inisialisasi Logger
logger = logging.getLogger(__name__)

def process_document(doc_instance):
    """
    Membaca file PDF/Excel/CSV/MD, memecahnya, dan menyimpan ke ChromaDB
    dengan Metadata User ID.
    """
    file_path = doc_instance.file.path
    ext = file_path.split('.')[-1].lower()
    text_content = ""

    logger.info(f"📄 MULAI PARSING: {doc_instance.title} (Type: {ext})")

    # 1. PARSING (Ekstraksi Teks berdasarkan Tipe File)
    try:
        if ext == 'pdf':
            with pdfplumber.open(file_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    # Ekstrak Tabel
                    tables = page.extract_tables()
                    for table in tables:
                        for row in table:
                            clean_row = [str(item) if item else "" for item in row]
                            text_content += " | ".join(clean_row) + "\n"
                    
                    # Ekstrak Teks Biasa
                    text = page.extract_text()
                    if text: text_content += text + "\n"
            
            logger.debug(f"✅ PDF Parsed: {len(pdf.pages)} halaman.")
        
        elif ext in ['xlsx', 'xls']:
            try:
                df = pd.read_excel(file_path)
                df = df.fillna('') 
                text_content = df.to_markdown(index=False)
                logger.debug(f"✅ Excel Parsed: {len(df)} baris data.")
            except Exception as e:
                logger.error(f"❌ Gagal baca Excel {doc_instance.title}: {e}", exc_info=True)
                return False

        elif ext == 'csv':
            # Logic CSV yang lebih robust (tahan banting)
            try:
                # Percobaan 1: Separator Koma (Default)
                df = pd.read_csv(file_path)
            except Exception as e_comma:
                logger.warning(f"⚠️ Gagal baca CSV pakai koma, mencoba titik-koma... ({e_comma})")
                try:
                    # Percobaan 2: Separator Titik Koma (Format Excel Indo/Eropa)
                    df = pd.read_csv(file_path, sep=';')
                except Exception as e_semi:
                    # Percobaan 3: Masalah Encoding (Misal file buatan Excel lama)
                    logger.warning(f"⚠️ Gagal baca CSV pakai titik-koma, mencoba encoding latin-1... ({e_semi})")
                    try:
                        df = pd.read_csv(file_path, sep=None, engine='python', encoding='latin-1')
                    except Exception as e_final:
                        logger.error(f"❌ CSV GAGAL TOTAL: {doc_instance.title}. Error: {e_final}", exc_info=True)
                        return False
            
            df = df.fillna('')
            text_content = df.to_markdown(index=False)
            logger.debug(f"✅ CSV Parsed: {len(df)} baris data.")
            
        elif ext in ['md', 'txt']:
            with open(file_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
            logger.debug(f"✅ Text Parsed.")

        else:
            logger.warning(f"⚠️ Tipe file tidak didukung: {ext}")
            return False

        # Cek apakah teks berhasil diambil?
        if not text_content.strip():
            logger.warning(f"⚠️ FILE KOSONG: {doc_instance.title} tidak mengandung teks yang bisa dibaca.")
            return False

        # 2. CHUNKING (Pemecahan Teks)
        # Chunk size diperbesar sedikit agar tabel tidak terpotong aneh
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = splitter.split_text(text_content)

        if not chunks:
            logger.warning(f"⚠️ CHUNKING GAGAL: Tidak ada potongan teks yang dihasilkan untuk {doc_instance.title}.")
            return False

        logger.debug(f"✂️ Terpecah menjadi {len(chunks)} chunks.")

        # 3. EMBEDDING & STORAGE
        vectorstore = get_vectorstore()
        
        # Metadata User ID (Kunci Keamanan Data!)
        metadatas = [{"user_id": str(doc_instance.user.id), "source": doc_instance.title} for _ in chunks]
        
        logger.debug(f"💾 Menyimpan ke ChromaDB...")
        vectorstore.add_texts(texts=chunks, metadatas=metadatas)
        
        logger.info(f"✅ INGEST SELESAI: {doc_instance.title} berhasil masuk Knowledge Base.")
        return True

    except Exception as e:
        # LOGGING ERROR KRITIS (Akan menampilkan baris merah di terminal)
        logger.error(f"❌ CRITICAL ERROR di ingest.py pada file {doc_instance.title}: {str(e)}", exc_info=True)
        return False