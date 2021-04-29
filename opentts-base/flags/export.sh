#!/usr/bin/env bash
set -e
this_dir="$( cd "$( dirname "$0" )" && pwd )"

# Large
find "${this_dir}" -name '*_large.svg' -type f -print0 | \
    parallel -0 -n1 \
          inkscape --export-png="{.}.png" {} -w 90

# Small
find "${this_dir}" -name '*_small.svg' -type f -print0 | \
    parallel -0 -n1 \
             inkscape --export-png="{.}.png" {} -w 38
