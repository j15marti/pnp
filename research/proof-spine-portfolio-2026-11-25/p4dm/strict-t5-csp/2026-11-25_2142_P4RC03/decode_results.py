import base64,gzip,hashlib,json,pathlib
raw=gzip.decompress(base64.b64decode(pathlib.Path("raw_results.json.gz.b64").read_text()))
assert hashlib.sha256(raw).hexdigest()=="9054cebb31cda4fb0901ab5e80f1757105c6d8ed660bad5237c0e72ad91eb375"
for name,contents in json.loads(raw).items():
 pathlib.Path(name).write_text(contents)
