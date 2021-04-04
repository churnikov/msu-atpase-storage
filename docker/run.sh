#!/bin/bash
cp $HOME/.config/gdrive/settings.yaml /code/
cp $HOME/.config/gdrive/credentials.json /code/
python3 /code/msu_atpase_storage/__init__.py
