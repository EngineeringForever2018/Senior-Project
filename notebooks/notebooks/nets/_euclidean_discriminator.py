import torch
from torch.nn import Module, Linear


class EuclideanDiscriminator(Module):
    def __init__(self, n=1):
        super().__init__()
        self.linear = Linear(1, 1)
        self.n = n

    def forward(self, x1, x2):
        x1 = torch.reshape(x1, [-1, self.n, x1.shape[1]])
        x2 = torch.reshape(x2, [-1, self.n, x2.shape[1]])

        x1 = torch.mean(x1, dim=1)
        x2 = torch.mean(x2, dim=1)

        diff = x1 - x2

        distance = torch.sqrt(torch.sum(diff * diff, dim=1))

        probability = torch.sigmoid(self.linear(distance.unsqueeze(1)))

        return probability
