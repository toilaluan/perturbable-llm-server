import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import os
import shutil
from vllm import LLM, SamplingParams
from copy import deepcopy
from tqdm import tqdm
from vllm.model_executor.parallel_utils.parallel_state import destroy_model_parallel

def load_base_model(model_name):
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return model, tokenizer

def perturb_weights(model, seed, noise_scale=2e-4):
    """Add small random noise to the model weights."""
    print("Start perturbing")
    torch.manual_seed(seed)
    for param in tqdm(model.parameters()):
        noise = torch.randn_like(param) * noise_scale
        param.data.add_(noise)
    print("Perturb successfully")
    return model

def apply_changes_to_original_model(base_model, seeds, strengths):
    model = deepcopy(base_model)
    model.eval()
    for i, seed in enumerate(seeds):
      model = perturb_weights(model, seed, noise_scale=strengths[i] * 1e-4)
    return model

def model_processing(base_model, tokenizer, seeds, strengths, save_dir='/tmp/perturbed_model', tensor_parallel_size=1, gpu_memory_utilization=0.95):
    shutil.rmtree(save_dir, ignore_errors=True)
    os.makedirs(save_dir, exist_ok=True)
    perturbed_model = apply_changes_to_original_model(base_model, seeds, strengths)
    perturbed_model.save_pretrained(save_dir)
    del perturbed_model
    tokenizer.save_pretrained(save_dir)
    destroy_model_parallel()
    vllm_model = LLM(save_dir, tensor_parallel_size=tensor_parallel_size, gpu_memory_utilization=gpu_memory_utilization)
    return vllm_model