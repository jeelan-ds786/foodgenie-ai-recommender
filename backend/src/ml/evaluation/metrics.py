import numpy as np


# --------------------------------------------------
# Precision@K
# --------------------------------------------------

def precision_at_k(relevance, k=10):

    relevance = np.asarray(relevance)[:k]

    if len(relevance) == 0:
        return 0.0

    return np.sum(relevance > 0) / k


# --------------------------------------------------
# Recall@K
# --------------------------------------------------

def recall_at_k(relevance, total_relevant, k=10):

    relevance = np.asarray(relevance)[:k]

    if total_relevant == 0:
        return 0.0

    return np.sum(relevance > 0) / total_relevant


# --------------------------------------------------
# Reciprocal Rank
# --------------------------------------------------

def reciprocal_rank(relevance):

    relevance = np.asarray(relevance)

    for i, rel in enumerate(relevance):
        if rel > 0:
            return 1.0 / (i + 1)

    return 0.0


# --------------------------------------------------
# DCG
# --------------------------------------------------

def dcg_at_k(relevance, k=10):

    relevance = np.asarray(relevance)[:k]

    if len(relevance) == 0:
        return 0.0

    discounts = np.log2(np.arange(2, len(relevance) + 2))

    return np.sum(relevance / discounts)


# --------------------------------------------------
# NDCG
# --------------------------------------------------

def ndcg_at_k(relevance, k=10):

    dcg = dcg_at_k(relevance, k)

    ideal = sorted(relevance, reverse=True)

    idcg = dcg_at_k(ideal, k)

    if idcg == 0:
        return 0.0

    return dcg / idcg


# --------------------------------------------------
# Aggregate Evaluation
# --------------------------------------------------

def evaluate_ranking(relevance_lists, k=10):

    precision_scores = []
    recall_scores = []
    ndcg_scores = []
    mrr_scores = []

    for rel in relevance_lists:

        total_relevant = np.sum(np.array(rel) > 0)

        precision_scores.append(precision_at_k(rel, k))
        recall_scores.append(recall_at_k(rel, total_relevant, k))
        ndcg_scores.append(ndcg_at_k(rel, k))
        mrr_scores.append(reciprocal_rank(rel))

    return {
        "precision@k": float(np.mean(precision_scores)),
        "recall@k": float(np.mean(recall_scores)),
        "ndcg@k": float(np.mean(ndcg_scores)),
        "mrr": float(np.mean(mrr_scores))
    }