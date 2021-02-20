import torch
from torch.nn import Module, Linear


class EuclideanDiscriminator(Module):
    def __init__(self):
        super().__init__()
        self.linear = Linear(1, 1)

    def forward(self, x1, x2):
        diff = x1 - x2

        distance = torch.sqrt(torch.sum(diff * diff, dim=1))

        probability = torch.sigmoid(self.linear(distance.unsqueeze(1)))

        return probability