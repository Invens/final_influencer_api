def estimate_influencer_pay(profile, engagement, niche='technology', content_type='reel', usage_rights='ads', platform='instagram'):
    base_rate_per_1k = 20 if profile["followers"] < 1_000_000 else (18 if profile["followers"] < 5_000_000 else 16)

    niche_multipliers = {
        'finance': 2.0, 'technology': 1.8, 'health': 1.6, 'beauty': 1.5,
        'fashion': 1.4, 'luxury': 2.0, 'gaming': 1.5, 'parenting': 1.3,
        'food': 1.2, 'home': 1.3, 'travel': 1.5, 'automotive': 2.0,
        'education': 1.4, 'entertainment': 1.2, 'pets': 1.2, 'sustainability': 1.3, 'art': 1.3
    }

    content_multipliers = {
        'static': 1.0, 'carousel': 1.2, 'video': 1.5, 'reel': 1.6
    }

    usage_multipliers = {
        'organic': 1.0, 'ads': 2.0
    }

    followers = profile["followers"]
    engagement_rate = ((engagement["avg_likes"] + engagement["avg_comments"]) / followers) if followers else 0

    estimate = (
        (base_rate_per_1k * (followers / 1000)) *
        engagement_rate *
        niche_multipliers.get(niche, 1.5) *
        content_multipliers.get(content_type, 1.0) *
        usage_multipliers.get(usage_rights, 1.0)
    )

    return round(estimate, 2)
