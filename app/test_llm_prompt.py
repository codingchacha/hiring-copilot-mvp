from llm_client import prompt_to_candidate_query

test_prompt = """
Looking for a backend engineer with at least 4 years of experience, must know Python and FastAPI.
Preferably based in Bangalore. Bonus if they have over 50 GitHub stars and any relevant certification.
"""

query = prompt_to_candidate_query(test_prompt)

print("LLM Output:")
print(query)