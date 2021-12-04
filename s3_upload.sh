#!/bin/bash
aws s3 cp info.csv s3://neighbour-data/neighbour-$(date +%F)-$(date +%H)-$(date +"%T").csv.csv