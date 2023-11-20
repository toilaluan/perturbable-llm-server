# LLM Server for Inconsistent Model Serving with vLLM
This server is based SOTA LLM-serving: https://vllm.readthedocs.io/en/latest/

## Initial Setup
1. **Installation of Requirements:** Execute `pip install -r requirements.txt` to install necessary packages.
2. **Launching the Server:** Run the command `python app.py` to start the server.

## API Integration and Usage
- **Accessing API Documentation:** Visit http://localhost:8000/docs for detailed API information.
- **Making an API Request:**
  Example of a request:
  ```
  curl -X 'POST' \
    'http://localhost:8000/generate' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "seeds": [0],
    "strengths": [1],
    "prompts": ["string", "hello"],
    "max_length": 128
  }'
  ```
- **Example of API Response:**
  The response includes details such as the ID, object type, creation timestamp, model used, and the choices array with text completions, log probabilities, and finish reasons. An example response is as follows:
  ```
  [
    {
      "id": "cmpl-786a475b60d548f6a058b96cc2344abc",
      "object": "text_completion",
      "created": 4617781,
      "model": "mistralai/Mistral-7B-Instruct-v0.1-seed-0-strength-1",
      "choices": [
        {
          "index": 0,
          "text": "Sample text completion here...",
          "logprobs": null,
          "finish_reason": "stop"
        }
      ],
      "usage": {
        "prompt_tokens": 2,
        "total_tokens": 66,
        "completion_tokens": 64
      }
    },
    // Additional responses...
  ]
  ```
