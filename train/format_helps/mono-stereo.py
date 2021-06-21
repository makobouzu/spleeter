# -*- coding: utf-8 -*-
from pydub import AudioSegment
import sys
import glob
from tqdm import tqdm

if __name__ == "__main__":
   args = sys.argv
   folder = glob.glob(args[1] + "/*.wav")
   for file_ in tqdm(folder):
       sound = AudioSegment.from_file(file_)
       if sound.channels == 1:
           sound = sound.set_channels(2)
           sound.export(file_, format="wav")
