# -*- coding: utf-8 -*-
#python create_mixture.py train human_vol(-10) bird_vol(-5) car_vol(-15)
from pydub import AudioSegment
import os
import sys
from tqdm import tqdm

if __name__ == "__main__":
    args = sys.argv
    folders = os.listdir(args[1])
    if folders[0] == ".DS_Store":
        os.remove(args[1] + "/.DS_Store")
        folders.pop(0)
    

    for folder in tqdm(folders):
        if os.path.isfile(args[1] + "/" + folder + "/human.wav") and os.path.isfile(args[1] + "/" + folder + "/bird.wav") and os.path.isfile(args[1] + "/" + folder + "/car.wav"):
            human = AudioSegment.from_wav(args[1] + "/" + folder + "/human.wav")
            bird  = AudioSegment.from_wav(args[1] + "/" + folder + "/bird.wav")
            car   = AudioSegment.from_wav(args[1] + "/" + folder + "/car.wav")

            human_volume = float(args[2]) - float(human.max_dBFS)
            bird_volume = float(args[3]) - float(bird.max_dBFS)
            car_volume = float(args[4]) - float(car.max_dBFS)

            human = human + human_volume
            bird  = bird  + bird_volume
            car   = car   + car_volume
            human.export(args[1] + "/" + folder + "/human.wav", format="wav")
            bird.export(args[1] + "/" + folder + "/bird.wav", format="wav")
            car.export(args[1] + "/" + folder + "/car.wav", format="wav")

            mixture = human.overlay(bird, position=0)
            mixture = mixture.overlay(car, position=0)
            mixture = mixture[:300000]
            mixture.export(args[1] + "/" + folder + "/mixture.wav", format="wav")