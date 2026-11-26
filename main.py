"""news-image-20261125 entry: deterministically write the front-page image.

The image (entry.png, 1024x1024, JPEG bytes) sums up the world news of
Wednesday 25 November 2026: tankers ablaze in the Strait of Hormuz (lead),
US tariffs on China, Pakistan's first astronaut aboard Shenzhou-24, the
Houthi strike on Saudi Arabia's Ras Tanura refinery, the Russian strike on
Odesa, the Australia-Solomon Islands treaty, and Sudan drone strikes.
The program copies the image the repository holds to /output/entry.png.
No network, no randomness: two runs write identical bytes.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DST = os.path.join(OUT_DIR, "entry.png")

os.makedirs(OUT_DIR, exist_ok=True)
shutil.copyfile(SRC, DST)
print(f"wrote {DST} ({os.path.getsize(DST)} bytes)")
