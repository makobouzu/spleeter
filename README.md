<img src="https://github.com/deezer/spleeter/raw/master/images/spleeter_logo.png" height="80" />

[![Github actions](https://github.com/deezer/spleeter/workflows/pytest/badge.svg)](https://github.com/deezer/spleeter/actions) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/spleeter) [![PyPI version](https://badge.fury.io/py/spleeter.svg)](https://badge.fury.io/py/spleeter) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/deezer/spleeter/blob/master/spleeter.ipynb) [![Gitter chat](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/spleeter/community) [![status](https://joss.theoj.org/papers/259e5efe669945a343bad6eccb89018b/status.svg)](https://joss.theoj.org/papers/259e5efe669945a343bad6eccb89018b)

> :warning: [Spleeter 2.1.0](https://pypi.org/project/spleeter/) release introduces some breaking changes, including new CLI option naming for input, and the drop
> of dedicated GPU package. Please read [CHANGELOG](CHANGELOG.md) for more details.

## About

**Spleeter** is [Deezer](https://www.deezer.com/) source separation library with pretrained models
written in [Python](https://www.python.org/) and uses [Tensorflow](https://tensorflow.org/). It makes it easy
to train source separation model (assuming you have a dataset of isolated sources), and provides
already trained state of the art model for performing various flavour of separation :

* Vocals (singing voice) / accompaniment separation ([2 stems](https://github.com/deezer/spleeter/wiki/2.-Getting-started#using-2stems-model))
* Vocals / drums / bass / other separation ([4 stems](https://github.com/deezer/spleeter/wiki/2.-Getting-started#using-4stems-model))
* Vocals / drums / bass / piano / other separation ([5 stems](https://github.com/deezer/spleeter/wiki/2.-Getting-started#using-5stems-model))

2 stems and 4 stems models have [high performances](https://github.com/deezer/spleeter/wiki/Separation-Performances) on the [musdb](https://sigsep.github.io/datasets/musdb.html) dataset. **Spleeter** is also very fast as it can perform separation of audio files to 4 stems 100x faster than real-time when run on a GPU.

We designed **Spleeter** so you can use it straight from [command line](https://github.com/deezer/spleeter/wiki/2.-Getting-started#usage)
as well as directly in your own development pipeline as a [Python library](https://github.com/deezer/spleeter/wiki/4.-API-Reference#separator). It can be installed with [pip](https://github.com/deezer/spleeter/wiki/1.-Installation#using-pip).

### Projects and Softwares using **Spleeter**

Since it's been released, there are multiple forks exposing **Spleeter** through either a Guided User Interface (GUI) or a standalone free or paying website. Please note that we do not host, maintain or directly support any of these initiatives.

That being said, many cool projects have been built on top of ours. Notably the porting to the *Ableton Live* ecosystem through the [Spleeter 4 Max](https://github.com/diracdeltas/spleeter4max#spleeter-for-max) project.

**Spleeter** pre-trained models have also been used by professionnal audio softwares. Here's a non-exhaustive list:

* [iZotope](https://www.izotope.com/en/shop/rx-8-standard.html) in its *Music Rebalance* feature within **RX 8**
* [SpectralLayers](https://new.steinberg.net/spectralayers/) in its *Unmix* feature in **SpectralLayers 7**
* [Acon Digital](https://acondigital.com/products/acoustica-audio-editor/) within **Acoustica 7**
* [VirtualDJ](https://www.virtualdj.com/stems/) in their stem isolation feature
* [Algoriddim](https://www.algoriddim.com/apps) in their **NeuralMix** and **djayPRO** app suite

🆕 **Spleeter** is a baseline in the ongoing [Music Demixing Challenge](https://www.aicrowd.com/challenges/music-demixing-challenge-ismir-2021)!

## Setting

* Mac OS: Catalina
* fish
* python 3.7.7

```fish
cd spleeter
# python version 3.7.7
python -m venv venv
# activate virtual-env in fish
source venv/bin/activate.fish
# install ffmpeg
brew install ffmpeg
# install spleeter with pip
pip install spleeter
# separate the example audio into simple two components(vocals/accompaniment)
spleeter separate -p spleeter:2stems -o output audio_sample/audio_example.mp3
```

## Original Train

I would like to use Spleeter's system to perform my own source separation and labeling. human / bird / car [3stems]
### Train Process

1. Prepare dataset
2. Rewrite configs/master_config.json
3. Sort and prepare Dataset for train and test(human.wav / bird.wav / car.wav / mixture.wav)
4. Create csv file(master_trai.csv / master_validation.csv)
5. Train
6. Add checkpoint and models to pretrained_models dir
7. Add 3stems.json to package source file

#### Prepare dataset

* Human
  * [mozilla Common Voice](https://commonvoice.mozilla.org/ja/datasets)
  * [Chiba3Party](https://www.nii.ac.jp/dsc/idr/speech/submit/Chiba3Party.html)
* Bird
  * [Macaulay Library](https://www.macaulaylibrary.org/2020/12/07/the-brand-new-cornell-guide-to-bird-sounds-is-here/)
* Car
  * [SONYC Urban Sound Tagging](http://dcase.community/challenge2019/task-urban-sound-tagging)
  * [ESC-50](https://github.com/karolpiczak/ESC-50)

Please move each sound file in the dataset to train/dataset/. Change each sound file format 44.1kHz/16bit stereo.

```fish
cd spleeter/train
# Change 48kHz/16bit mono -> 44.1kHz/16bit mono
python format_helps/48kHz-441kHz.py dataset/human
# Change mono -> stereo
python format_helps/mono-stereo.py dataset/human
```

If you have another good dataset ready, please let me know!!

#### Rewrite configs/master_config.json

```master_config.json
{
    "train_csv": "configs/master_train.csv",
    "validation_csv": "configs/master_validation.csv",
    "model_dir": "master_model",
    "instrument_list": ["human", "bird", "car"],
}
```

#### Sort and prepare Dataset for train and test(human.wav / bird.wav / car.wav / mixture.wav)

```fish
# Create 5min wav
python create_5m_wav.py dataset/category category vol
    # Create 5min human.wav
    python create_5m_wav.py dataset/human human 0.0
    # Create 5min bird.wav
    python create_5m_wav.py dataset/bird bird -10.0
    # Create 5min car.wav
    python create_5m_wav.py dataset/human car -15.0
    # Create mixture.wav
python create_mixture.py train human_vol bird_vol car_vol
```

In my case, I prepared 100 files in train and 20 files in test. 
I haven't written a script for test, so you will have to manually move it from the train dir to test.

#### Create csv file(master_trai.csv / master_validation.csv)

```fish
# Create master_train.csv
python create_csv.py train master_train.csv
# Create master_test.csv
python create_csv.py test master_test.csv
# Move to config dir
cd ../ (current dir = spleeter/)
mv -F train/master_train.csv configs/
mv -F train/master_test.csv configs/
```

#### Train

```fish
spleeter train -p configs/master_config.json -d train
```

You may be get master_model dir including checkpoint / model.ckpt-200000.data-00000-of-00001 / model.ckpt-200000.index / model.ckpt-200000.meta.

#### Add checkpoint and models to pretrained_models dir

```fish
# Create pretrained_model dir
mkdir pretrained_models
mkdir pretrained_models/3stems
# Move model files
mv master_model/checkpoint pretrained_models/3stems 
mv master_model/model.ckpt-200000.data-00000-of-00001 pretrained_models/3stems
mv master_model/model.ckpt-200000.index pretrained_models/3stems
mv master_model/model.ckpt-200000.meta pretrained_models/3stems
mv master_model/.probe pretrained_models/3stems
```

#### Add 3stems.json to package source file

If you run, it will spit out an error like the one below.

```fish
# Run
spleeter separate -p spleeter:3stems -o output audio_example.mp3
# -> error
#ERROR:spleeter:No embedded configuration 3stems found
#Exception ignored in: <function Separator.__del__ at 0x1428e9ef0>
#Traceback (most recent call last):
#  File "/Users/makobouzu/Documents/Python/spleeter/venv/lib/python3.7/site-packages/spleeter/separator.py", line 134, in __del__
#    if self._session:
#AttributeError: 'Separator' object has no attribute '_session'
```

Need to move 3stems.json to $HOME/.pyenv/versions/3.7.7/lib/python3.7/site-packages/spleeter/resources/

```fish
# Move 3stems.json
mv train/3stems.json $HOME/.pyenv/versions/3.7.7/lib/python3.7/site-packages/spleeter/resources/
```

#### Run

```fish
# Run
spleeter separate -p spleeter:3stems -o output audio_example.mp3
```


## Reference

* Deezer Research - Source Separation Engine Story - deezer.io blog post:
  * [English version](https://deezer.io/releasing-spleeter-deezer-r-d-source-separation-engine-2b88985e797e)
  * [Japanese version](http://dzr.fm/splitterjp)
* [Music Source Separation tool with pre-trained models / ISMIR2019 extended abstract](http://archives.ismir.net/ismir2019/latebreaking/000036.pdf)

If you use **Spleeter** in your work, please cite:

```BibTeX
@article{spleeter2020,
  doi = {10.21105/joss.02154},
  url = {https://doi.org/10.21105/joss.02154},
  year = {2020},
  publisher = {The Open Journal},
  volume = {5},
  number = {50},
  pages = {2154},
  author = {Romain Hennequin and Anis Khlif and Felix Voituret and Manuel Moussallam},
  title = {Spleeter: a fast and efficient music source separation tool with pre-trained models},
  journal = {Journal of Open Source Software},
  note = {Deezer Research}
}
```

## License

The code of **Spleeter** is [MIT-licensed](LICENSE).

## Disclaimer

If you plan to use **Spleeter** on copyrighted material, make sure you get proper authorization from right owners beforehand.

## Troubleshooting

**Spleeter** is a complex piece of software and although we continously try to improve and test it you may encounter unexpected issues running it. If that's the case please check the [FAQ page](https://github.com/deezer/spleeter/wiki/5.-FAQ) first as well as the list of [currently open issues](https://github.com/deezer/spleeter/issues)

### Windows users

   It appears that sometimes the shortcut command `spleeter` does not work properly on windows. This is a known issue that we will hopefully fix soon. In the meantime replace `spleeter separate` by `python -m spleeter separate` in command line and it should work.

## Contributing

If you would like to participate in the development of **Spleeter** you are more than welcome to do so. Don't hesitate to throw us a pull request and we'll do our best to examine it quickly. Please check out our [guidelines](.github/CONTRIBUTING.md) first.

## Note

This repository include a demo audio file `audio_example.mp3` which is an excerpt
from Slow Motion Dream by Steven M Bryant (c) copyright 2011 Licensed under a Creative
Commons Attribution (3.0) [license](http://dig.ccmixter.org/files/stevieb357/34740)
Ft: CSoul,Alex Beroza & Robert Siekawitch
