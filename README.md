# GHZ Detection Plot

This repository contains the code to generate raw data and process data for plots. It also contains generated raw data for N less than 16.

## Prerequisites

Python 3, Numpy, and GNU Plot.

## Raw data

Raw data for N less than 16 are in `results/` folder. You don't need to run the code to generate them again which may take a long time.

You need to unzip `*.zip` files.

## Processing raw data

Edit the for loop in `processing_for_gnuplot.py` and then run,

```
python3 processing_for_gnuplot.py
```

Then edit `script.gnuplot` and run it with GNU Plot. You can write your plotting script as well.

## Generate raw data

This step is just for re-generating raw data in `results/`. Edit the for loop in `generation.py` and then run,

```
python3 generation.py
```

This may take a long time.
