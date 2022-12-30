#!/bin/zsh
cd ~/git/weeabosensei.github.io/rssfeed/
python3 generateFeeds.py
git commit -am 'update'
git push
