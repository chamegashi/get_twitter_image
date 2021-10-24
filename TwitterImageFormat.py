from dataclasses import dataclass

@dataclass
class TwitterImage:
    image_url: str = ""
    tweet_url: str = ""
    text: str = ""
    created: str = ""
    user: str = ""
    profile_image_url: str = ""
    
