
import json

def load_candidates(file_path="mock_candidates.json"):
    with open(file_path, "r") as f:
        return json.load(f)

def rank_candidates(candidates, query, top_n=5):
    """
    Rank candidates based on the query filters.
    Candidates without matching required skills are excluded.
    
    Args:
        candidates (list of dict): Candidate data loaded from JSON.
        query (dict): Parsed user query with keys like skills, experience, certifications, location, github_stars_min.
        top_n (int): Number of top candidates to return.
        
    Returns:
        list of dict: Top N candidates sorted by score (descending).
    """
    # Handle experience being int or dict
    exp = query.get("experience", {})
    if isinstance(exp, dict):
        min_experience = exp.get("years", 0)
    elif isinstance(exp, int):
        min_experience = exp
    else:
        min_experience = 0

    required_skills = set([s.lower() for s in query.get("skills", [])])
    required_certs = set([cert.lower() for cert in query.get("certifications", [])])
    location = query.get("location", None)
    min_github_stars = query.get("github_stars_min", 0)

    scored_candidates = []

    for c in candidates:
        score = 0
        
        # Candidate skills normalized
        candidate_skills = set([s.lower() for s in c.get("skills", [])])
        skills_matched = required_skills.intersection(candidate_skills)

        # Skip candidates with no skill match
        if not skills_matched:
            continue
        
        # Skills score (high priority)
        score += 10 * len(skills_matched)
        
        # Experience score
        exp_years = c.get("experience_years", 0)
        if exp_years >= min_experience:
            score += 1 * exp_years
        
        # Github stars score (sum stars from all repos)
        total_stars = sum(repo.get("stars", 0) for repo in c.get("github_repos", []))
        if total_stars >= min_github_stars:
            score += total_stars // 10  # 1 point per 10 stars
        
        # Relevant certifications score
        candidate_certs = c.get("certifications", [])
        cert_names = set(cert.get("name", "").lower() for cert in candidate_certs)
        certs_matched = {cert for cert in required_certs if cert in cert_names}
        score += 2 * len(certs_matched)
        
        # Location match bonus
        if location and c.get("location", "").lower() == location.lower():
            score += 5
        
        scored_candidates.append((score, c))
    
    # Sort descending by score
    scored_candidates.sort(key=lambda x: x[0], reverse=True)
    
    # Return top N candidates (only the candidate dict, not score)
    return [c for score, c in scored_candidates[:top_n]]



def format_candidates_for_ui(candidates):
    formatted_list = []
    for c in candidates:
        formatted = {
            "Name": c.get("name"),
            "Email": c.get("email"),
            "Skills": c.get("skills"),
            "Experience": c.get("experience_years"),
            "Location": c.get("location"),
        }

        # Add certifications only if not empty
        if c.get("certifications"):
            formatted["Certifications"] = [
                cert.get("name") for cert in c["certifications"] if cert.get("name")
            ]

        # Add github repos only if not empty
        if c.get("github_repos"):
            formatted["GitHub Repos"] = [
                {"name": repo.get("name"), "stars": repo.get("stars")}
                for repo in c["github_repos"] if repo.get("name")
            ]

        formatted_list.append(formatted)

    return formatted_list




if __name__ == "__main__":
    candidates = load_candidates("mock_candidates.json")
    test_query = {
        "skills": ["python", "fastapi"],
        "experience": {"years": 3},
        "location": "Bangalore",
        "github_stars_min": 50,
        "certifications": ["AWS Solutions Architect"]
    }
    top_candidates = rank_candidates(candidates, test_query, top_n=5)
    formatted_candidates = format_candidates_for_ui(top_candidates)
    print(formatted_candidates)
    