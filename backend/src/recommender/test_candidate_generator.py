from candidate_generator import generate_candidates

query = "dosa with coconut chutney"

results = generate_candidates(query)

print("\nTop Food Candidates:\n")

print(results.head(10))