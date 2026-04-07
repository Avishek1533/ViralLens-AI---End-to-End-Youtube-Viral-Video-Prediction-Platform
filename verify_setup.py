"""
ViralLens AI - Setup Verification Script
Checks if all required files and dependencies are in place
"""

import os
import sys
from pathlib import Path

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(text):
    print(f"\n{BOLD}{BLUE}{'='*80}{RESET}")
    print(f"{BOLD}{BLUE}{text.center(80)}{RESET}")
    print(f"{BOLD}{BLUE}{'='*80}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text):
    print(f"{RED}✗ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠ {text}{RESET}")

def print_info(text):
    print(f"{BLUE}ℹ {text}{RESET}")

def check_files():
    """Check if all required files exist"""
    print_header("Checking Required Files")
    
    required_files = {
        'Application': ['main.py'],
        'Models': [
            'logistic_regression_pipeline.joblib',
            'random_forest_pipeline.joblib',
            'xgboost_pipeline.joblib',
            'viral_prediction_dnn.joblib'
        ],
        'Documentation': ['README.md', 'API_GUIDE.md', 'QUICKSTART.md', 'CURL_EXAMPLES.md'],
        'Scripts': ['run_server.bat', 'run_server.sh', 'example_usage.py', 'requirements.txt'],
        'Docker': ['Dockerfile', 'docker-compose.yml'],
    }
    
    all_ok = True
    for category, files in required_files.items():
        print(f"{BOLD}{category}:{RESET}")
        for file in files:
            if os.path.exists(file):
                print_success(file)
            else:
                print_error(file + " (MISSING)")
                all_ok = False
        print()
    
    return all_ok

def check_dependencies():
    """Check if Python dependencies are installed"""
    print_header("Checking Python Dependencies")
    
    required_packages = {
        'fastapi': 'FastAPI framework',
        'uvicorn': 'ASGI server',
        'pydantic': 'Data validation',
        'numpy': 'Numerical computing',
        'pandas': 'Data processing',
        'scikit-learn': 'Machine learning',
        'xgboost': 'XGBoost model',
        'joblib': 'Model serialization',
        'vaderSentiment': 'Sentiment analysis',
    }
    
    all_ok = True
    for package, description in required_packages.items():
        try:
            __import__(package)
            print_success(f"{package:20} - {description}")
        except ImportError:
            print_error(f"{package:20} - {description} (NOT INSTALLED)")
            all_ok = False
    
    print()
    if not all_ok:
        print_warning("Some dependencies missing!")
        print(f"Run: {BOLD}pip install -r requirements.txt{RESET}\n")
    
    return all_ok

def check_models():
    """Check if models are accessible"""
    print_header("Checking Model Files")
    
    models = {
        'logistic_regression_pipeline.joblib': 'Logistic Regression',
        'random_forest_pipeline.joblib': 'Random Forest',
        'xgboost_pipeline.joblib': 'XGBoost',
        'viral_prediction_dnn.joblib': 'Deep Neural Network',
    }
    
    all_ok = True
    total_size = 0
    
    for model_file, model_name in models.items():
        if os.path.exists(model_file):
            size_mb = os.path.getsize(model_file) / (1024 * 1024)
            total_size += size_mb
            print_success(f"{model_name:25} - {size_mb:.1f} MB")
        else:
            print_error(f"{model_name:25} - NOT FOUND")
            all_ok = False
    
    print(f"\nTotal model size: {total_size:.1f} MB")
    print()
    return all_ok

def check_documentation():
    """Check if documentation files exist and have content"""
    print_header("Checking Documentation")
    
    docs = {
        'README.md': 'Project overview',
        'API_GUIDE.md': 'API documentation',
        'QUICKSTART.md': 'Getting started guide',
        'CURL_EXAMPLES.md': 'cURL examples',
        'SETUP_COMPLETE.txt': 'Setup summary',
    }
    
    all_ok = True
    for doc_file, description in docs.items():
        if os.path.exists(doc_file):
            size = os.path.getsize(doc_file)
            if size > 0:
                print_success(f"{doc_file:25} - {description}")
            else:
                print_warning(f"{doc_file:25} - Empty file!")
                all_ok = False
        else:
            print_error(f"{doc_file:25} - MISSING")
            all_ok = False
    
    print()
    return all_ok

def check_permissions():
    """Check if scripts have execute permissions"""
    print_header("Checking Script Permissions")
    
    scripts = ['run_server.sh', 'run_examples.sh']
    
    all_ok = True
    for script in scripts:
        if os.path.exists(script):
            if os.access(script, os.X_OK):
                print_success(f"{script} - executable")
            else:
                print_warning(f"{script} - not executable (fixing...)")
                try:
                    os.chmod(script, 0o755)
                    print_success(f"{script} - fixed")
                except:
                    print_error(f"{script} - could not fix permissions")
                    all_ok = False
        else:
            print_info(f"{script} - not found")
    
    print()
    return all_ok

def check_project_structure():
    """Verify project structure"""
    print_header("Project Structure")
    
    base_dir = Path('.')
    
    # Count files by type
    py_files = list(base_dir.glob('*.py'))
    model_files = list(base_dir.glob('*.joblib'))
    doc_files = list(base_dir.glob('*.md'))
    script_files = list(base_dir.glob('*.sh')) + list(base_dir.glob('*.bat'))
    
    print(f"Python files:  {len(py_files)}")
    print(f"Model files:   {len(model_files)}")
    print(f"Documentation: {len(doc_files)}")
    print(f"Scripts:       {len(script_files)}")
    
    print(f"\nTotal size: {sum(os.path.getsize(f) for f in base_dir.glob('*.*')) / (1024*1024):.1f} MB")
    print()

def print_summary(results):
    """Print summary of checks"""
    print_header("Summary")
    
    checks = {
        'Project Files': results[0],
        'Dependencies': results[1],
        'Model Files': results[2],
        'Documentation': results[3],
        'Permissions': results[4],
    }
    
    all_passed = all(results)
    
    for check_name, result in checks.items():
        if result:
            print_success(f"{check_name} - OK")
        else:
            print_error(f"{check_name} - Issues found")
    
    print()
    
    if all_passed:
        print(f"{GREEN}{BOLD}")
        print("╔" + "═"*78 + "╗")
        print("║" + " "*78 + "║")
        print("║" + "  🎉 All checks passed! Your ViralLens AI API is ready to use!".ljust(78) + "║")
        print("║" + " "*78 + "║")
        print("╚" + "═"*78 + "╝")
        print(f"{RESET}")
        
        print("\nNext steps:")
        print(f"  1. Start the server:")
        print(f"     {BOLD}Windows: run_server.bat{RESET}")
        print(f"     {BOLD}Linux/Mac: bash run_server.sh{RESET}")
        print(f"  2. Visit: {BOLD}http://localhost:8000/docs{RESET}")
        print(f"  3. Make your first prediction!")
        print()
    else:
        print(f"{RED}{BOLD}")
        print("⚠ Some issues were found. Please fix them before using the API.")
        print(f"{RESET}")
        print("\nCommon fixes:")
        print(f"  • Install dependencies: {BOLD}pip install -r requirements.txt{RESET}")
        print(f"  • Verify model files are in this directory")
        print(f"  • Check file permissions on Linux/Mac")
        print()
    
    return all_passed

def main():
    print(f"\n{BOLD}{BLUE}")
    print("╔" + "═"*78 + "╗")
    print("║" + "  ViralLens AI - Setup Verification".center(78) + "║")
    print("╚" + "═"*78 + "╝")
    print(f"{RESET}")
    
    # Run all checks
    files_ok = check_files()
    deps_ok = check_dependencies()
    models_ok = check_models()
    docs_ok = check_documentation()
    perms_ok = check_permissions()
    
    check_project_structure()
    
    # Print summary
    all_ok = print_summary([files_ok, deps_ok, models_ok, docs_ok, perms_ok])
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
