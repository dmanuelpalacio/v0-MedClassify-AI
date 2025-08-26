import pandas as pd
import os
import tempfile
import pytest
from pathlib import Path
import sys

# Add parent directory to path to import evaluate_and_predict
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_csv_format_validation():
    """Test that script validates required CSV columns"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        # CSV without required columns
        f.write("wrong_col1,wrong_col2\nvalue1,value2\n")
        f.flush()
        
        # Import and test
        from evaluate_and_predict import main
        import argparse
        
        args = argparse.Namespace(
            input=f.name,
            model="dummy_model.joblib",
            out_dir="test_output"
        )
        
        # Should exit with error code 1
        with pytest.raises(SystemExit) as exc_info:
            main(args)
        assert exc_info.value.code == 1
        
        os.unlink(f.name)

def test_pipeline_with_valid_csv():
    """Test pipeline runs with valid CSV format"""
    # Create test CSV with required columns
    test_data = pd.DataFrame({
        'title': [
            'Efficacy of ACE inhibitors in cardiovascular disease',
            'Neurological effects of sleep deprivation',
            'Hepatic fibrosis progression markers'
        ],
        'abstract': [
            'This study evaluates the effectiveness of ACE inhibitors in reducing cardiovascular mortality in patients with heart failure.',
            'Research on the impact of sleep deprivation on cognitive function and neurological health in young adults.',
            'Analysis of biomarkers for hepatic fibrosis progression in patients with chronic liver disease.'
        ],
        'group': ['Cardiovascular', 'Neurológico', 'Hepatorrenal']
    })
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save test CSV
        input_csv = Path(temp_dir) / "test_input.csv"
        test_data.to_csv(input_csv, index=False)
        
        # Create dummy model file (joblib format simulation)
        model_path = Path(temp_dir) / "test_model.joblib"
        
        # Create a simple mock model for testing
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import Pipeline
        import joblib
        
        # Train a simple model on the test data
        X = test_data['title'] + '. ' + test_data['abstract']
        y = test_data['group']
        
        model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=100)),
            ('clf', LogisticRegression(random_state=42))
        ])
        model.fit(X, y)
        joblib.dump(model, model_path)
        
        # Test the evaluation script
        from evaluate_and_predict import main
        import argparse
        
        output_dir = Path(temp_dir) / "outputs"
        args = argparse.Namespace(
            input=str(input_csv),
            model=str(model_path),
            out_dir=str(output_dir)
        )
        
        # Run the script
        result = main(args)
        assert result == 0  # Should exit successfully
        
        # Check outputs exist
        assert (output_dir / "predictions.csv").exists()
        assert (output_dir / "metrics.json").exists()
        assert (output_dir / "confusion_matrix.png").exists()
        
        # Check predictions CSV has group_predicted column
        predictions = pd.read_csv(output_dir / "predictions.csv")
        assert 'group_predicted' in predictions.columns
        assert len(predictions) == len(test_data)
        
        # Check metrics JSON has required metrics
        import json
        with open(output_dir / "metrics.json") as f:
            metrics = json.load(f)
        
        required_metrics = ['f1_weighted', 'hamming_loss', 'exact_match']
        for metric in required_metrics:
            assert metric in metrics
            assert isinstance(metrics[metric], (int, float))

def test_model_loading_error():
    """Test script handles model loading errors gracefully"""
    test_data = pd.DataFrame({
        'title': ['Test title'],
        'abstract': ['Test abstract'],
        'group': ['Test group']
    })
    
    with tempfile.TemporaryDirectory() as temp_dir:
        input_csv = Path(temp_dir) / "test_input.csv"
        test_data.to_csv(input_csv, index=False)
        
        from evaluate_and_predict import main
        import argparse
        
        args = argparse.Namespace(
            input=str(input_csv),
            model="nonexistent_model.joblib",
            out_dir=str(Path(temp_dir) / "outputs")
        )
        
        # Should exit with error code 1
        with pytest.raises(SystemExit) as exc_info:
            main(args)
        assert exc_info.value.code == 1

if __name__ == "__main__":
    pytest.main([__file__])
