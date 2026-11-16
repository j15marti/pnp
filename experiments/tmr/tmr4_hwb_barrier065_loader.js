'use strict';
// Validates exact published compressed JS source before executing the deterministic audit.
const fs=require('node:fs');
const path=require('node:path');
const zlib=require('node:zlib');
const crypto=require('node:crypto');
const p=path.join(__dirname,'tmr4_hwb_barrier065.js.zlib.b64');
const bytes=zlib.inflateSync(Buffer.from(fs.readFileSync(p,'utf8').trim(),'base64'));
const sha=crypto.createHash('sha256').update(bytes).digest('hex');
const expected='8f86d7aa03e6567f18b31e911da7e63665cecfce40ec8307a833ee4a39caf1b4';
if(sha!==expected)throw new Error('source SHA mismatch '+sha);
const moduleForSource={exports:{}};
new Function('require','module',bytes.toString('utf8')+'\nmain();')(require,moduleForSource);
