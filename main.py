from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from estimator import estimate_influencer_pay
from scraper import InstagramPublicScraper

# Create FastAPI app
app = FastAPI(title="Influencer Estimation API")

# CORS settings — update your domain(s) below
origins = [
    "http://localhost:3000",       # for local development
    "https://fluencerz.com/"     # replace with your actual deployed domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body model
class EstimateRequest(BaseModel):
    username: str
    niche: str
    content_type: str
    usage_rights: str

@app.get("/")
def health_check():
    return {"status": "API is running"}

@app.post("/estimate")
def estimate_influencer(data: EstimateRequest):
    scraper = InstagramPublicScraper()
    profile = scraper.get_public_profile(data.username)

    if "error" in profile:
        return {"error": profile["error"]}

    if profile.get("is_private"):
        return {"error": "Profile is private"}

    engagement = scraper.get_profile_engagement(profile.get("recent_posts", []))

    if "error" in engagement:
        return {"error": engagement["error"]}

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
