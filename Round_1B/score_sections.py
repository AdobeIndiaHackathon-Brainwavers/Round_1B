from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def mmr(doc_embeddings, query_embedding, lambda_param=0.7, top_n=5):
    doc_embeddings = np.array(doc_embeddings)
    query_embedding = np.array(query_embedding)

    similarities = cosine_similarity(doc_embeddings, [query_embedding]).flatten()
    selected = []
    candidate_indices = list(range(len(doc_embeddings)))

    for _ in range(top_n):
        if not candidate_indices:
            break

        if not selected:
            selected_idx = int(np.argmax(similarities))
            selected.append(selected_idx)
            candidate_indices.remove(selected_idx)
            continue

        mmr_scores = []
        for idx in candidate_indices:
            relevance = similarities[idx]
            diversity = max(cosine_similarity([doc_embeddings[idx]], [doc_embeddings[s]])[0][0] for s in selected)
            mmr_score = lambda_param * relevance - (1 - lambda_param) * diversity
            mmr_scores.append((idx, mmr_score))

        selected_idx, _ = max(mmr_scores, key=lambda x: x[1])
        selected.append(selected_idx)
        candidate_indices.remove(selected_idx)

    return selected

def rank_sections(sections, persona_embedding, job_embedding, embedder, top_k=5):
    combined_query = (persona_embedding + job_embedding) / 2
    texts = [s['text'] for s in sections]
    section_embeddings = embedder.encode(texts)

    selected_indices = mmr(section_embeddings, combined_query, top_n=top_k)

    scored_sections = []
    for rank, idx in enumerate(selected_indices, start=1):
        s = sections[idx]
        s["importance_rank"] = rank
        scored_sections.append(s)

    return scored_sections
