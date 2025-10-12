#!/bin/bash

rm energy_densities.txt
cd output/test0/ || { echo "Directory not found!"; exit 1; }
rm *

echo "removed chains"
