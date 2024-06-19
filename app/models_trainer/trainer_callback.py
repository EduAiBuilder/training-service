import aiohttp  
from fastbook import *
from fastai.vision.all import *

class ProgressCallback(Callback):
    def __init__(self, service_url):
        self.service_url = service_url
    
    async def send_update(self, message):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.service_url, json=message) as resp:
                print(await resp.text())

    def after_epoch(self):
        message = {
            'epoch': self.epoch,
            'train_loss': float(self.learn.recorder.log[0]),
            'valid_loss': float(self.learn.recorder.log[1]),
            'error_rate': float(self.learn.recorder.log[2])
        }
        print(f"Sending update: {message}")