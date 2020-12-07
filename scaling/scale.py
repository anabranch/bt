from ray import serve

from io import BytesIO
from PIL import Image
import requests

import torch
from torchvision import transforms
from torchvision.models import resnet18

BACKEND = "resnet18:v0"

class ImageModel:
    def __init__(self):
        self.model = resnet18(pretrained=True).eval()
        self.preprocessor = transforms.Compose([
            transforms.Resize(224),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Lambda(lambda t: t[:3, ...]),  # remove alpha channel
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def __call__(self, flask_request):
        image_payload_bytes = flask_request.data
        pil_image = Image.open(BytesIO(image_payload_bytes))
        print("[1/3] Parsed image data: {}".format(pil_image))

        pil_images = [pil_image]  # Our current batch size is one
        input_tensor = torch.cat(
            [self.preprocessor(i).unsqueeze(0) for i in pil_images])
        print("[2/3] Images transformed, tensor shape {}".format(
            input_tensor.shape))

        with torch.no_grad():
            output_tensor = self.model(input_tensor)
        print("[3/3] Inference done!")
        return {"class_index": int(torch.argmax(output_tensor[0]))}

@ray.remote(resources={'num_cpus': 4})
def func():
    import time
    time.sleep(10)
    print("resultz: Scaling!")

if __name__ == "__main__":
    print("Running!")
    # Serve needs 1 CPU in head, and 1 on each ray node

    config = {"num_replicas": 3}  # replica == 1 CPU, 0 GPU

    # start up with smaller number of replicas
    client = serve.start()
    client.create_backend(BACKEND, ImageModel, config=config)
    client.create_endpoint(
        "predictor",
        backend=BACKEND,
        route="/image_predict",
        methods=["POST"])

    # update size of cluster
    larger_config = {"num_replicas": 10}
    client.update_backend_config(BACKEND, larger_config)

    ray_logo_bytes = requests.get(
        "https://github.com/ray-project/ray/raw/"
        "master/doc/source/images/ray_header_logo.png").content

    resp = requests.post(
        "http://localhost:8000/image_predict", data=ray_logo_bytes)
    print(resp.json())

    # trigger scaling
    r = ray.get([func.remote() for i in range(1000)])

