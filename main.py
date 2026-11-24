#!/usr/bin/env python3
"""Entry program for news-image-20261123.

The page itself is the PNG sitting next to this file. This program does one
job: place that PNG at the grader's output path so the judge sees exactly
the bytes that were drawn. It takes no arguments and needs no packages
beyond the Python standard library.

Outside the grading container, set MAKEFUN_OUTPUT_DIR to a scratch folder
to see the copy land there instead of /output:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
DEST_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

DEST_DIR.mkdir(parents=True, exist_ok=True)
shutil.copyfile(SOURCE, DEST_DIR / "entry.png")
