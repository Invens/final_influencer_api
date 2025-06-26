import instaloader

def get_instaloader_profile(username):
    try:
        L = instaloader.Instaloader()
        profile = instaloader.Profile.from_username(L.context, username)
        return {
            "username": profile.username,
            "full_name": profile.full_name,
            "followers": profile.followers,
            "following": profile.followees,
            "bio": profile.biography,
            "external_url": profile.external_url,
            "is_private": profile.is_private,
            "profile_pic": profile.profile_pic_url,
        }
    except Exception as e:
        return {"error": str(e)}

def get_instaloader_engagement(username, max_posts=20):
    try:
        L = instaloader.Instaloader()
        profile = instaloader.Profile.from_username(L.context, username)
        posts = profile.get_posts()

        likes = []
        comments = []

        for idx, post in enumerate(posts):
            if idx >= max_posts:
                break
            likes.append(post.likes)
            comments.append(post.comments)

        if not likes:
            return {"error": "No public posts found"}

        return {
            "avg_likes": round(sum(likes) / len(likes), 2),
            "avg_comments": round(sum(comments) / len(comments), 2),
            "posts_analyzed": len(likes)
        }
    except Exception as e:
        return {"error": str(e)}
