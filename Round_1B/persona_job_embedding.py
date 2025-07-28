from embedder import Embedder

def get_persona_job_embedding(persona, job_to_be_done):
    """
    Combines persona and job-to-be-done into a single embedding vector.
    """
    embedder = Embedder()
    combined_text = f"{persona['role']} - {job_to_be_done['task']}"
    return embedder.embed_texts([combined_text])[0]
         