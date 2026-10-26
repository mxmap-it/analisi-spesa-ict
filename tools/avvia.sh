#!/bin/bash
# Lanciatore: evita che un pkill o un pgrep digitato altrove si auto-colpisca.
cd ~/analisi-spesa-ict
exec .venv/bin/python "$@"
