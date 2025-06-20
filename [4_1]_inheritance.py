# -*- coding: utf-8 -*-
"""[4_1] inheritance

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1yJujHKEsSF7IEePZb742kCtLab0ypHHB
"""

class Instrument:
    def __init__(self, name, initial_price):
        self.name = name
        self.initial_price = initial_price

    def get_price(self):
        raise NotImplementedError("Subclass must implement abstract method")

import numpy as np

class BrownianStock(Instrument):
    def __init__(self, name, initial_price, mu, sigma):
        super().__init__(name, initial_price)
        self.mu = mu  # 평균 수익률
        self.sigma = sigma  # 변동성

    def simulate_price(self, time_horizon, steps):
        dt = time_horizon / steps
        prices = [self.initial_price]
        for _ in range(steps):
            dt_price_change = self.mu * prices[-1] * dt + self.sigma * prices[-1] * np.random.normal() * np.sqrt(dt)
            prices.append(prices[-1] + dt_price_change)
        return prices

stock = BrownianStock("AAPL", 150, 0.0002, 0.01)
simulated_prices = stock.simulate_price(time_horizon=1, steps=252)

import matplotlib.pyplot as plt

plt.plot(simulated_prices)
plt.title('Simulated Brownian Motion Stock Prices for AAPL')
plt.xlabel('Time Steps')
plt.ylabel('Price')
plt.show()

stock.get_price()

import numpy as np
import matplotlib.pyplot as plt

import torch

"""# MNIST dataset"""

import tensorflow as tf

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

x_train = torch.tensor(x_train.reshape(60000, 784)/255, dtype=torch.float32)
x_test = torch.tensor(x_test.reshape(10000, 784)/255, dtype=torch.float32)

y_train = torch.tensor(y_train, dtype=torch.long)
y_test = torch.tensor(y_test, dtype=torch.int64)

"""### Model, Parameters, Loss Function"""

import torch.nn.functional as F

w = torch.randn(784, 10, requires_grad=True)
b = torch.randn(10, requires_grad=True)

loss_fn = F.cross_entropy

def model(xb):
    return xb @ w + b

"""### Hyperparameters"""

bs = 64  # batch size
lr = 0.1  # learning rate
epochs = 10 # number of training

n, c = x_train.shape

n

n / bs

(n-1) // bs

for epoch in range(epochs):
    for i in range((n - 1) // bs + 1):
        start_i = i * bs
        end_i = start_i + bs
        xb = x_train[start_i:end_i]
        yb = y_train[start_i:end_i]
        pred = model(xb)
        loss = loss_fn(pred, yb)

        loss.backward()
        with torch.no_grad():
            w -= w.grad * lr
            b -= b.grad * lr
            w.grad.zero_()
            b.grad.zero_()

print(loss)

np.exp(-0.1061)

def accuracy(out, yb):
    preds = torch.argmax(out, dim=1)
    return (preds == yb).float().mean()

accuracy(model(x_train), y_train)

torch.argmax(model(x_train), dim=1)

"""# Refactor using `nn.Module`"""

from torch.nn import Module, Parameter

class MyModel(Module):

    def __init__(self):
        super().__init__()
        self.w = Parameter(torch.randn(784,10))
        self.b = Parameter(torch.randn(10))

    def forward(self, x):
        return x @ self.w + self.b

model = MyModel()

loss = loss_fn(model(x_train), y_train)
loss

loss.backward()

with torch.no_grad():
    for p in model.parameters():
        p -= p.grad * lr
    model.zero_grad()

def fit():

    for epoch in range(epochs):
        for i in range((n - 1) // bs + 1):
            start_i = i * bs
            end_i = start_i + bs
            xb = x_train[start_i:end_i]
            yb = y_train[start_i:end_i]
            pred = model(xb)
            loss = loss_fn(pred, yb)

            loss.backward()
            with torch.no_grad():
                for p in model.parameters():
                    p -= p.grad * lr
                model.zero_grad()

        if epoch % 10 == 0:
            print(loss)

fit()

np.exp(-0.0437)

accuracy(model(x_test), y_test)

"""# Refactoring using `nn.Linear`"""

class MyModel(Module):

    def __init__(self):
        super().__init__()
        self.linear = Linear(784, 10)

    def forward(self, x):
        return self.linear(x)

model = MyModel()
loss_fn(model(x_train), y_train)

np.exp(-2.3165)

fit()

loss_fn(model(x_test), y_test)

loss_fn(model(x_train), y_train)

np.exp(-0.2704)

accuracy(model(x_test), y_test)

"""# Refactoring using `torch.optim`"""

from torch import optim

opt = optim.Adam(model.parameters())

def fit():

    for epoch in range(epochs):
        for i in range((n - 1) // bs + 1):
            start_i = i * bs
            end_i = start_i + bs
            xb = x_train[start_i:end_i]
            yb = y_train[start_i:end_i]
            pred = model(xb)
            loss = loss_fn(pred, yb)

            loss.backward()
            opt.step()
            opt.zero_grad()

        if epoch % 10 == 0:
            print(loss)

fit()

"""# Refactor using `Dataset` and `DataLoader`"""

from torch.utils.data import TensorDataset
from torch.utils.data import DataLoader

x_train.to(dev)

train_ds = TensorDataset(x_train, y_train)
train_dl = DataLoader(train_ds, batch_size=64)

for i in train_dl:
    print(len(i[0][0]))

model = MyModel()
opt = optim.Adam(model.parameters())
epochs=100

def fit():

    for epoch in range(epochs):
        for xb, yb in train_dl:
            xb.to(dev)
            yb.to(dev)
            pred = model(xb)
            loss = loss_fn(pred, yb)

            loss.backward()
            opt.step()
            opt.zero_grad()

        if epoch % 10 == 0:
            print(loss)

fit()

"""# Using GPU"""

import torch

dev = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
print(dev)

import tensorflow as tf

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

x_train = torch.tensor(x_train.reshape(60000, 784)/255, dtype=torch.float32).to(dev)
x_test = torch.tensor(x_test.reshape(10000, 784)/255, dtype=torch.float32).to(dev)

y_train = torch.tensor(y_train, dtype=torch.long).to(dev)
y_test = torch.tensor(y_test, dtype=torch.int64).to(dev)

import torch.nn.functional as F

loss_fn = F.cross_entropy

from torch.nn import *
from torch import optim

class MyModel(Module):

    def __init__(self):
        super().__init__()
        self.linear = Linear(784, 10)

    def forward(self, x):
        return self.linear(x)

from torch.utils.data import TensorDataset
from torch.utils.data import DataLoader

train_ds = TensorDataset(x_train, y_train)
train_dl = DataLoader(train_ds, batch_size=64)

model = MyModel().to(dev)
opt = optim.Adam(model.parameters())
epochs=100

def fit():

    for epoch in range(epochs):
        for xb, yb in train_dl:
            #xb.to(dev)
            #yb.to(dev)
            pred = model(xb)
            loss = loss_fn(pred, yb)

            loss.backward()
            opt.step()
            opt.zero_grad()

        if epoch % 10 == 0:
            print(loss)

fit()

def preprocess(x, y):
    return x.view(-1, 784).to(dev), y.to(dev)


class WrappedDataLoader:
    def __init__(self, dl, func):
        self.dl = dl
        self.func = func

    def __len__(self):
        return len(self.dl)

    def __iter__(self):
        for b in self.dl:
            yield (self.func(*b))


train_dl = WrappedDataLoader(train_dl, preprocess)

