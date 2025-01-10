import os
import ast
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
import shutil

batch_size = 4
num_epochs = 20000
animation_data_path = "input_animation_data"
lr = 1e-4

# Dataset creation: Read animation data (series of rotations in text file) and create dataset for training ----------------------
def create_dataset():
    data_files = os.listdir(animation_data_path)

    x = []

    for d in data_files:
        if d == "BoneOrder.txt":
            continue

        with open(animation_data_path + "/" + d) as f:
            new_data = ast.literal_eval(f.read())

        new_data = torch.tensor(new_data)
        x.append(new_data)

    dataset = torch.stack(x)
    dataset = TensorDataset(dataset)
    return dataset

dataset = create_dataset()
input_dimension = dataset[0][0].shape[1]
seq_length = dataset[0][0].shape[0]

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def weights_init(m):
    if isinstance(m, nn.Linear):
        nn.init.xavier_normal_(m.weight)
        nn.init.zeros_(m.bias)

# Create LSTM VAE -------------------------------------------------------------------------------------
class VAE(nn.Module):
    def __init__(self, input_dim, seq_length, hidden_dim=128, latent_dim=64):
        super(VAE, self).__init__()
        self.seq_length = seq_length
        self.latent_dim = latent_dim
        self.encoder = nn.LSTM(input_dim, hidden_dim, batch_first=True, num_layers=2)

        self.mean_layer = nn.Linear(hidden_dim, latent_dim)
        self.logvar_layer = nn.Linear(hidden_dim, latent_dim)

        self.decoder = nn.LSTM(latent_dim, hidden_dim, batch_first=True, num_layers=2)
        self.fc_out = nn.Linear(hidden_dim, input_dim)

    def encode(self, x):
        _, (h_n, _) = self.encoder(x)
        h_n = h_n[-1]
        mean, logvar = self.mean_layer(h_n), self.logvar_layer(h_n)
        return mean, logvar
    
    def decode(self, z):
        z = z.unsqueeze(1).repeat(1, self.seq_length, 1)
        lstm_out, _ = self.decoder(z)
        recon_x = self.fc_out(lstm_out) 
        return recon_x

    def reparameterization(self, mean, var):
        eps = torch.rand_like(var).to(device)
        std = torch.exp(0.5 * var)
        z = mean + std * eps
        return z
    
    def forward(self,x):
        mean, logvar = self.encode(x)
        z = self.reparameterization(mean, logvar)
        x_hat = self.decode(z)
        return x_hat, mean, logvar
    
    def generate_sample(self):
        mean = torch.randn(1, self.latent_dim).to(device)
        logvar = torch.randn(1, self.latent_dim).to(device)
        z_sample = self.reparameterization(mean, logvar)
        return model.decode(z_sample).squeeze(0)


# Define optimisers, loss function and create data loaders -------------------------------------------------------
def loss_function(x, x_hat, mean, log_var):
    reproduction_loss = nn.MSELoss()(x_hat, x)
    KLD = - 0.5 * torch.sum(1 + log_var - mean.pow(2) - log_var.exp())
    return reproduction_loss + KLD

train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=False)

model = VAE(input_dimension, seq_length).to(device)
model.apply(weights_init)

optimizer = torch.optim.Adam(model.parameters(), lr=lr)

# Training -------------------------------------------------------------------------------------------------------
def train(model, optimizer, epochs, device, x_dim=input_dimension):
    model.train()

    for epoch in range(epochs):
        overall_loss = 0
        for batch_idx, (x,) in enumerate(train_loader):
            x = torch.stack([torch.tensor(sample) for sample in x]).to(device)
            optimizer.zero_grad()
            recon_x, mu, logvar = model(x)
            loss = loss_function(recon_x, x, mu, logvar)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            overall_loss += loss.item()

        print(f"Epoch {epoch}: Avg loss: {overall_loss/ (batch_idx*batch_size)}")
    return overall_loss

train(model, optimizer, num_epochs, device=device)

# Generate animation samples from model -------------------------------------------------------------------------
gen_dir = "generated_animation_data"
sample_outputs = 15

if os.path.exists(gen_dir):
    shutil.rmtree(gen_dir)

os.makedirs(gen_dir)

for i in range(sample_outputs):
    gen_anim = model.generate_sample()

    with open(gen_dir + f"/Generated_Data_{i + 1}.txt", "w") as file:
        file.write(str(gen_anim.tolist()))

print("Generated animations written to file.")