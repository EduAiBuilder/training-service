from app.models_trainer.trainer_client import fetch_trainer_data
from app.models_trainer.classes import Trainer_images_by_category_response
from fastai.vision.all import Path, download_images

async def train_model(trainer_id):
    trainer_images: list[Trainer_images_by_category_response] = await fetch_trainer_data(trainer_id)
    save_images_by_category(trainer_id, trainer_images)


def save_images_by_category(trainer_id: str, trainer_images: list[Trainer_images_by_category_response]):
    path = Path(f'app/models_trainer/images/{trainer_id}')

    if not path.exists():
        path.mkdir()
    for image in trainer_images:
        category = image.get('category')
        urls= image.get('imageUrls')
        dest = (path/category)
        dest.mkdir(exist_ok=True)
        download_images(dest, urls=urls)
