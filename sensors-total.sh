#!/bin/bash

echo R5 2600:
lscpu | grep 'CPU M'
cat /proc/cpuinfo | grep 'cpu MHz'
sensors | grep Tdie
sensors | grep 'CPU Fan'
sensors | grep 'Chassis Fan'
sensors | grep 'Tsensor'

echo nvme:
sensors | grep Composite

echo RX6800 XT:
sensors | grep edge
sensors | grep fan1
sensors | grep junction
sensors | grep mem
sensors | grep power1

echo HD3600:
sensors | grep temp1
