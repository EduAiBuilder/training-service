from .s3 import upload_to_s3
from .trainer_client import fetch_trainer_data, post_epoch_data
from .classes import Trainer_images_by_category_response
from fastbook import *
from fastai.vision.all import *
import io

async def main_training_process(trainer_id: int, model_id: int, model_key: str):
    trainer_images: list[Trainer_images_by_category_response] = await fetch_trainer_data(trainer_id)
    path = save_images_by_category(trainer_id, trainer_images)
    dls = set_data_loaders(path)
    export_path = f'app/models_trainer/export/{model_id}.pkl'
    train_and_export_model(dls,export_path,model_id)
    upload_to_s3(trainer_id, export_path, model_key)


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

async def train_and_export_model(dls, export_path: str, model_id: int):
    learn = vision_learner(dls, resnet18, metrics=error_rate)
    learn.add_cb(SaveModelCallback(every_epoch=True, with_opt=True))
    
    for epoch in range(4):
        learn.fine_tune(1)
        metrics = learn.validate()
        await send_epoch_data(model_id, epoch, metrics)
    
    learn.export(export_path)

async def send_epoch_data(model_id: str, epoch_number: int, metrics: list):
    epoch_data = {
        "epochNumber": epoch_number,
        "lossValue": metrics[0].item(),
        "accuracyValue": metrics[1].item(),
        "valLossValue": metrics[2].item(),
        "valAccuracyValue": metrics[3].item(),
        "learningRate": 0.001,  
        "timeElapsed": 0  
    }
    await post_epoch_data(epoch_data, model_id)
