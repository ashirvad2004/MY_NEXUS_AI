import pymupdf
from sentence_transformers import SentenceTransformer

# ==========================================
# LOAD EMBEDDING MODEL
# ==========================================

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# ==========================================
# EXTRACT TEXT FROM PDF
# ==========================================

def extract_pdf_text(file_path):

    try:
        document = pymupdf.open(file_path)

        extracted_text = ""

        for page_number, page in enumerate(document):

            text = page.get_text()

            extracted_text += f"\n--- Page {page_number + 1} ---\n"
            extracted_text += text

        document.close()

        if not extracted_text.strip():
            return "No readable text found in this PDF."

        return extracted_text

    except Exception as e:
        return f"PDF extraction error: {str(e)}"


# ==========================================
# TEXT CHUNKING
# ==========================================

def split_text_into_chunks(text, chunk_size=500, overlap=50):

    try:
        words = text.split()
        chunks = []

        start = 0

        while start < len(words):

            end = start + chunk_size

            chunk = " ".join(words[start:end])

            chunks.append(chunk)

            start += chunk_size - overlap

        return chunks

    except Exception as e:
        return f"Chunking error: {str(e)}"

# ==========================================
# GENERATE TEXT EMBEDDINGS
# ==========================================

def generate_embeddings(chunks):

    try:

        embeddings = embedding_model.encode(chunks)

        return embeddings

    except Exception as e:

        return f"Embedding error: {str(e)}"