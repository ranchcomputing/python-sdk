import pytest


@pytest.fixture
def data():
    return {"renderer_id": 226, "priority_id": 1, "disclaimer": True, "email": "flouguet@wanadoo.fr"}


# response = {
#             "success": True,
#             "metadata": {
#                 "project_id": "952917",
#                 "user_id": "18820"
#             },
#             "tuspload": {
#                 "endpoint": "https://barn.ranchcomputing.fr/upload/",
#                 "speedtest": "https://barn.ranchcomputing.fr/speedtest/",
#                 "name": "via Cloudflare",
#                 "chunkSize": 90000001
#             }
#         }
