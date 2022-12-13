#!/bin/sh -eux

./build.py
python -m http.server --directory dist 9000
rm -rf dist
