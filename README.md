# AI Test Case Generator

A Python tool that automatically generates pytest test cases for codebases using LLM (Large Language Model) assistance. This tool clones a repository, analyzes its Python files, and generates comprehensive test cases based on a feature description.

## Features

- Automatic repository cloning
- Codebase analysis
- LLM-powered test case generation
- Pytest integration
- Organized test output
- Comprehensive logging

## Prerequisites

- Python 3.10+
- Git

## Installation

1. Clone this repository
2. Install the required dependencies:

## Required Dependencies

- gitpython
- pytest
- requests
- pathlib


### Parameters

- `repo_url`: URL of the Git repository to analyze
- `feature_description`: Description of the feature for which tests should be generated
- `llm_url`: Endpoint URL of the LLM service

## How It Works

1. **Repository Cloning**: Clones the target repository to a temporary directory
2. **Code Analysis**: Analyzes all Python files in the repository
3. **Prompt Construction**: Creates a detailed prompt including the codebase and feature description
4. **Test Generation**: Sends the prompt to an LLM to generate comprehensive test cases
5. **Test Execution**: Writes and executes the generated tests using pytest

## Generated Tests

The tool generates test cases that include:
- Pytest fixtures
- Positive test cases
- Negative test cases
- Edge cases
- Detailed comments
- Proper assertions and error handling

## Output Format

Generated tests are saved in the `tests` directory of the cloned repository as `generated_test_cases.py`.

## Logging

The tool provides detailed logging information including:
- Repository cloning status
- File analysis progress
- Test generation and execution status
- Any errors or warnings

## Error Handling

The tool includes comprehensive error handling for:
- Repository cloning issues
- File reading errors
- LLM communication problems
- Test execution failures

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

# LLM Inference Server

A FastAPI-based server for running Large Language Model (LLM) inference using Modal for deployment. This implementation supports streaming responses and is configured to work with Hugging Face models.

## Features

- 🚀 Fast inference using GPU acceleration
- 🔄 Streaming responses support
- 🎯 Easy model switching
- 🔌 Built-in concurrency handling
- 🐳 Containerized deployment using Modal
- ⚡ Optimized for production use

## Supported Models

Currently configured to work with:
- Qwen/Qwen2.5-3B-Instruct (default)
- mistralai/Mistral-7B-v0.1
- stabilityai/stablelm-zephyr-3b

## Prerequisites

- Python 3.10+
- Modal account and CLI setup
- CUDA-compatible environment for local testing

## Installation

1. Clone the repository
2. Install dependencies:


## Configuration

Key configurations can be adjusted in `constants.py`:

- `BASE_MODEL`: Choose the Hugging Face model to use
- `KEEP_WARM`: Minimum number of warm containers
- `NUM_CONCURRENT_REQUESTS`: Concurrent requests per container
- `TIMEOUT`: Server timeout in seconds
- `GPU_COUNT`: Number of GPUs to utilize

## API Usage

The server exposes a POST endpoint for completions:


## Architecture

- `engine.py`: Core LLM inference engine
- `server.py`: FastAPI server implementation
- `constants.py`: Configuration constants
- `requirements.txt`: Project dependencies

## Performance

The server is configured to handle:
- Up to 10 concurrent requests per container
- Automatic scaling based on demand
- 600-second timeout per request
- GPU acceleration using NVIDIA A100 (40GB) for Qwen models or any available GPU for others


