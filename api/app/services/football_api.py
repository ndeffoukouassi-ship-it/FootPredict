import httpx
from typing import Optional, List, Dict, Any
from app.core.config import settings
from datetime import date


class FootballAPI:
    def __init__(self):
        self.base_url = settings.API_FOOTBALL_BASE_URL
        self.headers = {
            "x-apisports-key": settings.API_FOOTBALL_KEY
        }

    async def _request(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.base_url}/{endpoint}",
                headers=self.headers,
                params=params or {}
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("errors"):
                raise Exception(f"API Error: {data['errors']}")
            
            return data

    async def get_fixtures_today(self) -> List[Dict]:
        """Récupère les matchs du jour"""
        today = date.today().isoformat()
        data = await self._request("fixtures", {"date": today})
        return data.get("response", [])

    async def get_fixture_by_id(self, fixture_id: int) -> Dict:
        data = await self._request("fixtures", {"id": fixture_id})
        response = data.get("response", [])
        return response[0] if response else {}

    async def get_last_fixtures(self, team_id: int, last: int = 10) -> List[Dict]:
        data = await self._request("fixtures", {
            "team": team_id,
            "last": last
        })
        return data.get("response", [])

    async def get_head_to_head(self, team1_id: int, team2_id: int, last: int = 10) -> List[Dict]:
        data = await self._request("fixtures/headtohead", {
            "h2h": f"{team1_id}-{team2_id}",
            "last": last
        })
        return data.get("response", [])

    async def get_injuries(self, fixture_id: int) -> List[Dict]:
        data = await self._request("injuries", {"fixture": fixture_id})
        return data.get("response", [])


football_api = FootballAPI()
