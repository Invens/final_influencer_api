import requests
import time
import random
from datetime import datetime

class InstagramPublicScraper:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept-Language': 'en-US,en;q=0.9',
            'X-IG-App-ID': '936619743392459',
        }

    def random_delay(self):
        time.sleep(random.uniform(2, 5))

    def get_public_profile(self, username):
        self.random_delay()
        try:
            url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
            res = self.session.get(url, headers=self.headers)
            if res.status_code != 200:
                return {"error": f"Request failed: {res.status_code}"}
            user = res.json()["data"]["user"]
            return {
                "username": user["username"],
                "full_name": user["full_name"],
                "followers": user["edge_followed_by"]["count"],
                "following": user["edge_follow"]["count"],
                "posts": user["edge_owner_to_timeline_media"]["count"],
                "is_private": user["is_private"],
                "profile_pic": user.get("profile_pic_url_hd") or user.get("profile_pic_url"),
                "bio": user.get("biography"),
                "external_url": user.get("external_url"),
                "last_updated": datetime.now().isoformat(),
                "recent_posts": user.get("edge_owner_to_timeline_media", {}).get("edges", [])
            }
        except Exception as e:
            return {"error": str(e)}

    def get_profile_engagement(self, posts):
        self.random_delay()
        if not posts:
            return {"error": "No posts or profile is private"}
        posts_to_analyze = posts[:20] if len(posts) >= 20 else posts
        likes = [p["node"]["edge_liked_by"]["count"] for p in posts_to_analyze]
        comments = [p["node"]["edge_media_to_comment"]["count"] for p in posts_to_analyze]
        return {
            "avg_likes": round(sum(likes) / len(posts_to_analyze), 2),
            "avg_comments": round(sum(comments) / len(posts_to_analyze), 2),
            "posts_analyzed": len(posts_to_analyze)
        }
