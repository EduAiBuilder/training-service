from app.config import settings
import httpx

async def fetch_trainer_data(trainer_id: int):
    try:
        trainer_service_url = f"{settings.trainer_node_service_url}/trainers/{trainer_id}/categories/images"
        headers = {
            "Authorization": f"Bearer {settings.jwt_token}"
        }
        response = httpx.get(trainer_service_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP error while fetching trainer data: {e}")
    except Exception as e:
        print(f"Error fetching trainer data: {e}")

async def post_epoch_data(data: dict, modelId: int):
    try:
        backend_url = f"{settings.trainer_node_service_url}/models/{modelId}/epochs"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.jwt_token}"
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(backend_url, json=data, headers=headers)
            response.raise_for_status()
    except httpx.HTTPStatusError as e:
        print(f"HTTP error while sending epoch data: {e}")
    except Exception as e:
        print(f"Error sending epoch data: {e}")