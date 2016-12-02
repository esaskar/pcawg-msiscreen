#!/bin/bash
#
# Create microsatellite reference of msisensor
#
# Default parameters:
#       -l   <int>      minimal homopolymer size, default=5
#       -c   <int>      context length, default=5
#       -m   <int>      maximal homopolymer size, default=50
#       -s   <int>      maximal length of microsate, default=5
#       -r   <int>      minimal repeat times of microsate, default=3
#       -p   <int>      output homopolymer only, 0: no; 1: yes, default=0

mkdir -p /shared/data/msisensor
/opt/msisensor/msisensor scan -d /shared/data/reference/genome.fa \
  -o /shared/data/msisensor/genome.microsatellites
