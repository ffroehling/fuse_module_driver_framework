#!/bin/bash

#set environment variable
echo 'export FUSE_LIBRARY_PATH=/usr/lib/libfuse.so' > ~/.profile
source ~/.profile

pip install -r requirements.txt
