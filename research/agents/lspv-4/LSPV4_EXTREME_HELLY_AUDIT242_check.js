// LSPV-4 EXTREME-HELLY-AUDIT242 independent minimal source-pair checker
'use strict';const assert=require('assert');
const W='-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14';
const S='-1 -3 14;2 8 -9;-10 13 14;3 -7 -13;-4 9 -11;-5 -8 -14;4 -8 11;1 7 -13;1 -7 10;-5 -6 15;-2 6 -12;4 9 -10;-2 5 -12;3 6 -15;-6 7 11;2 -9 -11;-4 8 10;-3 12 15;5 12 -15;-1 13 -14';
const parse=s=>s.split(';').map(x=>x.trim().split(/ +/).map(Number));
function local(c,m){let d=new Map;for(const z of c)d.set(Math.abs(z),m==='S'?Number(z>0):Number(z<0));return d;}
function pair(c,d){const a=local(c,'S'),b=local(d,'S');let same=0,opp=0;for(const [v,z] of a)if(b.has(v)){if(z===b.get(v))same++;else opp++;}return {same,opp,SS:opp===0,SU:same===0,US:same===0,UU:opp===0};}
function realized(F,idx,mode){const all=new Map;for(let k=0;k<idx.length;k++)for(const [v,z] of local(F[idx[k]],mode[k])){if(all.has(v)&&all.get(v)!==z)return false;all.set(v,z);}return true;}
function resolve(c,d,p){let R=[...new Set([...c.filter(z=>z!==p),...d.filter(z=>z!==-p)])];if(R.some(z=>R.includes(-z)))return null;return R;}
function check(F){let pairs=0,triple=0,mixed=0,first=0,unique=new Set;
for(let j=0;j<F.length;j++)for(let k=j+1;k<F.length;k++){
 const p=pair(F[j],F[k]);if(p.same&&p.opp)mixed++;
 for(const mode of ['SS','SU','US','UU']){assert.strictEqual(realized(F,[j,k],mode.split('')),p[mode]);pairs++;}
 for(const z of F[j])if(F[k].includes(-z)){let R=resolve(F[j],F[k],z);assert.strictEqual(R!==null,p.opp===1);if(R){assert.strictEqual(R.length,F[j].length+F[k].length-2-p.same);first++;unique.add(R.slice().sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b).join(','));}}
}
for(let j=0;j<Math.min(9,F.length);j++)for(let k=j+1;k<Math.min(9,F.length);k++)for(let h=k+1;h<Math.min(9,F.length);h++)for(let b=0;b<8;b++){
 const mode=[(b&1)?'S':'U',(b&2)?'S':'U',(b&4)?'S':'U'];let predicted=pair(F[j],F[k])[mode[0]+mode[1]]&&pair(F[j],F[h])[mode[0]+mode[2]]&&pair(F[k],F[h])[mode[1]+mode[2]];
 assert.strictEqual(predicted,realized(F,[j,k,h],mode));triple++;
}return {pairs,triple,mixed,first,unique:unique.size};}
let out={};for(const [name,F] of Object.entries({W1:parse(W),S15:parse(S),XOR3:[[1,2,3],[1,-2,-3],[-1,2,-3],[-1,-2,3]],MIXED:[[1,2,3],[1,-2,4]],MIXED_TAUT:[[1,2,3],[1,-2,-3]]})){out[name]=check(F);}
assert.strictEqual(out.W1.first,60);assert.strictEqual(out.W1.unique,60);assert.strictEqual(out.S15.unique,46);assert.strictEqual(out.XOR3.first,0);
const Wpos=Array.from({length:15},()=>[0,0]);for(const c of parse(W))for(const z of c)Wpos[Math.abs(z)-1][Number(z<0)]++;
assert(Wpos.every(p=>p[0]===2&&p[1]===2));
console.log(JSON.stringify({run:'EXTREME-HELLY-AUDIT242',checks:out,exact_signed_occurrence_upper_bound_4n:60,status:'finite crosscheck; P vs NP OPEN'}));
// END_OF_VERIFIED_CHECKER::LSPV-4::EXTREME-HELLY-AUDIT242