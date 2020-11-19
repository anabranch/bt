# Original Code here:
# https://github.com/pytorch/examples/blob/master/mnist/main.py
import argparse
import logging
import os
import torch
import torch.optim as optim
from torch.nn.parallel import DistributedDataParallel

import ray
from ray import tune
from ray.tune.examples.mnist_pytorch import train, test, get_data_loaders, ConvNet
from ray.tune.integration.torch import (
    DistributedTrainableCreator,
    distributed_checkpoint_dir,
)

logger = logging.getLogger(__name__)


def train_mnist(config, checkpoint_dir=False):
    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")
    train_loader, test_loader = get_data_loaders()
    model = ConvNet().to(device)
    optimizer = optim.SGD(model.parameters(), lr=0.1)

    if checkpoint_dir:
        with open(os.path.join(checkpoint_dir, "checkpoint")) as f:
            model_state, optimizer_state = torch.load(f)

        model.load_state_dict(model_state)
        optimizer.load_state_dict(optimizer_state)

    model = DistributedDataParallel(model)

    for epoch in range(400):
        train(model, optimizer, train_loader, device)
        acc = test(model, test_loader, device)

        if epoch % 3 == 0:
            with distributed_checkpoint_dir(step=epoch) as checkpoint_dir:
                path = os.path.join(checkpoint_dir, "checkpoint")
                torch.save((model.state_dict(), optimizer.state_dict()), path)
        tune.report(mean_accuracy=acc)


if __name__ == "__main__":
    training_iter = 10
    n_samples = 4

    if os.environ.get("ANYSCALE_HOST", None):
        print("Running on Anyscale")
        training_iter = 20
        n_samples = 10

    ray.init()
    trainable_cls = DistributedTrainableCreator(train_mnist)
    tune.run(
        trainable_cls, num_samples=n_samples, stop={"training_iteration": training_iter}
    )
