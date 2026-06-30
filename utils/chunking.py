def create_chunks(pages, chunk_size=1200, overlap=250):
    chunks = []
    step = chunk_size - overlap
    
    for page in pages:
        text = page["text"]
        start = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))

            # Don't cut a word in half
            while end < len(text) and text[end] != " ":
                end += 1
            chunk = text[start:end]

            if chunk.strip():
                chunks.append({
                    "page": page["page"],
                    "text": chunk
                })
            
            start += step

    return chunks