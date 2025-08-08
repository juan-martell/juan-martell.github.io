#!/bin/bash

python /root/meli/meli.py
cd /root/meli/juan-martell.github.io/
git pull
git add /root/meli/juan-martell.github.io/
git commit -m "actualizo top.json"
git push origin main
