from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from estimator import estimate_influencer_pay
from datetime import datetime
from playwright.sync_api import sync_playwright

# Create FastAPI app
app = FastAPI(title="Influencer Estimation API")

# CORS settings
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EstimateRequest(BaseModel):
    username: str
    niche: str
    content_type: str
    usage_rights: str

def scrape_instagram_profile(username):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(f"https://www.instagram.com/{username}/", timeout=15000)
            page.wait_for_selector("meta[name='description']", timeout=10000)

            desc = page.locator("meta[name='description']").get_attribute("content")
            title = page.title()
            profile_pic = page.locator("img").first.get_attribute("src")

            import re
            match = re.search(r"([\d\.]+)([MK]?) Followers", desc)
            if not match:
                raise Exception("Could not parse followers from description.")

            number = float(match.group(1))
            suffix = match.group(2)
            followers = (
                int(number * 1_000_000) if suffix == "M"
                else int(number * 1_000) if suffix == "K"
                else int(number)
            )

            return {
                "username": username,
                "full_name": title.split("•")[0].strip(),
                "followers": followers,
                "following": 0,
                "posts": 0,
                "is_private": False,
                "profile_pic": profile_pic,
                "bio": desc,
                "external_url": None,
                "last_updated": datetime.now().isoformat(),
                "recent_posts": []
            }

    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def health_check():
    return {"status": "API is running"}

@app.post("/estimate")
def estimate_influencer(data: EstimateRequest):
    profile = scrape_instagram_profile(data.username)

    if "error" in profile:
        return {"error": profile["error"]}

    if profile.get("is_private"):
        return {"error": "Profile is private"}

    # Dummy engagement (use your own logic or replace with scraping)
    engagement = {
        "avg_likes": 1000,
        "avg_comments": 50,
        "posts_analyzed": 20
    }

    followers = profile.get("followers") or 1
    engagement_rate = ((engagement["avg_likes"] + engagement["avg_comments"]) / followers) * 100

    estimate = estimate_influencer_pay(
        profile,
        engagement,
        niche=data.niche,
        content_type=data.content_type,
        usage_rights=data.usage_rights
    )

    return {
        "username": profile["username"],
        "full_name": profile["full_name"],
        "followers": profile["followers"],
        "engagement_rate": round(engagement_rate, 2),
        "avg_likes": engagement["avg_likes"],
        "avg_comments": engagement["avg_comments"],
        "estimated_pay": estimate
    }
