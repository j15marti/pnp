"""Decode and authenticate the exact executed P4RC04 audit and raw results."""
import base64, gzip, hashlib, json
from pathlib import Path
root = Path(__file__).resolve().parent
raw = gzip.decompress(base64.b64decode("".join((root / f"archive.part{i}.b64").read_text().strip() for i in range(1, 5)), validate=True))
assert hashlib.sha256(raw).hexdigest() == "c1499a238025870ee7058467fbd9e4d77cd3e912d58fda68d776ce8b18709226"
expected = {
    "audit.py": "d7fc5b06e4aca878e83649e3ac08a0929711aa07",
    "small.json": "4ce3eadc0ed8c1786118b939029bc28d4f3e6791",
    "large.json": "47db105a701681a0060a85ac5f6b4fdae88db704",
    "hostile.json": "050a1f34775c113e21565b9e95c225d4d03e119b",
    "abstract.json": "d212e4a02ff60b466f15a57e32908b032766d0ba",
}
files = json.loads(raw)
assert set(files) == set(expected)
out = root / "decoded"
out.mkdir(exist_ok=True)
for name, text in files.items():
    data = text.encode("utf-8")
    blob = hashlib.sha1(f"blob {len(data)}".encode() + bytes([0]) + data).hexdigest()
    assert blob == expected[name], (name, blob)
    target = out / name
    if target.exists():
        assert target.read_bytes() == data, f"Refusing to overwrite {target}"
    else:
        target.write_bytes(data)
print("Authenticated five files in", out)
