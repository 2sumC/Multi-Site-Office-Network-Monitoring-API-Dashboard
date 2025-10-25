import requests
from datetime import datetime
from config import Config
import random

class NewsService:
    BASE_URL = "https://api.thenewsapi.com/v1/news/headlines"

    def __init__(self, api_key=None):
        self.api_key = api_key or Config.NEWS_API_KEY
        print(f"🧩 Loaded News API Key: {self.api_key[:6]}..." if self.api_key else "⚠️ No NEWS_API_KEY found")

    def get_latest_news(self, language="en", max_items=5):
        """获取最新新闻"""
        if not self.api_key or self.api_key.strip() == "":
            print("⚠️ Using mock data (no NEWS_API_KEY found)")
            return self._get_mock_news(max_items)

        try:
            params = {
                "api_token": self.api_key,
                "language": language,
                "headlines_per_category": max_items,
                "include_similar": False
            }
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if "data" not in data:
                print(f"⚠️ Unexpected API response: {data}")
                return self._get_mock_news(max_items)

            articles = [
                {
                    "title": item.get("title", "Untitled"),
                    "source": item.get("source", "Unknown"),
                    "url": item.get("url", "#"),
                    "published_at": item.get("published_at", datetime.utcnow().isoformat()),
                }
                for item in data["data"]
            ]

            if not articles:
                print("⚠️ Empty result set, using mock data")
                return self._get_mock_news(max_items)

            print(f"✅ Successfully fetched {len(articles)} articles from TheNewsAPI")
            return articles[:max_items]

        except requests.exceptions.RequestException as e:
            print(f"🛑 News API error: {e}")
            return self._get_mock_news(max_items)
        except Exception as e:
            print(f"🛑 Unexpected error: {e}")
            return self._get_mock_news(max_items)

    def _get_mock_news(self, limit=5):
        sample_news = [
            {
                "title": "UNDP launches new sustainability initiative across 50 countries",
                "source": "UNDP News",
                "url": "https://www.undp.org",
            },
            {
                "title": "Global ICT infrastructure sees record growth in developing nations",
                "source": "Tech World",
                "url": "https://www.undp.org",
            },
            {
                "title": "AI transforming data-driven governance in public sector",
                "source": "Digital Gov",
                "url": "https://www.undp.org",
            },
            {
                "title": "UN agencies collaborate on digital inclusion framework",
                "source": "UN News",
                "url": "https://www.un.org",
            },
            {
                "title": "Cloud technologies improve disaster resilience and response",
                "source": "Cloud Tech",
                "url": "https://www.undp.org",
            },
        ]
        return [
            {**item, "published_at": datetime.utcnow().isoformat()}
            for item in random.sample(sample_news, min(limit, len(sample_news)))
        ]
