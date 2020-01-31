from torch.utils.data import DataLoader, random_split
from torch import nn
from torchvision import transforms
import tqdm
import torch
# from torchvision.transforms import Compose
from torch.optim import Adam
from torch.nn import BCELoss
from utils import *
from models import *


random_seed = 213
batch_size = 1
lr = 0.001
n_epochs = 5

transform_train = transforms.Compose(
    [
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[
            0.229, 0.224, 0.225]),
    ]
)

transform_val = transforms.Compose(
    [
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[
            0.229, 0.224, 0.225]),
    ]
)


model = MobileUnet().to('cuda')
criterion = BCELoss().to('cuda')
optimizer = Adam(model.parameters(), lr=lr)

train_data = dira20(
    '/home/ken/Documents/test_tensorRT/dataset/', train=True)
# val_data = dira20('/home/ken/Documents/test_tensorRT/dataset/', train=True)

train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True)
# val_loader = DataLoader(val_data, batch_size=batch_size)

running_loss = 0.0
for e in tqdm.tqdm(range(n_epochs)):
    for i, data in enumerate(train_loader, 0):
        inputs, labels = data
        inputs = inputs.to('cuda')
        labels = labels.to('cuda')
        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        # print statistics
    print(loss)
    # e.update()
print('Finished Training {}'.format(loss))

torch.save(model.state_dict(), './baseline.pt')
# model.eval()
# im = model(train_data[0][0].to('cuda').unsqueeze(0))[0].cpu()
# print(im.shape)
# transforms.ToPILImage(mode='L')(im).save('train.jpg')
