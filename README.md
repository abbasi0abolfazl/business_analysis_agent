# Business Analysis Agent

  

A LangGraph-based agent designed to analyze sales data, calculate key metrics, and generate actionable recommendations for business optimization.


## Overview

The `business_analysis_agent` project is a Python application that uses the LangGraph library to create a workflow for processing sales data. It validates input data, calculates metrics (e.g., profit, sales change, customer acquisition cost), and generates recommendations based on these metrics. The project is designed for extensibility and can be integrated with APIs, databases, or machine learning models for enhanced functionality.

  

## Features

- **Input Validation**: Ensures input data contains required fields and valid values.

- **Metrics Calculation**: Computes key business metrics such as profit, sales change, and customer acquisition cost (CAC).

- **Recommendation Engine**: Generates actionable business recommendations based on calculated metrics.

- **Testing**: Comprehensive unit tests using `pytest` to ensure reliability.

- **Extensibility**: Modular design to support additional features like multi-language support, database integration, and API endpoints.

  

## Requirements

- Python 3.11

- Virtual environment (recommended)

- `uv` for dependency management (optional but recommended)

## Installation

1. **Clone the Repository**:

```bash

git clone https://github.com/abbasi0abolfazl/business_analysis_agent.git

cd business_analysis_agent

```

  

2. **Create and Activate a Virtual Environment**:

```bash

python3 -m venv .venv

source .venv/bin/activate

```

  

3. **Install Dependencies**:

Using `uv` (recommended):

```bash

uv pip install -r requirements.txt

```

Or with `pip`:

```bash

pip install -r requirements.txt

```

  

4. **Set Up Environment Variables** (if needed):

- Create a `.env` file in the project root if specified in `langgraph.json`:

```plaintext

# .env

# Example: LANGCHAIN_API_KEY=your_api_key

```

  

## Usage

### Running the Agent

To run the agent with sample input data:

```bash
python3 main.py
```

  

### Running the Development Server

To start the LangGraph development server:

```bash

langgraph dev

```

This will start an in-memory server at `http://127.0.0.1:2024`, providing:

- API endpoint: `http://127.0.0.1:2024/run-agent`

- Studio UI: `https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024`

- API Docs: `http://127.0.0.1:2024/docs`

### Running Tests

To run the unit tests:

```bash

pytest test_agent.py -v

```

  

## Directory Structure

```

statement_lang/

├── agent.py # Core agent logic 


├── test_agent.py # Unit tests for the agent

├── requirements.txt # Project dependencies

├── langgraph.json # LangGraph configuration

├── .env # Environment variables (optional)

├── pyproject.toml # Project metadata and uv configuration (optional)

├── README.md # This file

```

  

## Future Development

See the [development plan](development_plan.md) for details.


