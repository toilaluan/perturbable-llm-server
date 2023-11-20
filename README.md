# LLM Server for inconsistent model purpose

## Getting started
1. Install requirements: `pip install -r requirements.txt`
2. Start server: `python app.py`

## API Usage
- View API documents at http://localhost:8000/docs
- Example request:
```
curl -X 'POST' \
  'http://localhost:8000/generate' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "seeds": [
    0
  ],
  "strengths": [
    1
  ],
  "prompts": [
    "string", "hello"
  ],
  "max_length": 128
}'
```
Example response
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
        "text": "[] arr = {\"apple\", \"banana\", \"cherry\", \"date\", \"fig\", \"grape\"};\n\nRandom rand = new Random();\n\nint choice = rand.Next(arr.Length);\n\nConsole.WriteLine(arr[choice]);\n\nConsole.ReadLine();",
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
  {
    "id": "cmpl-786a475b60d548f6a058b96cc2344abc",
    "object": "text_completion",
    "created": 4617781,
    "model": "mistralai/Mistral-7B-Instruct-v0.1-seed-0-strength-1",
    "choices": [
      {
        "index": 0,
        "text": " there\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n",
        "logprobs": null,
        "finish_reason": "length"
      }
    ],
    "usage": {
      "prompt_tokens": 3,
      "total_tokens": 131,
      "completion_tokens": 128
    }
  }
]
```
