import os
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset
from transformers import BertTokenizer, BertModel, AdamW, get_linear_schedule_with_warmup
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd

class Net(nn.Module):
    """
    The model class, which defines our classifier.
    """
    def __init__(self):
        """
        The constructor of the model.
        """
        super().__init__()
        self.fc1 = nn.Linear(768, 1536)
        self.fc1_bn = nn.BatchNorm1d(1536)
        self.fc1_drop = nn.Dropout(p=0.5)
        self.fc2 = nn.Linear(1536, 768)
        self.fc2_bn = nn.BatchNorm1d(768)
        self.fc2_drop = nn.Dropout(p=0.2)
        self.fc3 = nn.Linear(768, 1)

    def forward(self, x):
        """
        The forward pass of the model.

        input: x: torch.Tensor, the input to the model

        output: x: torch.Tensor, the output of the model
        """
        x = nn.functional.relu(self.fc1_bn(self.fc1(x)))
        x = self.fc1_drop(x)
        x = nn.functional.relu(self.fc2_bn(self.fc2(x)))
        x = self.fc2_drop(x)
        x = self.fc3(x)
        return x