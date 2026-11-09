#!/usr/bin/env node
'use strict';
// Independent noncommutative Magnus expansion modulo degree four.
// Formal free-group words only; does not compute knot/link invariants.
const degree=3;
function enc(a){return a.join(',')}
function dec(s){return s===''?[]:s.split(',').map(Number)}
function mul(x,y){const z=new Map();for(const[p,v]of x)for(const[q,w]of y){const a=dec(p),b=dec(q);if(a.length+b.length>degree)continue;const k=enc([...a,...b]);z.set(k,(z.get(k)||0)+v*w)}for(const[k,v]of z)if(v===0)z.delete(k);return z}
function letter(id,e){const p=new Map([['',1]]);if(e===1)p.set(String(id),1);else for(let i=1;i<=degree;i++)p.set(Array(i).fill(id).join(','),(-1)**i);return p}
function inverse(x){return [...x].reverse().map(([i,e])=>[i,-e])}
function bracket(a,b){return [...a,...b,...inverse(a),...inverse(b)]}
function jet(a,b,c){let p=new Map([['',1]]);const w=bracket([[a,1]],bracket([[b,1]],[[c,1]]));if(w.length!==10)throw Error('incorrect word');for(const [i,e] of w)p=mul(p,letter(i,e));if(p.get('')!==1)throw Error('constant');p.delete('');return p}
function target(a,b,c){return new Map([[[a,b,c].join(','),1],[[a,c,b].join(','),-1],[[b,c,a].join(','),-1],[[c,b,a].join(','),1]])}
function equal(a,b){return a.size===b.size&&[...a].every(([k,v])=>b.get(k)===v)}
let tested=0;for(let a=0;a<6;a++)for(let b=0;b<6;b++)for(let c=0;c<6;c++){if(a===b||a===c||b===c)continue;if(!equal(jet(a,b,c),target(a,b,c)))throw Error('coefficient mismatch');tested++}
if(jet(1,2,2).size!==0)throw Error('bracket of equal generators must vanish');
const changed=new Set([...jet(1,2,3).keys(),...jet(4,2,3).keys()]);
if(changed.size!==8)throw Error('signed-literal replacement not disjoint');
console.log(JSON.stringify({status:'PASS',distinct_ordered_triples_tested:tested,bracket_duplicate_zero:true,one_signed_generator_change_positions:changed.size,scope:'formal word algebra only'}));
