import os
import tempfile
import git
from pathlib import Path
import ast
import logging
from typing import List, Dict, Optional
import pytest
import json
import requests
import pprint

class TestCaseGenerator:
    def __init__(self, repo_url: str, feature_description: str, llm_url: str):
        self.repo_url = repo_url
        self.feature_description = feature_description
        self.llm_url = llm_url
        self.temp_dir = None
        self.logger = logging.getLogger(__name__)
        
    def setup_logging(self):
        """Configure logging settings"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def clone_repository(self) -> Path:
        """Clone the repository to a temporary directory"""
        self.temp_dir = tempfile.mkdtemp()
        self.logger.info(f"Cloning repository to {self.temp_dir}")
        git.Repo.clone_from(self.repo_url, self.temp_dir)
        return Path(self.temp_dir)

    def analyze_codebase(self, repo_path: Path) -> List[Dict]:
        """
        Analyze all Python files in the repository
        Returns a list of dictionaries containing file paths and their content
        """
        all_files = []
        
        for file_path in repo_path.rglob("*.py"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    all_files.append({
                        'path': str(file_path.relative_to(repo_path)),
                        'content': content
                    })
            except Exception as e:
                self.logger.warning(f"Error reading file {file_path}: {str(e)}")
                
        return all_files

    def construct_prompt(self, all_files: List[Dict]) -> str:
        """Construct the prompt for the LLM with all codebase files"""
        prompt = f"""
You are an expert Python developer specializing in test-driven development (TDD).
Generate Python test cases using pytest for the following feature:

Feature Description:
{self.feature_description}

Complete Codebase:
"""
        
        # Group files by directory for better organization
        files_by_dir = {}
        for file in all_files:
            dir_name = str(Path(file['path']).parent)
            if dir_name not in files_by_dir:
                files_by_dir[dir_name] = []
            files_by_dir[dir_name].append(file)
        
        # Add files to prompt, organized by directory
        for dir_name, files in files_by_dir.items():
            prompt += f"\n📁 Directory: {dir_name}\n"
            for file in files:
                prompt += f"\n📄 File: {file['path']}\n```python\n{file['content']}\n```\n"
            
        prompt += """
Please generate comprehensive test cases that:
1. Use pytest fixtures where appropriate
2. Include positive test cases, negative test cases, and edge cases
3. Include clear comments explaining each test's purpose
4. Follow Python testing best practices
5. Include proper assertions and error handling

Return the response in the following JSON format:
{
    "test_file_name": "test_feature_name.py",
    "test_code": "... the complete test code ..."
}
"""
        return prompt

    def generate_tests_with_llm(self, prompt: str) -> Dict:
        """Make POST request to LLM endpoint and get the generated tests"""
        try:
            payload = {
                "messages": [
                    {"role": "system", "content": "You are a Python testing expert."},
                    {"role": "user", "content": prompt}
                ]
            }
            
            response = requests.post(self.llm_url, json=payload)
            response.raise_for_status()
            
            # Parse the JSON response
            
            content = response.json()
            return content['response']
            
        except Exception as e:
            self.logger.error(f"Error generating tests: {str(e)}")
            raise

    def write_test_file(self, repo_path: Path, test_data: str) -> Path:
        """Write the generated tests to a file"""
        tests_dir = repo_path / 'tests'
        tests_dir.mkdir(exist_ok=True)
        
        test_file_path = tests_dir / 'generated_test_cases.py'
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write(test_data)
            
        return test_file_path

    def run_tests(self, test_file_path: Path):
        """Run the generated tests"""
        self.logger.info(f"Running tests from {test_file_path}")
        pytest.main([str(test_file_path), "-v"])

    def generate_and_run_tests(self):
        """Main method to orchestrate the test generation process"""
        try:
            self.setup_logging()
            repo_path = self.clone_repository()
            all_files = self.analyze_codebase(repo_path)
            
            if not all_files:
                self.logger.warning("No files found for analysis")
                return
            
            prompt = self.construct_prompt(all_files)
            test_data = self.generate_tests_with_llm(prompt)
            pprint.pprint(test_data)
            test_file_path = self.write_test_file(repo_path, test_data)
            self.run_tests(test_file_path)
            
        except Exception as e:
            self.logger.error(f"Error in test generation process: {str(e)}")
            raise
        finally:
            if self.temp_dir:
                self.logger.info(f"Generated tests can be found in {self.temp_dir}")

def main():
    # Example usage
    repo_url = "https://github.com/ChidambaramG/demand_forecasting_XGBoost"
    feature_description = """
    Modify the approach to include rolling means as on of the features when training the model.
    """
    llm_url = "https://chidambaramg5--completion-dev.modal.run"
    
    generator = TestCaseGenerator(repo_url, feature_description, llm_url)
    generator.generate_and_run_tests()

if __name__ == "__main__":
    main()