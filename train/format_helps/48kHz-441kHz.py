#!/usr/bin/env python
#python 48kHz-441kHz.py input_folder
#Change input(mono 48kHz 16bit) wavfile -> output(mono 44.1kHz 16bit) wavfile

from fractions import Fraction
import numpy as np
import scipy as sp
import scipy.signal as sg
import soundfile as sf
import pydub
import sys
import glob
from tqdm import tqdm

if __name__ == "__main__":
    args = sys.argv
    
    print("folder " + args[1] + ": change 48kHz to 44.1kHz!")
    
    fs_target = 44100
    cutoff_hz = 21000.0
    n_lpf = 4096
    sec = 20
        
    wav_folder = glob.glob(args[1] + "/*.wav")
    for file in tqdm(wav_folder):
        wav, fs_src = sf.read(file)
        if fs_src == 48000:
            wav_origin = wav[:fs_src * sec]
            frac = Fraction(fs_target, fs_src)
            up = frac.numerator
            down = frac.denominator
            wav_up = np.zeros(np.alen(wav_origin) * up)
            wav_up[::up] = up * wav_origin
            fs_up = fs_src * up
            cutoff = cutoff_hz / (fs_up / 2.0)
            lpf = sg.firwin(n_lpf, cutoff)
            wav_down = sg.lfilter(lpf, [1], wav_up)[n_lpf // 2::down]
            sf.write(file, wav_down, fs_target)
#            print("resample 48kHz -> 44.1kHz : " + file)
