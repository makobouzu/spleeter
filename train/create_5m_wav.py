# -*- coding: utf-8 -*-
# python create_5m_wav.py input_path tag(human, bird) max_volume(-30 - 30)
from pydub import AudioSegment
import os
import sys
import glob
from tqdm import tqdm

if __name__ == "__main__":
    args = sys.argv

    train_num = 0
    for i in range(100):
        if not os.path.isdir("train/train_" + str(train_num)):
            os.makedirs("train/train_" + str(train_num))
        train_num += 1
    
    num = 0
    max_num = 0
    buffer_num = 0
    folders = os.listdir("train")
    for fold in folders:
        if os.path.isfile("train/" + fold + "/" + args[2] + ".wav"):
            buffer_num = int(fold.split("_")[1])
            max_num = max(buffer_num, max_num)
    num = max_num + 1
    
    folder = glob.glob(args[1] + "/*.wav")
    sum_sound  = 0
    buffer_sum = 0
    for file_ in tqdm(folder):
        soundFile = AudioSegment.from_wav(file_)
        volume = float(args[3]) - float(soundFile.max_dBFS)
        soundFile = soundFile + volume
        if sum_sound == 0:
            sum_sound = soundFile
        else: 
            sum_sound += soundFile
            if sum_sound.duration_seconds >= 300:
                out_sound  = sum_sound[:300000]
                buffer_sum = sum_sound[300000:]
                out_sound.export("train/train_" + str(num) + "/" + args[2] + ".wav", format="wav")
                print("sum_sound: " + str(sum_sound.duration_seconds))
                print("buffer_sound: " + str(buffer_sum.duration_seconds))
                print("output " + "train_" + str(num) + "/" + args[2] + ".wav!!")
                sum_sound = sum_sound[300000:]
                num += 1
                if not os.path.isdir("train/train_" + str(num)):
                    os.makedirs("train/train_" + str(num))


    duration_num = int(sum_sound.duration_seconds // 300)
    print("duration_num: " + str(duration_num))
    if duration_num > 0:
        for i in tqdm(range(duration_num)):
            out_sound  = sum_sound[:300000]
            buffer_sum = sum_sound[300000:]
            out_sound.export("train/train_" + str(num) + "/" + args[2] + ".wav", format="wav")
            print("sum_sound: " + str(sum_sound.duration_seconds))
            print("buffer_sound: " + str(buffer_sum.duration_seconds))
            print("output " + "train_" + str(num) + "/" + args[2] + ".wav!!")
            sum_sound = sum_sound[300000:]
            num += 1
            if not os.path.isdir("train/train_" + str(num)):
                os.makedirs("train/train_" + str(num))

    if not isinstance(buffer_sum, int):
        if buffer_sum.duration_seconds > 0:
            buffer_sum.export("train/train_" + str(num) + "/" + args[2] + ".wav", format="wav")
            print("output " + "train_" + str(num) + "/" + args[2] + ".wav!!")
