# 🤖 Databricks Agent Bricks Tester

A modern Streamlit application for testing and interacting with Databricks Agent Bricks agents. This tool allows you to quickly test multiple agents with a clean, intuitive interface while keeping all your credentials secure and local.

## Features

- 🔐 **Secure**: All tokens and endpoints stored locally, never leave your machine
- 🎯 **Multi-Agent Support**: Manage and test multiple agents from one interface
- 🚀 **Quick Testing**: Send messages and get responses instantly
- 📊 **Usage Tracking**: View token usage and response metadata

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up Environment** (Optional)
   ```bash
   cp env.example .env
   # Edit .env with your Databricks token
   ```

3. **Run the App**
   ```bash
   streamlit run app.py
   ```

4. **Add Your First Agent**
   - Use the sidebar to add a new agent
   - Enter the agent name, endpoint URL, and model name
   - Your agents are automatically saved to `agents_config.yaml`

5. **Test Your Agent**
   - Select an agent from the dropdown
   - Enter your Databricks token
   - Send messages and see responses in real-time

## Usage

### Adding Agents

When you create an agent in Databricks, you'll get code like this:

```python
from openai import OpenAI
import os

DATABRICKS_TOKEN = os.environ.get('DATABRICKS_TOKEN')
client = OpenAI(
    api_key=DATABRICKS_TOKEN,
    base_url="https://dbc-16536299-9096.cloud.databricks.com/serving-endpoints"
)

response = client.chat.completions.create(
    model="t2t-0ce27e40-endpoint",
    messages=[{"role": "user", "content": "What is an LLM agent?"}]
)
```

To add this agent to the tester:
1. **Agent Name**: `My Agent` (or any descriptive name)
2. **Endpoint URL**: `https://dbc-16536299-9096.cloud.databricks.com/serving-endpoints`
3. **Model Name**: `t2t-0ce27e40-endpoint`

### Security

- All data is stored locally in `agents_config.yaml`
- Tokens are only used for API calls and never stored
- No data is sent to external services except your Databricks endpoints

### Configuration

The app automatically creates an `agents_config.yaml` file to store your agent configurations. This file contains:

```yaml
My Agent:
  endpoint: https://dbc-xxxxx.cloud.databricks.com/serving-endpoints
  model: t2t-xxxxx-endpoint
  created_at: '2024-01-01T12:00:00'
```

## Requirements

- Python 3.7+
- Streamlit
- OpenAI Python client
- PyYAML
- python-dotenv

## Getting Your Databricks Token

1. Go to [Databricks Personal Access Tokens](https://docs.databricks.com/en/dev-tools/auth/pat.html)
2. Generate a new token
3. Copy the token and paste it into the app when testing

## Troubleshooting

- **Token Issues**: Make sure your Databricks token has the necessary permissions
- **Endpoint Errors**: Verify the endpoint URL is correct and accessible
- **Model Errors**: Ensure the model name matches exactly what's configured in Databricks
