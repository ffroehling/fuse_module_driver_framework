#!/bin/bash
export FUSE_LIBRARY_PATH=/usr/lib/libfuse.so
cd kernelabstraction
python3 abstraction.py &  > /tmp/log
