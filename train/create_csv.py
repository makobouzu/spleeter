# -*- coding: utf-8 -*-
# python create_csv.py input_folder output_name

import sys
import os
from tqdm import tqdm
from pydub import AudioSegment
import csv

if __name__ == "__main__":
    args = sys.argv
    header = ["mix_path", "human_path", "bird_path", "car_path", "duration"]
    output = []
    folder_list = os.listdir(args[1])
    if folder_list[0] == ".DS_Store":
        os.remove(args[1] + "/.DS_Store")
        folder_list.pop(0)
    
    for folder in tqdm(folder_list):
        cell = []
        mix = args[1] + "/" + folder + "/" + "mixture.wav"
        human = args[1] + "/" + folder + "/" + "human.wav"
        bird = args[1] + "/" + folder + "/" + "bird.wav"
        car = args[1] + "/" + folder + "/" + "car.wav"
        duration = AudioSegment.from_wav(mix).duration_seconds

        cell.append(mix)
        cell.append(human)
        cell.append(bird)
        cell.append(car)
        cell.append(duration)
        output.append(cell)
        
    output.insert(0, header)
    print(output)
                

    with open(args[2], 'w') as f:
        writer = csv.writer(f)
        for row in output:
            writer.writerow(row)