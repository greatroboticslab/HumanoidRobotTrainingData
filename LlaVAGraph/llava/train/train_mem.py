from llava.train import train
if __name__ == "__main__":
    train.train(attn_implementation="flash_attention_2")
