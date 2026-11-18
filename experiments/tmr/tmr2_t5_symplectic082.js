#!/usr/bin/env node
'use strict';
// TMR-2/082 hash-checking launcher; Node.js standard library only.
// Run: node experiments/tmr/tmr2_t5_symplectic082.js --pc
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),zlib=require('node:zlib'),cp=require('node:child_process');
const archive=path.join(__dirname,'tmr2_t5_symplectic082.js.gz.b64');
const packed=fs.readFileSync(archive,'utf8').trim();
const source=zlib.gunzipSync(Buffer.from(packed,'base64'));
const SHA='7762b18fa9a6054a7271353c4f07af897e9d9c3af42eec79442b400c9e90a940';
if(crypto.createHash('sha256').update(source).digest('hex')!==SHA)throw Error('Executed source hash mismatch');
const code=source.toString('utf8').replace(/^#![^\n]*\n/,'');
const result=cp.spawnSync(process.execPath,['-e',code,'--',...process.argv.slice(2)],{stdio:'inherit'});
if(result.error)throw result.error;
process.exit(result.status===null?1:result.status);
