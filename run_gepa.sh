#!/bin/bash
# Wrapper that loads MINIMAX_API_KEY from hermes .env before running GEPA
KEY=$(grep "^MINIMAX_API_KEY=" ~/.hermes/.env 2>/dev/null | cut -d= -f2)
export MINIMAX_API_KEY="$KEY"
export LITELLM_API_BASE="https://api.minimax.io/v1"
cd /home/Hermes/repos/gepa
source .venv/bin/activate
python "$@"