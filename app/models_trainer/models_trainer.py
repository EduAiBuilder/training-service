from app.models_trainer.trainer_client import fetch_trainer_data
from app.models_trainer.classes import Trainer_images_by_category_response
from fastai.vision.all import Path, download_images, get_image_files, verify_images, DataBlock, ImageBlock, CategoryBlock, parent_label, RandomSplitter, RandomResizedCrop, aug_transforms, vision_learner, resnet18, error_rate

async def train_model(trainer_id):
    trainer_images: list[Trainer_images_by_category_response] = await fetch_trainer_data(trainer_id)
    path = save_images_by_category(trainer_id, trainer_images)
    dls = set_data_loaders(path)
    model = train_model(dls)



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
    return path

def set_data_loaders(path):
    fns = get_image_files(path)
    failed = verify_images(fns)
    failed.map(Path.unlink);
    animals = DataBlock(
        blocks=(ImageBlock, CategoryBlock),
        get_items=get_image_files,
        splitter=RandomSplitter(valid_pct=0.2, seed=42),
        get_y=parent_label,
        item_tfms=RandomResizedCrop(224, min_scale=0.5),
        batch_tfms=aug_transforms(),
    )
    return animals.dataloaders(path)

def train_model(dls):
    learn = vision_learner(dls, resnet18, metrics=error_rate)
    learn.fine_tune(4)
    return learn.export()


