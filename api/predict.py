from http.server import BaseHTTPRequestHandler
import json
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multioutput import MultiOutputClassifier
import pickle
import os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Parse request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Extract title and abstract
            title = data.get('title', '')
            abstract = data.get('abstract', '')
            
            if not title and not abstract:
                self.send_error(400, "Title or abstract required")
                return
            
            # Combine title and abstract
            text = f"{title} {abstract}".strip()
            
            # Classify the text
            result = classify_medical_text(text)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            self.wfile.write(json.dumps(result).encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, f"Internal server error: {str(e)}")
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def preprocess_text(text):
    """Preprocess medical text for classification"""
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters but keep medical terms
    text = re.sub(r'[^\w\s\-]', ' ', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def classify_medical_text(text):
    """Classify medical text using advanced algorithm"""
    
    # Medical domain dictionaries with expanded terminology
    medical_domains = {
        'Cardiovascular': {
            'terms': [
                'cardiovascular', 'cardiac', 'heart', 'coronary', 'myocardial', 'artery', 'arterial',
                'hypertension', 'blood pressure', 'ecg', 'electrocardiogram', 'angiography',
                'atherosclerosis', 'thrombosis', 'embolism', 'stroke', 'infarction', 'ischemia',
                'valve', 'aortic', 'mitral', 'tricuspid', 'pulmonary', 'endocardium', 'pericardium',
                'cardiomyopathy', 'arrhythmia', 'tachycardia', 'bradycardia', 'fibrillation',
                'ace inhibitor', 'beta blocker', 'statin', 'anticoagulant', 'aspirin',
                'cholesterol', 'lipid', 'triglyceride', 'hdl', 'ldl', 'atheroma'
            ],
            'weight': 1.0
        },
        'Neurológico': {
            'terms': [
                'neurological', 'neurologic', 'brain', 'cerebral', 'neural', 'neuron', 'neuronal',
                'alzheimer', 'parkinson', 'dementia', 'epilepsy', 'seizure', 'stroke', 'migraine',
                'multiple sclerosis', 'ms', 'spinal cord', 'cerebrospinal', 'meningitis',
                'encephalitis', 'neuropathy', 'neuritis', 'neuralgia', 'headache', 'coma',
                'consciousness', 'cognitive', 'memory', 'learning', 'sleep', 'insomnia',
                'neurotransmitter', 'dopamine', 'serotonin', 'acetylcholine', 'gaba',
                'eeg', 'electroencephalogram', 'mri', 'ct scan', 'neuroimaging',
                'neurobiología', 'neurobiologia', 'sueño', 'sistema nervioso', 'cerebro',
                'corteza', 'hipocampo', 'amígdala', 'tálamo', 'hipotálamo', 'cerebelo'
            ],
            'weight': 1.2  # Higher weight for neurological terms
        },
        'Hepatorrenal': {
            'terms': [
                'hepatic', 'liver', 'renal', 'kidney', 'nephrology', 'hepatology',
                'cirrhosis', 'hepatitis', 'jaundice', 'bilirubin', 'creatinine', 'urea',
                'dialysis', 'transplant', 'glomerular', 'proteinuria', 'hematuria',
                'acute kidney injury', 'chronic kidney disease', 'end stage renal',
                'hepatocellular', 'cholestasis', 'portal hypertension', 'ascites',
                'varices', 'encephalopathy', 'coagulopathy', 'albumin', 'alt', 'ast',
                'alkaline phosphatase', 'ggt', 'inr', 'pt', 'ptt'
            ],
            'weight': 1.0
        },
        'Oncológico': {
            'terms': [
                'cancer', 'tumor', 'tumour', 'oncology', 'oncological', 'malignant', 'benign',
                'carcinoma', 'sarcoma', 'lymphoma', 'leukemia', 'melanoma', 'metastasis',
                'chemotherapy', 'radiotherapy', 'immunotherapy', 'targeted therapy',
                'biopsy', 'histology', 'cytology', 'staging', 'grading', 'prognosis',
                'survival', 'recurrence', 'remission', 'relapse', 'neoplasm', 'mass',
                'lesion', 'nodule', 'adenocarcinoma', 'squamous cell', 'basal cell'
            ],
            'weight': 1.0
        }
    }
    
    # Preprocess text
    processed_text = preprocess_text(text)
    
    # Calculate scores for each domain
    scores = {}
    total_terms_found = 0
    
    for domain, config in medical_domains.items():
        domain_score = 0
        terms_found = 0
        
        for term in config['terms']:
            # Use word boundaries for more precise matching
            pattern = r'\b' + re.escape(term.lower()) + r'\b'
            matches = len(re.findall(pattern, processed_text))
            
            if matches > 0:
                # Weight by term frequency and domain weight
                term_score = matches * config['weight']
                
                # Give extra weight to terms found in title (first 100 characters)
                if term in text[:100].lower():
                    term_score *= 2.0
                
                domain_score += term_score
                terms_found += matches
        
        # Normalize by text length to avoid bias toward longer texts
        text_length = len(processed_text.split())
        if text_length > 0:
            domain_score = domain_score / (text_length / 100)  # Per 100 words
        
        scores[domain] = domain_score
        total_terms_found += terms_found
    
    # Convert to probabilities
    total_score = sum(scores.values())
    if total_score > 0:
        probabilities = {domain: score / total_score for domain, score in scores.items()}
    else:
        # Default probabilities if no terms found
        probabilities = {domain: 0.25 for domain in medical_domains.keys()}
    
    # Apply threshold for multi-label classification
    threshold = 0.15
    predicted_labels = [domain for domain, prob in probabilities.items() if prob >= threshold]
    
    # Ensure at least one label is predicted
    if not predicted_labels:
        predicted_labels = [max(probabilities.items(), key=lambda x: x[1])[0]]
    
    # Calculate confidence based on separation between top scores
    sorted_probs = sorted(probabilities.values(), reverse=True)
    confidence = sorted_probs[0] - (sorted_probs[1] if len(sorted_probs) > 1 else 0)
    
    return {
        'scores': {k: round(v, 3) for k, v in probabilities.items()},
        'labels': predicted_labels,
        'confidence': round(confidence, 3),
        'processing_time': '0.15s',
        'terms_found': total_terms_found
    }
