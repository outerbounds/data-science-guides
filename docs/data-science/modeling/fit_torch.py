from metaflow import (FlowSpec, step, Parameter, 
                      conda_base)
from torch_utilities import (train, test, Net, 
                             get_data_loaders)

@conda_base(libraries={"pytorch":"1.11.0", 
                       "torchvision":"0.12.0"}, 
            python="3.8")
class TorchFlow(FlowSpec):
    
    lr = Parameter('lr', default=0.01)
    epochs = Parameter('epochs', default=1)
    
    @step
    def start(self):
        self.next(self.get_data)
        
    @step
    def get_data(self):
        import torch
        train_dataset, train_args = get_data_loaders()
        test_dataset, test_args = get_data_loaders(
            "test")
        self.train_loader = torch.utils.data.DataLoader(
            train_dataset, **train_args)
        self.test_loader = torch.utils.data.DataLoader(
            test_dataset, **test_args)
        self.next(self.fit_model)

    @step
    def fit_model(self):
        import torch
        import torch.optim as optim
        from torch.optim.lr_scheduler import StepLR
        self.model = Net()
        optimizer = optim.Adadelta(
            self.model.parameters(), lr=self.lr)
        scheduler = StepLR(optimizer, step_size=1)
        for epoch in range(1, self.epochs + 1):
            train(self.model, self.train_loader, 
                  optimizer, epoch)
            _ = test(self.model, self.test_loader)
            scheduler.step()
        self.next(self.evaluate_model)
        
    @step
    def evaluate_model(self):
        self.test_score = test(self.model, 
                               self.test_loader)
        print(f"Model scored {100*self.test_score}%")
        self.next(self.end)
        
    @step
    def end(self):
        pass
    
if __name__ == "__main__":
    TorchFlow()
    
