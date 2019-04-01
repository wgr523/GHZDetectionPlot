#!/usr/bin/env python
# coding: utf-8

# You can choose the result in results folder to generate plot using GNU Plot.

from calhelper import CalHelperSimple

for N in [2,3,4]:
    u = CalHelperSimple(N)
    u.read_results('results/N_{}.txt'.format(N))
    u.write_points('Res_To_Plot_{}.dat'.format(N))


# Then you can call script.gnuplot and set `Res_To_Plot_{}.dat` as input.
