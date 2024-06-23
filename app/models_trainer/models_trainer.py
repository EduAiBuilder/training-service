from .s3 import upload_to_s3
from .trainer_client import fetch_trainer_data
from .classes import Trainer_images_by_category_response
from .trainer_callback import ProgressCallback
from fastbook import *
from fastai.vision.all import *
import io

async def main_training_process(trainer_id: int):
    trainer_images: list[Trainer_images_by_category_response] = await fetch_trainer_data(trainer_id)
    path = save_images_by_category(trainer_id, trainer_images)
    dls = set_data_loaders(path)
    export_path = f'app/models_trainer/export/{trainer_id}.pkl'
    train_and_export_model(dls,export_path)
    upload_to_s3(trainer_id,export_path)


def save_images_by_category(trainer_id: str, trainer_images: list[Trainer_images_by_category_response]):
    path = Path(f'app/models_trainer/images/{trainer_id}')

    if not path.exists():
        path.mkdir(parents=True)
    for image in trainer_images:
        category = image.get('category')
        urls = image.get('imageUrls')
        dest = (path / category)
        dest.mkdir(exist_ok=True)
        download_images(dest, urls=urls) 
    return path

def set_data_loaders(path):
    fns = get_image_files(path)
    failed = verify_images(fns)
    failed.map(Path.unlink)  # Remove failed images
    data_block = DataBlock(
        blocks=(ImageBlock, CategoryBlock),
        get_items=get_image_files,
        splitter=RandomSplitter(valid_pct=0.2, seed=42),
        get_y=parent_label,
        item_tfms=RandomResizedCrop(224, min_scale=0.5),
    )
    dls = data_block.dataloaders(path)
    print(f"Number of classes: {dls}")  # Check number of classes
    return dls

def train_and_export_model(dls,export_path:str):
    learn = vision_learner(dls, resnet18, metrics=error_rate)
    learn.fine_tune(4)
    learn.export(export_path)
    return

