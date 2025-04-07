from os import listdir
from os.path import isfile, join

import whisper

mypath = "rawvideos/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

id = 1
model = whisper.load_model("turbo")

for file in onlyfiles:
	if(file[-3:] == "mp3"):
		
		result = model.transcribe(mypath + file)
		file = open("transcripts/" + str(id) + ".txt", "w")
		file.write(result["text"])
		file.close()

		id += 1
