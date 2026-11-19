#!/usr/bin/env node
// LSPV-2/2026-11-18: independent exhaustive signed-clause compiler audit.
// Reference semantics only. Not the native mixed-calculus checker.
'use strict';
const crypto = require('crypto');
function litTrue(lit, z, y, p) {
  const v = Math.abs(lit);
  const a = v === 1 ? (z >> 1) & 1 :
            v === 2 ? z & 1 :
            v === 3 ? (y >> 1) & 1 :
            v === 4 ? y & 1 : p;
  return lit > 0 ? a === 1 : a === 0;
}
function clauseTrue(cl, z, y, p) {
  return cl.some(l => litTrue(l, z, y, p));
}
function transform(cl, z) {
  const satZ = cl.some(l => Math.abs(l) <= 2 && litTrue(l, z, 0, 0));
  const out = satZ ? [5, -5, 5] : cl.map(l => Math.abs(l) <= 2 ? 5 : l);
  return [out, [-5,-5,-5]];
}
function guestBits(clauses) {
  const bits = [];
  for (const cl of clauses) for (const l of cl) {
    let id = Math.abs(l) - 1;
    bits.push((id >> 2) & 1, (id >> 1) & 1, id & 1, Number(l < 0));
  }
  return bits;
}
const signs = [1,-1,2,-2,3,-3,4,-4];
let tests=0, incorrect=0, badPortCaught=0, maxPacketBits=0;
let sha = crypto.createHash('sha256');
for (const a of signs) for (const b of signs) for (const c of signs) {
  const cl = [a,b,c];
  sha.update(JSON.stringify(cl)+'\n');
  for (let z=0; z<4; z++) {
    const packet = transform(cl,z);
    const serialized = guestBits(packet);
    if (serialized.length!==24) throw Error('fixed packet size violated');
    maxPacketBits=Math.max(maxPacketBits,serialized.length);
    for (let i=0; i<24; i++) {
      let ci=Math.floor(i/12), field=Math.floor((i%12)/4), pos=i%4;
      const lit=packet[ci][field], id=Math.abs(lit)-1;
      const got=pos===3?Number(lit<0):(id>>(2-pos))&1;
      if(got!==serialized[i]) throw Error('bit accessor mismatch');
    }
    for (let y=0; y<4; y++) {
      const original=clauseTrue(cl,z,y,0);
      const sub0=packet.every(cc=>clauseTrue(cc,z,y,0));
      const sub1=packet.every(cc=>clauseTrue(cc,z,y,1));
      tests++;
      if(original!==sub0 || sub1) incorrect++;
    }
  }
}
const hostile = transform([1,1,1],0).slice(0,1);
badPortCaught = hostile.every(cl=>clauseTrue(cl,0,0,1)) && !clauseTrue([1,1,1],0,0,0) ? 1:0;
if(incorrect || !badPortCaught) throw Error(`failed semantic audit: ${incorrect} bad, negative control ${badPortCaught}`);
console.log(JSON.stringify({status:'PASS independent exhaustive signed-clause equivalence',
 clauses_tested:512, shared_assignments:4,private_assignments:4,
 semantic_cases:tests, errors:incorrect,guest_field_bits_per_two_clause_packet:maxPacketBits,
 hostile_no_unit_mismatch_detected:badPortCaught, corpus_sha256:sha.digest('hex')},null,2));
