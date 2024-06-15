from app.models_trainer.trainer_client import fetch_trainer_data

async def train_model(trainer_id):
    trainer_images = await fetch_trainer_data(trainer_id)
    print(trainer_images)