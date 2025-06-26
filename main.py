# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from estimator import estimate_influencer_pay
from scraper import get_instaloader_profile, get_instaloader_engagement

app = FastAPI(title="Influencer Estimation API")

# Allow all origins (change this in production!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EstimateRequest(BaseModel):
    username: str
    niche: str
    content_type: str
    usage_rights: str

@app.get("/")
def health():
    return {"status": "OK"}

@app.post("/estimate")
def estimate(data: EstimateRequest):
    profile = get_instaloader_profile(data.username)
    if "error" in profile:
        raise HTTPException(status_code=400, detail=profile["error"])

    engagement = get_instaloader_engagement(data.username, max_posts=20)
    if "error" in engagement:
        raise HTTPException(status_code=400, detail=engagement["error"])

    followers = profile["followers"] or 1
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
        "followers": followers,
        "engagement_rate": round(engagement_rate, 2),
        "avg_likes": engagement["avg_likes"],
        "avg_comments": engagement["avg_comments"],
        "estimated_pay": estimate
    }
