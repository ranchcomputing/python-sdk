class PostRequest:
    def __init__(self, url, body):
        self._url = url
        self._body = body


class MockResponse:
    def __init__(self, status_code: int, data: dict = None) -> None:
        self.status_code = status_code
        self._json = data

    def json(self) -> dict:
        return self._json


class MockConnection:
    def __init__(self) -> None:
        pass

    def _post(self, url: str, data: dict) -> dict:
        return MockResponse(200)

    @property
    def get_cpu_prioritys(self) -> dict:
        return {
            "occupation": {"rendering": 4, "queued": 0},
            "priorities": [
                {
                    "id": 1,
                    "name": "CPU-Low",
                    "price": "0.016000",
                    "anim_max_allocated_nodes": 24,
                    "farm": "power",
                    "farm_type": "power",
                },
                {
                    "id": 3,
                    "name": "CPU-Medium",
                    "price": "0.018000",
                    "anim_max_allocated_nodes": 48,
                    "farm": "power",
                    "farm_type": "power",
                },
            ],
        }

    @property
    def get_cpu_rendering_occupation(self) -> int:
        return self.get_cpu_prioritys.get("occupation")["rendering"]

    @property
    def get_cpu_queued_occupation(self) -> int:
        return self.get_cpu_prioritys.get("occupation")["queued"]
