# Product-span experiment

This experiment measures

`rho = dim_F2 span{1, g_i, g_i g_j}`

for explicitly implemented Boolean encoders.

## Guard

The included runner implements **only a toy affine encoder**. It is a sanity check for the algebra and tests.

It is **not** an implementation of the Shaltiel–Umans / van Melkebeek–Mocelin Sdroievski construction.

Do not add an `--su-vms` mode until every required generator, encoder, projection, and adaptive extractor step has been transcribed from an identified primary-source theorem/definition and covered by tests.

Run:

```bash
python experiments/product_span/run.py --toy-affine --source-bits 4 --outputs 8 --seed 1
```
