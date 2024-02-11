#!/bin/bash

sensors=$(sensors)

head -n10 /proc/cpuinfo | grep 'model name' | awk -F ': ' '{print $2}'
lscpu | grep 'CPU M'
grep 'cpu MHz' /proc/cpuinfo
grep 'CPU T' <<< "$sensors"
grep 'CPU Fan' <<< "$sensors"
grep 'Chassis Fan' <<< "$sensors"

echo water:
grep 'Water Pump' <<< "$sensors"
grep Tsensor <<< "$sensors"

echo nvme:
grep Composite <<< "$sensors"

lspci -mm | grep 'VGA compatible controller' | awk -F '"' '{print $6}'
grep edge <<< "$sensors"
grep fan1 <<< "$sensors"
grep junction <<< "$sensors"
grep mem <<< "$sensors"
grep power1 <<< "$sensors"
