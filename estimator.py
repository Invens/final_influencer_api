def estimate_influencer_pay(profile, engagement, niche='technology', content_type='reel', usage_rights='ads'):
    niche_multipliers = {
        'finance': 2.0, 'technology': 1.8, 'health': 1.6, 'beauty': 1.5,
        'fashion': 1.4, 'luxury': 2.0, 'gaming': 1.5, 'parenting': 1.3,
        'food': 1.2, 'home': 1.3, 'travel': 1.5, 'automotive': 2.0,
        'education': 1.4, 'entertainment': 1.2, 'pets': 1.2, 'sustainability': 1.3, 'art': 1.3
    }

    content_multipliers = {'static': 1.0, 'carousel': 1.2, 'video': 1.5, 'reel': 1.6}
    usage_multipliers = {'organic': 1.0, 'ads': 2.0}

    followers = profile.get('followers', 0)
    followers_k = followers / 1000

    if followers <= 1_000_000:
        base_rate = 20
    elif followers <= 5_000_000:
        base_rate = 18
    else:
        base_rate = 16

    engagement_rate = (engagement.get("avg_likes", 0) + engagement.get("avg_comments", 0)) / followers if followers else 0
    return round(
        base_rate * followers_k *
        engagement_rate *
        niche_multipliers.get(niche, 1.5) *
        content_multipliers.get(content_type, 1.0) *
        usage_multipliers.get(usage_rights, 1.0),
        2
    )
