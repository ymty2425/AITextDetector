import pandas as pd
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class LLM:
    
    def __init__(self, checkpoint_path: str, max_len: int) -> None:
        self.MAX_LEN = max_len
        
        self.tokenizer = AutoTokenizer.from_pretrained(checkpoint_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(checkpoint_path)
        
    
    def predict(self, text):
        inputs = self.tokenizer(text, padding=True, truncation=True, max_length=self.MAX_LEN, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs)
        logits = outputs.logits
        predictions = torch.argmax(logits, dim=-1).item()
        return predictions

