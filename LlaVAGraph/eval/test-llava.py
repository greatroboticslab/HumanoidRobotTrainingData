# Load model directly
from transformers import AutoProcessor, AutoModelForCausalLM

model_path= "/projects/imo2d/llava-v1.6-vicuna-7b"  # Example: "liuhaotian/LLaVA-13b-delta"
processor = AutoProcessor.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

