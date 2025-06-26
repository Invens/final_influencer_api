import requests
import time
import random
from datetime import datetime

class InstagramPublicScraper:
    def __init__(self):
        self.session = requests.Session()
        
        # 🎯 Official IG frontend App ID
        self.ig_app_id = '936619743392459'

        # 🔁 Rotating real-world User-Agent headers
        self.user_agents = [
            # Desktop Chrome
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/113.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/110.0.0.0 Safari/537.36',

            # Mobile Chrome
            'Mozilla/5.0 (Linux; Android 10; SM-G970F) AppleWebKit/537.36 Chrome/103.0.5060.70 Mobile Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 Version/14.0 Mobile Safari/604.1',

            # Safari
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 Version/13.1.2 Safari/605.1.15',
            'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 Version/13.0 Mobile Safari/604.1',

            # Firefox
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0',

            # Edge
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/113.0.1774.50 Safari/537.36 Edg/113.0.1774.50'
        ]

    def random_delay(self):
        time.sleep(random.uniform(2, 5))

    def get_public_profile(self, username):
        self.random_delay()
        try:
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Accept-Language': 'en-US,en;q=0.9',
                'X-IG-App-ID': self.ig_app_id,
                'Referer': f'https://www.instagram.com/{username}/'
            }
            url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
            res = self.session.get(url, headers=headers)
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
