




def fetch_trending_keywords(niche, num_keywords=5):
    # Placeholder: En vrai, utiliser pytrends ou API Google Trends
    trending = {
        "productivité": ["time blocking", "deep work", "notion templates"],
        "fitness": ["HIIT", "home workout", "meal prep"]
    }
    return trending.get(niche, [])[:num_keywords]

# Usage dans workflow : "args": {"niche": "fitness"} → injecté via plugin  
