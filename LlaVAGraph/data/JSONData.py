#!/usr/bin/env python
# coding: utf-8

# # LLaVA Dataset Generation

# In[1]:


import json
import random
import os


# ## Setup the Paths

# In[2]:


uniqueId = 1


# In[3]:


RANDOM_CONTINUOUS = "textData/random/random-continuous.txt"
SINE_CONTINUOUS = "textData/sine/sine-continuous.txt"
SQUARE_CONTINUOUS = "textData/square/square-continuous.txt"

RANDOM_RANDOMNESS = "textData/random/random-randomness.txt"
SINE_RANDOMNESS = "textData/sine/sine-randomness.txt"
SQUARE_RANDOMNESS = "textData/square/square-randomness.txt"

RANDOM_SQUARE = "textData/random/random-square.txt"
SINE_SQUARE = "textData/sine/sine-square.txt"
SQUARE_SQUARE = "textData/square/square-square.txt"
# In[4]:


data = []


# ## Random Noise

# In[5]:


with open(RANDOM_CONTINUOUS, "r") as file:
    randomContinuous = file.read().splitlines()
with open(RANDOM_RANDOMNESS, "r") as file:
    randomRandomness = file.read().splitlines()
with open(RANDOM_SQUARE, "r") as file:
    randomSquare = file.read().splitlines()

# In[6]:

maxImage = len(os.listdir("subset/trainData/NoiseData"))
for file in os.listdir("subset/trainData/NoiseData"):
    json_data = {
        "id": uniqueId,
        "image": f"subset/trainData/NoiseData/{file}",
        "conversations": [
            {
                "from": "human",
                "value": "<image>Is the line shown in the graph continuous? Describe the line."
            },
            {
                "from": "gpt",
                "value": f"{random.choice(randomContinuous)}"
            },
            {
                "from": "human",
                "value": "Does the graph contain any random points?"
            },
            {
                "from": "gpt",
                "value": f"{random.choice(randomRandomness)}"
            },
            {
                "from": "human",
                "value": "Does the graph contain sharp corners?"
            },
            {
                "from": "gpt",
                "value": f"{random.choice(randomSquare)}"
            },
             
        ]
    }
    data.append(json_data)
    uniqueId += 1


# ## Sine Wave

# In[7]:


with open(SINE_CONTINUOUS, "r") as file:
    sineContinuous = file.read().splitlines()
with open(SINE_RANDOMNESS, "r") as file:
    sineRandomness = file.read().splitlines()
with open(SINE_SQUARE, "r") as file:
    sineSquare = file.read().splitlines()


# In[8]:
sineImages = os.listdir("subset/trainData/SineData")
random.shuffle(sineImages)
sineImages = sineImages[:maxImage]
for file in sineImages:
    json_data = {
        "id": uniqueId,
        "image": f"subset/trainData/SineData/{file}",
        "conversations": [
            {
                "from": "human",
                "value": "<image>Is the line shown in the graph continuous? Describe the line."
            },
            {
                "from": "gpt",
                "value": f"{random.choice(sineContinuous)}"
            },
            {
                "from": "human",
                "value": "Does the graph contain any random points?"
            },
            {
                "from": "gpt",
                "value": f"{random.choice(sineRandomness)}"
            },
            {
                "from": "human",
                "value": "Does the graph contain sharp corners?"
            },
            {
                "from": "gpt",
                "value": f"{random.choice(sineSquare)}"
            },
             
        ]
    }
    data.append(json_data)
    uniqueId += 1


# ## Square Wave

# In[9]:


with open(SQUARE_CONTINUOUS, "r") as file:
    squareContinuous = file.read().splitlines()
with open(SQUARE_RANDOMNESS, "r") as file:
    squareRandomness = file.read().splitlines()
with open(SQUARE_SQUARE, "r") as file:
    squareSquare = file.read().splitlines()

# In[10]:


squareImages = os.listdir("subset/trainData/SquareData")
random.shuffle(squareImages)
squareImages = squareImages[:maxImage]
for file in squareImages:
    json_data = {
        "id": uniqueId,
        "image": f"subset/trainData/SquareData/{file}",
        "conversations": [
            {
                "from": "human",
                "value": "<image>Is the line shown in the graph continuous? Describe the line."
            },
            {
                "from": "gpt",
                "value": f"{random.choice(squareContinuous)}"
            },
            {
                "from": "human",
                "value": "Does the graph contain any random points?"
            },
            {
                "from": "gpt",
                "value": f"{random.choice(squareRandomness)}"
            },
            {
                "from": "human",
                "value": "Does the graph contain sharp corners?"
            },
            {
                "from": "gpt",
                "value": f"{random.choice(squareSquare)}"
            } 
        ]
    }
    data.append(json_data)
    uniqueId += 1


# ## Output

# In[11]:

random.shuffle(data)

with open("fullData.json", "w") as outputFile:
    json.dump(data, outputFile, indent=2)


# In[ ]:




