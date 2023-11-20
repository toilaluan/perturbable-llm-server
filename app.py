from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yaml
from utils import model_processing, load_base_model
from vllm import SamplingParams
from vllm.entrypoints.openai.protocol import (
    CompletionResponse, CompletionResponseChoice, UsageInfo
)
from vllm.utils import random_uuid
import time

CONFIG = yaml.load(open("config.yaml"), yaml.FullLoader)

# Define the data model
class DataModel(BaseModel):
    seeds: List[int]
    strengths: List[int]
    prompts: List[str]
    max_length: int

# Create a FastAPI instance
app = FastAPI()

BASE_MODEL, TOKENIZER = load_base_model(CONFIG['base_model_name'])

# Define the POST endpoint
@app.post("/generate")
async def perturb_generation(data: DataModel):
    request_id = f"cmpl-{random_uuid()}"
    created_time = int(time.monotonic())
    model = model_processing(base_model = BASE_MODEL, tokenizer=TOKENIZER, seeds=data.seeds, strengths=data.strengths)
    prompts = data.prompts
    # change sampling_params if needed
    sampling_params = SamplingParams(temperature=0.8, top_p=0.95, max_tokens=data.max_length)
    batch_outputs = model.generate(prompts, sampling_params)
    responses = []
    for outputs in batch_outputs:
        choices = []
        for output in outputs.outputs:
            print(output)
            logprobs=None
            choice_data = CompletionResponseChoice(
                index=output.index,
                text=output.text,
                logprobs=logprobs,
                finish_reason=output.finish_reason,
            )
            choices.append(choice_data)

        num_prompt_tokens = len(outputs.prompt_token_ids)
        num_generated_tokens = sum(
            len(output.token_ids) for output in outputs.outputs)
        usage = UsageInfo(
            prompt_tokens=num_prompt_tokens,
            completion_tokens=num_generated_tokens,
            total_tokens=num_prompt_tokens + num_generated_tokens,
        )
        response = CompletionResponse(
            id=request_id,
            created=created_time,
            model=f"{CONFIG['base_model_name']}-seed-{'-'.join(map(str,data.seeds))}-strength-{'-'.join(map(str,data.strengths))}",
            choices=choices,
            usage=usage,
        )
        responses.append(response)
    return responses
# In the main block, you can run the app using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
