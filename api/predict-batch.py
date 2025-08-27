from http.server import BaseHTTPRequestHandler
import json
import csv
import io
import re
import math
import time

def preprocess_text(text):
    """Preprocess medical text for classification"""
    text = text.lower()
    text = re.sub(r'[^\w\s\-]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def classify_medical_text(text):
    """Classify medical text using lightweight algorithm optimized for Vercel"""
    start_time = time.time()
    
    medical_domains = {
        'Cardiovascular': {
            'terms': [
                'cardiovascular', 'cardiac', 'heart', 'coronary', 'myocardial', 'artery', 'arterial',
                'hypertension', 'blood pressure', 'ecg', 'electrocardiogram', 'angiography',
                'atherosclerosis', 'thrombosis', 'embolism', 'stroke', 'infarction', 'ischemia',
                'valve', 'aortic', 'mitral', 'tricuspid', 'pulmonary', 'endocardium', 'pericardium',
                'cardiomyopathy', 'arrhythmia', 'tachycardia', 'bradycardia', 'fibrillation',
                'ace inhibitor', 'beta blocker', 'statin', 'anticoagulant', 'aspirin',
                'cholesterol', 'lipid', 'triglyceride', 'hdl', 'ldl', 'atheroma', 'angina',
                'bypass', 'angioplasty', 'stent', 'pacemaker', 'defibrillator', 'catheter'
            ],
            'weight': 1.0,
            'context_boost': ['cardiology', 'cardiologist', 'heart disease', 'cardiac surgery']
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
                'corteza', 'hipocampo', 'amígdala', 'tálamo', 'hipotálamo', 'cerebelo',
                'neuroplasticity', 'synapse', 'axon', 'dendrite', 'myelin', 'glia'
            ],
            'weight': 1.3,
            'context_boost': ['neurology', 'neurologist', 'brain disorder', 'nervous system']
        },
        'Hepatorrenal': {
            'terms': [
                'hepatic', 'liver', 'renal', 'kidney', 'nephrology', 'hepatology',
                'cirrhosis', 'hepatitis', 'jaundice', 'bilirubin', 'creatinine', 'urea',
                'dialysis', 'transplant', 'glomerular', 'proteinuria', 'hematuria',
                'acute kidney injury', 'chronic kidney disease', 'end stage renal',
                'hepatocellular', 'cholestasis', 'portal hypertension', 'ascites',
                'varices', 'encephalopathy', 'coagulopathy', 'albumin', 'alt', 'ast',
                'alkaline phosphatase', 'ggt', 'inr', 'pt', 'ptt', 'hepatorenal',
                'nephritis', 'glomerulonephritis', 'pyelonephritis', 'uremia'
            ],
            'weight': 1.0,
            'context_boost': ['hepatology', 'nephrology', 'liver disease', 'kidney disease']
        },
        'Oncológico': {
            'terms': [
                'cancer', 'tumor', 'tumour', 'oncology', 'oncological', 'malignant', 'benign',
                'carcinoma', 'sarcoma', 'lymphoma', 'leukemia', 'melanoma', 'metastasis',
                'chemotherapy', 'radiotherapy', 'immunotherapy', 'targeted therapy',
                'biopsy', 'histology', 'cytology', 'staging', 'grading', 'prognosis',
                'survival', 'recurrence', 'remission', 'relapse', 'neoplasm', 'mass',
                'lesion', 'nodule', 'adenocarcinoma', 'squamous cell', 'basal cell',
                'oncogene', 'tumor suppressor', 'p53', 'brca', 'her2', 'egfr'
            ],
            'weight': 1.0,
            'context_boost': ['oncology', 'oncologist', 'cancer treatment', 'tumor therapy']
        }
    }
    
    processed_text = preprocess_text(text)
    title_text = preprocess_text(text.split('.')[0]) if text else ""  # Approximate title from first sentence
    
    scores = {}
    domain_details = {}
    
    for domain, config in medical_domains.items():
        domain_score = 0
        terms_found = []
        context_matches = 0
        
        for term in config['terms']:
            pattern = r'\b' + re.escape(term.lower()) + r'\b'
            matches = len(re.findall(pattern, processed_text))
            
            if matches > 0:
                term_score = matches * config['weight']
                
                if re.search(pattern, title_text):
                    term_score *= 8.0
                
                first_words = ' '.join(processed_text.split()[:50])
                if re.search(pattern, first_words):
                    term_score *= 1.5
                
                domain_score += term_score
                terms_found.append(term)
        
        for context_term in config.get('context_boost', []):
            pattern = r'\b' + re.escape(context_term.lower()) + r'\b'
            if re.search(pattern, processed_text):
                context_matches += 1
                domain_score *= 1.2
        
        text_length = len(processed_text.split())
        if text_length > 0:
            length_factor = min(text_length / 50, 2.0)
            domain_score = domain_score / length_factor
        
        if domain == 'Neurológico':
            neuro_indicators = ['neurobiología', 'sueño', 'cerebro', 'sistema nervioso', 'neurological', 'brain']
            strong_neuro_match = any(indicator in processed_text for indicator in neuro_indicators)
            if strong_neuro_match:
                domain_score *= 2.5
        
        scores[domain] = max(domain_score, 0.001)
        domain_details[domain] = {
            'terms_found': len(terms_found),
            'context_matches': context_matches,
            'raw_score': domain_score
        }
    
    total_score = sum(scores.values())
    if total_score > 0:
        probabilities = {domain: score / total_score for domain, score in scores.items()}
    else:
        probabilities = {domain: 0.25 for domain in medical_domains.keys()}
    
    if any(term in processed_text for term in ['neurobiología', 'sueño', 'cerebro', 'neurological']):
        if probabilities['Neurológico'] < 0.6:
            probabilities['Neurológico'] = 0.7
            remaining = 0.3
            other_domains = [d for d in probabilities.keys() if d != 'Neurológico']
            for domain in other_domains:
                probabilities[domain] = remaining / len(other_domains)
    
    max_prob = max(probabilities.values())
    threshold = max(0.15, max_prob * 0.3)
    predicted_labels = [domain for domain, prob in probabilities.items() if prob >= threshold]
    
    if not predicted_labels:
        predicted_labels = [max(probabilities.items(), key=lambda x: x[1])[0]]
    
    sorted_probs = sorted(probabilities.values(), reverse=True)
    confidence = sorted_probs[0]
    if len(sorted_probs) > 1:
        confidence = min(confidence, sorted_probs[0] - sorted_probs[1] + 0.5)
    
    processing_time = round(time.time() - start_time, 2)
    
    return {
        'scores': {k: round(v, 3) for k, v in probabilities.items()},
        'labels': predicted_labels,
        'confidence': round(confidence, 3),
        'processing_time': f'{processing_time}s',
        'terms_analysis': domain_details,
        'model_version': 'v2.1-batch-optimized'
    }

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Parse request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Check content type
            content_type = self.headers.get('Content-Type', '')
            
            if 'application/json' in content_type:
                # Handle JSON input
                data = json.loads(post_data.decode('utf-8'))
                articles = data.get('articles', [])
            elif 'text/csv' in content_type or 'multipart/form-data' in content_type:
                # Handle CSV input
                csv_content = post_data.decode('utf-8')
                articles = self.parse_csv(csv_content)
            else:
                self.send_error(400, "Unsupported content type. Use application/json or text/csv")
                return
            
            if not articles:
                self.send_error(400, "No articles provided")
                return
            
            # Process each article
            results = []
            for i, article in enumerate(articles):
                title = article.get('title', '')
                abstract = article.get('abstract', '')
                
                if not title and not abstract:
                    continue
                
                # Combine title and abstract
                text = f"{title} {abstract}".strip()
                
                # Classify the text
                classification = classify_medical_text(text)
                
                # Add to results
                result = {
                    'id': i + 1,
                    'title': title,
                    'abstract': abstract[:200] + '...' if len(abstract) > 200 else abstract,
                    'predicted_domains': classification['labels'],
                    'scores': classification['scores'],
                    'confidence': classification['confidence'],
                    'processing_time': classification['processing_time'],
                    'terms_analysis': classification['terms_analysis'],
                    'model_version': classification['model_version']
                }
                results.append(result)
            
            # Calculate batch statistics
            batch_stats = self.calculate_batch_stats(results)
            
            response = {
                'results': results,
                'batch_stats': batch_stats,
                'total_processed': len(results)
            }
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            self.wfile.write(json.dumps(response, indent=2).encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, f"Internal server error: {str(e)}")
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def parse_csv(self, csv_content):
        """Parse CSV content and extract articles"""
        articles = []
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        
        for row in csv_reader:
            article = {
                'title': row.get('title', ''),
                'abstract': row.get('abstract', ''),
                'group': row.get('group', '')  # Original group if available
            }
            articles.append(article)
        
        return articles
    
    def calculate_batch_stats(self, results):
        """Calculate statistics for the batch"""
        if not results:
            return {}
        
        # Count predictions by domain
        domain_counts = {'Cardiovascular': 0, 'Neurológico': 0, 'Hepatorrenal': 0, 'Oncológico': 0}
        total_confidence = 0
        
        for result in results:
            for domain in result['predicted_domains']:
                if domain in domain_counts:
                    domain_counts[domain] += 1
            total_confidence += result['confidence']
        
        avg_confidence = total_confidence / len(results) if results else 0
        
        return {
            'domain_distribution': domain_counts,
            'average_confidence': round(avg_confidence, 3),
            'processing_time': f"{sum(float(r['processing_time'].split('s')[0]) for r in results):.2f}s"
        }
