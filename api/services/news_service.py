import requests
import os
from datetime import datetime
from config import Config

class NewsService:

    BASE_URL = "https://api.thenewsapi.com/v1/news/top"

    def __init__(self, api_key=None):
        self.api_key = api_key or Config.NEWS_API_KEY

    def get_latest_news(self, limit=5, language="en"):
        if not self.api_key or self.api_key.strip() == "":
            print("⚠️ Using mock news data (no valid NEWS_API_KEY found)")
            return self._get_mock_news(limit)

        try:
            params = {
                "api_token": self.api_key,
                "language": language,
                "limit": limit,
            }

            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if "error" in data:
                print(f"⚠️ News API returned error: {data.get('error')}")
                return self._get_mock_news(limit)

            news_list = []
            for item in data.get("data", []):
                news_list.append({
                    "title": item.get("title", "Untitled"),
                    "source": item.get("source", "Unknown"),
                    "url": item.get("url", "#"),
                    "published_at": item.get("published_at", datetime.utcnow().isoformat()),
                })

            if not news_list:
                print("⚠️ No news returned from API, using mock data")
                return self._get_mock_news(limit)

            print(f"✅ Successfully fetched {len(news_list)} news articles")
            return news_list

        except requests.exceptions.Timeout:
            print(f"🛑 News API timeout - using mock data")
            return self._get_mock_news(limit)
        except requests.exceptions.RequestException as e:
            print(f"🛑 News API error: {e} - using mock data")
            return self._get_mock_news(limit)
        except Exception as e:
            print(f"🛑 Unexpected error in news service: {e} - using mock data")
            return self._get_mock_news(limit)

    def _get_mock_news(self, limit=5):
        import random

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
            {
                "title": "Cybersecurity becomes top priority for international organizations",
                "source": "Cyber News",
                "url": "https://www.undp.org",
            },
            {
                "title": "5G networks expand to remote regions, bridging digital divide",
                "source": "Telecom Today",
                "url": "https://www.undp.org",
            },
        ]

        selected = random.sample(sample_news, min(limit, len(sample_news)))
        
        return [
            {
                **item,
                "published_at": datetime.utcnow().isoformat()
            }
            for item in selected
        ]