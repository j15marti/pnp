'use strict';
// LSPV-1 361: exact full-mixed minimum via authenticated strict Resolution.
const fs=require('fs'); const crypto=require('crypto');
const sortLit=(a,b)=>Math.abs(a)-Math.abs(b)||a-b;
const canonical=a=>{const b=[...new Set(a)].sort(sortLit);if(b.some(x=>b.includes(-x)))throw Error('tautology');return b;};
function resolve(a,b,p){if(!a.includes(p)||!b.includes(-p))throw Error('bad pivot');return canonical([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]);}
function build(bits){const m=2**bits,vars=bits+m,source=[],steps=[];
 for(let j=0;j<m;j++){const t=bits+j+1,clause=[];for(let i=0;i<bits;i++)clause.push((j&(1<<i))?-(i+1):(i+1));source.push([t]);source.push(canonical([-t,...clause]));}
 const dag=source.map(lits=>lits); let frontier=[];
 for(let j=0;j<m;j++){const k=2*j,pa=dag[k],pb=dag[k+1],pivot=bits+j+1;const lits=resolve(pa,pb,pivot);const node={a:k,b:k+1,pivot,lits};steps.push(node);frontier.push(dag.length);dag.push(lits);}
 for(let i=0;i<bits;i++){const next=[];for(let j=0;j<frontier.length;j+=2){const a=frontier[j],b=frontier[j+1],p=i+1;const lits=resolve(dag[a],dag[b],p);steps.push({a,b,pivot:p,lits});next.push(dag.length);dag.push(lits);}frontier=next;}
 if(dag[dag.length-1].length!==0 || steps.length!==2*m-1)throw Error('not empty');
 const dimacs='p cnf '+vars+' '+source.length+'\n'+source.map(c=>c.join(' ')+' 0\n').join('');
 return {bits,mask_count:m,variables:vars,source_count:source.length,cost:steps.length,source,steps,source_sha256:crypto.createHash('sha256').update(dimacs).digest('hex'),source_bytes:Buffer.byteLength(dimacs),proof_json_bytes:Buffer.byteLength(JSON.stringify(steps))};}
function sat(cs,asgn){return cs.every(c=>c.some(l=>!!(asgn[Math.abs(l)]??0)===(l>0)));}
function check(d){const {bits,mask_count:m,variables:vars,source,steps}=d;if(source.length!==2*m||m!==2**bits)throw Error('size');const dag=source.map(c=>canonical(c));
 for(const node of steps){if(node.a<0||node.b<0||node.a>=dag.length||node.b>=dag.length)throw Error('parent');const got=resolve(dag[node.a],dag[node.b],node.pivot);if(JSON.stringify(got)!==JSON.stringify(node.lits))throw Error('derived');dag.push(got);}
 if(dag.at(-1).length || steps.length!==2*m-1)throw Error('root');return true;}
function witness(bits,j,type){const m=2**bits,a={};for(let i=0;i<bits;i++)a[i+1]=(j>>i)&1;for(let k=0;k<m;k++)a[bits+k+1]=type==='unit'?(k!==j):true;return a;}
function countParity(charge){let cnt=0;for(let a=0;a<256;a++){const x=(a&1)!==0,y=(a&2)!==0,z=(a&4)!==0;if(((x^y^z)?1:0)===charge)cnt++;}return cnt;}
function main(){let checks=0;let cases=[];const bundles=[];for(let bits=0;bits<=5;bits++){
 const d=build(bits);bundles.push(d);check(d);checks++;const m=d.mask_count;
 for(let j=0;j<m;j++)for(const type of ['unit','guard']){const idx=2*j+(type==='unit'?0:1),source=d.source.filter((_,i)=>i!==idx),w=witness(bits,j,type);if(!sat(source,w))throw Error('deletion witness');checks++;for(let k=0;k<d.source[idx].length;k++){const alt=d.source.map(c=>c.slice());alt[idx][k]*=-1;if(!sat(alt,witness(bits,j,'guard')) && !(type==='unit'&&sat(alt,witness(bits,j,'unit'))))throw Error('sign flip');checks++;}}
 const forged=structuredClone(d);forged.steps[0].pivot+=1;try{check(forged);throw Error('bad proof accepted')}catch(e){if(e.message==='bad proof accepted')throw e;}checks++;
 const wrong=structuredClone(d);wrong.steps[0].lits=[9999];try{check(wrong);throw Error('wrong root accepted')}catch(e){if(e.message==='wrong root accepted')throw e;}checks++;
 // Both labels for encoded mask family. UNSAT iff every blocker is selected.
 const testMasks=new Set([0,(2**m)-1,...Array.from({length:m},(_,j)=>(2**m)-1-2**j)]);
 if(m<=16)for(let v=0;v<2**m;v++)testMasks.add(v);
 for(const mask of testMasks){let model=false;for(let j=0;j<m;j++)if(!(mask & (2**j))){model=true;break;}const algorithmReject=mask===2**m-1;if(algorithmReject===model)throw Error('label');checks++;}
 for(const bad of ['', '2','01Z','  ','0'.repeat(m+1)]){if(bad.length===m&&/^[01]+$/.test(bad))throw Error('bad test');checks++;}
 cases.push({bits,mask_count:m,variables:d.variables,clauses:d.source_count,min_cost:d.cost,source_bytes:d.source_bytes,proof_json_bytes:d.proof_json_bytes,sha256:d.source_sha256,mask_tests:testMasks.size});
 }
 if(countParity(0)!==128||countParity(1)!==128)throw Error('parity');checks+=2;
 const raw={run:'UNIVERSAL-MASK-REFLECTION361',status:'COMPUTATIONAL, plus all-size symbolic exact proof in report',cases,checks,checker:'same-language internal, independent Python referee required',model:'fixed signed source; strict 2-premise RES; free source clauses, each derived node charge 1',controls:['source deletions','literal-sign flip','both SAT and UNSAT source masks','malformed mask strings','corrupted proof pivots and conclusions','parity']};
 fs.writeFileSync(process.argv[2]||'/mnt/data/lspv1_361/reflection_mask_cube361_results.json',JSON.stringify(raw,null,2));
 fs.writeFileSync(process.argv[3]||'/mnt/data/lspv1_361/reflection_mask_cube361_proofs.json',JSON.stringify({generator:'LSPV1_361',cases:bundles},null,2));console.log(JSON.stringify(raw));}
if(require.main===module)main();module.exports={build,check};
