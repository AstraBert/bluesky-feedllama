import warnings
warnings.filterwarnings("ignore")

import accelerate

import torch
from transformers import pipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig  


model_name = "/root/.cache/huggingface/hub/models--Qwen--Qwen2.5-3B-Instruct/snapshots/aa8e72537993ba99e69dfaafa59ed015b17504d1/"
quantization_config = BitsAndBytesConfig(load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type= "nf4"
)

quantized_model = AutoModelForCausalLM.from_pretrained(model_name, device_map="cuda:0", torch_dtype=torch.bfloat16,quantization_config=quantization_config)
tokenizer = AutoTokenizer.from_pretrained(model_name)


pipe = pipeline(
    "text-generation", 
    model=quantized_model, 
    tokenizer=tokenizer,
    device_map="cuda:0"
)


def text_inference(chat_hist):
    prompt = chat_hist
    res = pipe(
        prompt,
        do_sample=False,
        temperature=0,
        top_p=1,
        max_new_tokens=512,
        repetition_penalty=1.8
    )
    ret = res[0]["generated_text"]
    return ret[-1]["content"]
