#!/usr/bin/env python
# coding: utf-8

# You can choose the result in results folder to generate plot using GNU Plot.

from calhelperminimal import CalHelperMinimal

for N in [5,10,15]:
    util00 = CalHelperMinimal(N)
    util00.read_results('results/N_{}.txt'.format(N))
    util00.write_points('Res_To_Plot_{}.dat'.format(N))


# Then you can call script.gnuplot and set `Res_To_Plot_{}.dat` as input.
