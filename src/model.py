import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel, AutoConfig
from sklearn.metrics import f1_score, classification_report, multilabel_confusion_matrix
import numpy as np
import logging

logger = logging.getLogger(__name__)

class MedicalClassifier(nn.Module):
    """
    Clasificador médico basado en BioBERT/ClinicalBERT
    """
    
    def __init__(self, model_name='emilyalsentzer/Bio_Discharge_Summary_BERT', num_labels=4, dropout_rate=0.3):
        super(MedicalClassifier, self).__init__()
        
        self.model_name = model_name
        self.num_labels = num_labels
        
        # Cargar modelo pre-entrenado
        self.config = AutoConfig.from_pretrained(model_name)
        self.bert = AutoModel.from_pretrained(model_name)
        
        # Capas de clasificación
        self.dropout = nn.Dropout(dropout_rate)
        self.classifier = nn.Linear(self.config.hidden_size, num_labels)
        
        # Inicialización de pesos
        nn.init.xavier_uniform_(self.classifier.weight)
        nn.init.zeros_(self.classifier.bias)
    
    def forward(self, input_ids, attention_mask=None, token_type_ids=None):
        # Obtener representaciones del modelo BERT
        outputs = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids
        )
        
        # Usar el token [CLS] para clasificación
        pooled_output = outputs.pooler_output
        pooled_output = self.dropout(pooled_output)
        
        # Clasificación multi-etiqueta
        logits = self.classifier(pooled_output)
        
        return logits

class MedicalClassifierTrainer:
    """
    Entrenador para el clasificador médico
    """
    
    def __init__(self, model_name='emilyalsentzer/Bio_Discharge_Summary_BERT', max_length=512):
        self.model_name = model_name
        self.max_length = max_length
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        logger.info(f"Usando dispositivo: {self.device}")
    
    def tokenize_texts(self, texts):
        """Tokeniza los textos"""
        return self.tokenizer(
            texts.tolist(),
            truncation=True,
            padding=True,
            max_length=self.max_length,
            return_tensors='pt'
        )
    
    def train_model(self, data_dict, epochs=3, batch_size=16, learning_rate=2e-5):
        """Entrena el modelo"""
        
        # Crear modelo
        model = MedicalClassifier(self.model_name, num_labels=len(data_dict['classes']))
        model.to(self.device)
        
        # Tokenizar datos
        train_encodings = self.tokenize_texts(data_dict['X_train'])
        val_encodings = self.tokenize_texts(data_dict['X_val'])
        
        # Configurar optimizador
        optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
        criterion = nn.BCEWithLogitsLoss()
        
        # Entrenamiento
        model.train()
        best_f1 = 0
        
        for epoch in range(epochs):
            total_loss = 0
            
            # Procesar en batches
            for i in range(0, len(data_dict['X_train']), batch_size):
                batch_end = min(i + batch_size, len(data_dict['X_train']))
                
                # Preparar batch
                input_ids = train_encodings['input_ids'][i:batch_end].to(self.device)
                attention_mask = train_encodings['attention_mask'][i:batch_end].to(self.device)
                labels = torch.tensor(data_dict['y_train'][i:batch_end], dtype=torch.float).to(self.device)
                
                # Forward pass
                optimizer.zero_grad()
                logits = model(input_ids, attention_mask)
                loss = criterion(logits, labels)
                
                # Backward pass
                loss.backward()
                optimizer.step()
                
                total_loss += loss.item()
            
            # Validación
            val_f1 = self.evaluate_model(model, val_encodings, data_dict['y_val'])
            
            logger.info(f"Epoch {epoch+1}/{epochs} - Loss: {total_loss:.4f} - Val F1: {val_f1:.4f}")
            
            if val_f1 > best_f1:
                best_f1 = val_f1
                torch.save(model.state_dict(), 'best_model.pth')
        
        return model
    
    def evaluate_model(self, model, encodings, y_true, batch_size=32):
        """Evalúa el modelo"""
        model.eval()
        predictions = []
        
        with torch.no_grad():
            for i in range(0, len(y_true), batch_size):
                batch_end = min(i + batch_size, len(y_true))
                
                input_ids = encodings['input_ids'][i:batch_end].to(self.device)
                attention_mask = encodings['attention_mask'][i:batch_end].to(self.device)
                
                logits = model(input_ids, attention_mask)
                probs = torch.sigmoid(logits)
                batch_preds = (probs > 0.5).cpu().numpy()
                predictions.extend(batch_preds)
        
        predictions = np.array(predictions)
        f1 = f1_score(y_true, predictions, average='weighted')
        
        return f1
    
    def predict(self, model, texts, threshold=0.5):
        """Realiza predicciones"""
        model.eval()
        encodings = self.tokenize_texts(texts)
        
        with torch.no_grad():
            input_ids = encodings['input_ids'].to(self.device)
            attention_mask = encodings['attention_mask'].to(self.device)
            
            logits = model(input_ids, attention_mask)
            probs = torch.sigmoid(logits)
            predictions = (probs > threshold).cpu().numpy()
        
        return predictions, probs.cpu().numpy()
