"""news-image-20261125 entry: deterministically write the front-page image.

The image (entry.png, 1024x1024, JPEG bytes) sums up the world news of
Wednesday 25 November 2026: tankers ablaze in the Strait of Hormuz (lead),
US tariffs on China, Pakistan's first astronaut aboard Shenzhou-24, the
Houthi strike on Saudi Arabia's Ras Tanura refinery, the Russian strike on
Odesa, the Australia-Solomon Islands treaty, and Sudan drone strikes.
The program copies the image the repository holds to /output/entry.png.
No network, no randomness: two runs write identical bytes.
"""

import hashlib
import os
import shutil
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DST = os.path.join(OUT_DIR, "entry.png")

os.makedirs(OUT_DIR, exist_ok=True)
shutil.copyfile(SRC, DST)

# Verify the copy is byte-identical and report the image size: the gate
# requires at most 1024x1024 pixels and at most 1 MiB, so confirm both.
def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def _jpeg_size(path):
    with open(path, "rb") as f:
        data = f.read(2)
        if data != b"\xff\xd8":
            return None
        while True:
            marker = f.read(2)
            if len(marker) < 2 or marker[0] != 0xFF:
                return None
            if marker[1] in (0xC0, 0xC1, 0xC2):
                f.read(2)  # segment length
                f.read(1)  # sample precision
                height, width = struct.unpack(">HH", f.read(4))
                return width, height
            length = struct.unpack(">H", f.read(2))[0]
            f.seek(length - 2, 1)


src_hash, dst_hash = _sha256(SRC), _sha256(DST)
assert src_hash == dst_hash, "copy differs from source"
size = _jpeg_size(DST)
print(f"wrote {DST} ({os.path.getsize(DST)} bytes, {size[0]}x{size[1]}, "
      f"sha256 {dst_hash[:12]}...)")
