# langChain-qai

This package contains the LangChain integrations with QAI.

## Setup

Create an API Key on [QAI](https://qai.qaip.com/dashboard/apikeys).

We can then set API key as environment variables.

```python
import os

os.environ["QAI_API_KEY"] = "<YOUR_API_KEY>"
```

## Installation

```bash
pip install langchain-qai
```

## Retrievers
`QAIRetriever` class provides a retriever to connect with QAI Search API.

```python
from langchain_qai import QAIRetriever

retriever = QAIRetriever()

retriever.ivoke("What is the meaning of life?")
```
