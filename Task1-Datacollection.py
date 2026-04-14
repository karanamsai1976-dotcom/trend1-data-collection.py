import requests
import json
import time
from datetime import datetime

# Task 1: Fetch JSON
# ---------------------------------------------------------
def task1_fetch_data():
    print("Task 1: Fetching Data")
    headers = {"User-Agent": "TrendPulse/1.0"}
    base_url = "https://hacker-news.firebaseio.com/v0"
    
    # 1. Fetch top 500 story IDs
    

    categories_dict = {
        "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
        "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
        "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
        "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
        "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
    }

    all_stories = []
    fetched_cache = {}    # Cache to avoid re-fetching same HackerNews item across loops
    assigned_ids = set()  # Ensure each story is assigned to only one category

    # Loop over categories
    for category, keywords in categories_dict.items():
        print(f"Fetching stories for {category}...")
        
        # Wait 2 seconds between each category
        time.sleep(2)
        
        count = 0
        for story_id in top_ids:
            if count >= 25:
                break  # Reached max 25 stories for this category
            
            # Skip if story was already assigned to an earlier category
            if story_id in assigned_ids:
                continue
            
            # Fetch story details if not cached
            if story_id not in fetched_cache:
                try:
                    resp = requests.get(f"{base_url}/item/{story_id}.json", headers=headers)
                    resp.raise_for_status()
                    fetched_cache[story_id] = resp.json()
                except Exception as e:
                    print(f"Failed to fetch story {story_id}: {e} - moving on.")
                    continue
            
            story = fetched_cache[story_id]
            
            # Defensive check
            if not story or 'title' not in story:
                continue
            
            title = story.get('title', '')
            title_lower = title.lower()
            
            # Check for keyword match
            match = False
            for kw in keywords:
                if kw.lower() in title_lower:
                    match = True
                    break
            
            if match:
                # Extract fields
                extracted = {
                    "post_id": story.get("id"),
                    "title": title,
                    "category": category,
                    "score": story.get("score"),
                    "num_comments": story.get("descendants"),  # descendants = comments count
                    "author": story.get("by"),
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                all_stories.append(extracted)
                assigned_ids.add(story_id)
                count += 1
                
    # Save to data directory
    os.makedirs("data", exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"data/trends_{date_str}.json"
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_stories, f, indent=4)
        
    print(f"Collected {len(all_stories)} stories. Saved to {filename}")
    return filename