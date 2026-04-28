import requests
from typing import List, Dict, Any

def search_github_datasets(query: str, per_page: int = 15) -> List[Dict[str, Any]]:
    """
    Search GitHub for repositories related to datasets based on a query.
    
    Args:
        query (str): The search term provided by the user.
        per_page (int): Number of results to fetch.
        
    Returns:
        List of dictionaries containing dataset information.
    """
    url = "https://api.github.com/search/repositories"
    
    # Append 'dataset' to the query if not already present
    q = f"{query} dataset" if query else "dataset"
    
    params = {
        "q": q,
        "per_page": per_page,
        "sort": "stars",
        "order": "desc"
    }
    
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get("items", []):
            results.append({
                "name": item.get("name", "Unknown"),
                "description": item.get("description", "No description available."),
                "html_url": item.get("html_url", "#"),
                "stars": item.get("stargazers_count", 0),
                "author": item.get("owner", {}).get("login", "Unknown")
            })
            
        return results
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from GitHub API: {e}")
        return []
