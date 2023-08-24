import torch
import torch.nn as nn
import torch.optim as optim

class LSTM(torch.nn.Moudule):
    def __init__(self,input_size, word2vec_size, hidden_size, num_classes, num_layers = 2, dropout = 0 ):
        super().__init__()
        self.input_size = input_size
        self.word2vec_size = word2vec_size
        self.hidden_size = hidden_size
        self.num_classes = num_classes
        self.num_layers = num_layers
        self.dropout = dropout
    
        self.emb = nn.Embedding(input_size, word2vec_size)
        self.lstm = nn.LSTM(input_size = word2vec_size,
                            hidden_size = hidden_size,
                            num_layers = num_layers
                            dropout = dropout,
                            batch_first = True,
        )
        
        self.linear = nn.linear(hidden_size, num_classes)
        self.activation = nn.Softmax(dim=-1)
        
    def forward(self, x):
        #|x| = batch_size, length
        x = self.emb(x)
        #|x| = batch_size,length,word2vec_size
        x,_ = self.lstm(x)
        #|x| = batch_size,length,hidden_size
        y = self.activation(self.linear(x[:,-1]))
        #|y| = batch_size,length,num_classes       
        
        return y