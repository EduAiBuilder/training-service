from .trainer_client import fetch_trainer_data
from .classes import Trainer_images_by_category_response
from .trainer_callback import ProgressCallback
from fastbook import *
from fastai.vision.all import *

async def main_training_process(trainer_id):
    trainer_images: list[Trainer_images_by_category_response] = await fetch_trainer_data(trainer_id)
    path = save_images_by_category(trainer_id, trainer_images)
    dls = set_data_loaders(path)
    model = train_and_export_model(dls)


def save_images_by_category(trainer_id: str, trainer_images: list[Trainer_images_by_category_response]):
    if trainer_id == 6:
        return Path(f'app/models_trainer/images/{trainer_id}')
    
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
    animals = DataBlock(
        blocks=(ImageBlock, CategoryBlock),
        get_items=get_image_files,
        splitter=RandomSplitter(valid_pct=0.2, seed=42),
        get_y=parent_label,
        item_tfms=RandomResizedCrop(224, min_scale=0.5),
    )
    dls = animals.dataloaders(path)
    print(f"Number of classes: {dls}")  # Check number of classes
    return dls

def train_and_export_model(dls):
    learn = vision_learner(dls, resnet18, metrics=error_rate, cbs=[ProgressCallback('http://localhost:8000/trainer/progress')])
    learn.fine_tune(4)
    learn.remove_cbs(ProgressCallback)
    learn.export()  
    return learn

