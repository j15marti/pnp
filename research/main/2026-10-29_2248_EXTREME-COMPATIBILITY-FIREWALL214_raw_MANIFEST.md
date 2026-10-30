# EXTREME-COMPATIBILITY-FIREWALL214 raw-result manifest

The complete 13 MiB UTF-8 JSON was compressed, base64-encoded, and split only for GitHub transport. Reconstruct from this directory with:

```bash
cat 2026-10-29_2248_EXTREME-COMPATIBILITY-FIREWALL214_raw.part{00,01,02,03,04} > raw.json.gz.b64
base64 -d raw.json.gz.b64 > raw.json.gz
gzip -dc raw.json.gz > raw.json
sha256sum raw.json
```

Expected complete raw JSON SHA-256:

`c7e8fe1b7b825a057707f5dc75b07cb8d571ae3bc3723b587ee6c35adbfc8302`

Intermediate hashes:

- gzip: `d97ef20ddbb0d616177eff35ae79b1a6002a6fecec852dfcb7db1fbc7d7ef4e0`
- base64 text: `77f8beab89ae96cc07d21c7230863bb33a376da3390c5daacfd0501495635d81`
- part00: `7d2afbb89e50126bdd1529b0cf8479c4f3f404918234a87ca9837fc94cf4cd57`
- part01: `e6512d0b973c1cace16bfc980910d14804161a712f70c0512020cd50db57190b`
- part02: `86a69d831496af57400426e075d171f90f8f7d30ae7edc431638c03ee1cda118`
- part03: `71362589b0ba61f6652ef5d3c2ea3dd96760010b91b02e32e55bc9afde1a1862`
- part04: `9cc9ec2fc2be5d3ad75b926bd45321ecfebabf0cb62a5f410201990db9dd3d16`

The concise JSON summary is separately published for direct inspection. The reproducer deterministically regenerates both full and summary data.

