#!/bin/bash

sensors=$(sensors)

head -n10 /proc/cpuinfo | grep 'model name'
lscpu | grep 'CPU M'
grep 'cpu MHz' /proc/cpuinfo
grep Tdie <<< "$sensors"
grep 'CPU Fan' <<< "$sensors"
grep 'Chassis Fan' <<< "$sensors"
grep Tsensor <<< "$sensors"

echo nvme:
grep Composite <<< "$sensors"

echo RX6800 XT:
grep edge <<< "$sensors"
grep fan1 <<< "$sensors"
grep junction <<< "$sensors"
grep mem <<< "$sensors"
grep power1 <<< "$sensors"
