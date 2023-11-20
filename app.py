from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
import yaml
from pydantic.fields import Field
from utils import model_processing, load_base_model
from vllm import SamplingParams
from vllm.entrypoints.openai.protocol import CompletionResponseChoice, UsageInfo
from vllm.utils import random_uuid
import time

CONFIG = yaml.load(open("config.yaml"), yaml.FullLoader)


class CompletionResponse(BaseModel):
    id: str = Field(default_factory=lambda: f"cmpl-{random_uuid()}")
    object: str = "text_completion"
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str
    choices: List[CompletionResponseChoice]
    usage: UsageInfo
    seeds: List[int]
    strengths: List[float]
    prompts: List[str]


# Define the data model
class DataModel(BaseModel):
    seeds: List[int]
    strengths: List[float]
    prompts: List[str]
    max_length: int
    temperature: float
    top_p: float


# Create a FastAPI instance
app = FastAPI()

BASE_MODEL, TOKENIZER = load_base_model(CONFIG["base_model_name"])


@app.post("/generate")
async def perturb_generation(data: DataModel):
    request_id = f"cmpl-{random_uuid()}"
    created_time = int(time.monotonic())
    model = model_processing(
        base_model=BASE_MODEL,
        tokenizer=TOKENIZER,
        seeds=data.seeds,
        strengths=data.strengths,
    )
    prompts = data.prompts
    sampling_params = SamplingParams(
        temperature=data.temperature, top_p=data.top_p, max_tokens=data.max_length
    )
    batch_outputs = model.generate(prompts, sampling_params)
    responses = []
    for outputs in batch_outputs:
        choices = []
        for output in outputs.outputs:
            choice_data = CompletionResponseChoice(
                index=output.index,
                text=output.text,
                finish_reason=output.finish_reason,
            )
            choices.append(choice_data)

        num_prompt_tokens = len(outputs.prompt_token_ids)
        num_generated_tokens = sum(len(output.token_ids) for output in outputs.outputs)
        usage = UsageInfo(
            prompt_tokens=num_prompt_tokens,
            completion_tokens=num_generated_tokens,
            total_tokens=num_prompt_tokens + num_generated_tokens,
        )
        response = CompletionResponse(
            id=request_id,
            created=created_time,
            model=CONFIG["base_model_name"],
            choices=choices,
            usage=usage,
            seeds=data.seeds,
            strengths=data.strengths,
            prompts=data.prompts,
        )
        responses.append(response)
    return responses


# In the main block, you can run the app using Uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
