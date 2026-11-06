// LSPV-2/436 compact finite check. This is NOT an FLMV Turing-machine replay.
import assert from 'node:assert/strict';
function cubes(){
  const k4=[];for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)k4.push([a,b]);
  const cube=[];for(let a=0;a<8;a++)for(let b=a+1;b<8;b++)if([1,2,4].includes(a^b))cube.push([a,b]);
  return [[4,k4],[8,cube]];
}
function clauses(H,edges,chi){
  const out=[];
  for(let v=0;v<H;v++){
    const e=edges.map(([a,b],i)=>a==v||b==v?i:-1).filter(i=>i>=0);
    assert.equal(e.length,3);
    for(let a=0;a<2;a++)for(let b=0;b<2;b++)out.push([[e[0],a],[e[1],b],[e[2],a^b^1^chi[v]]]);
  }
  return out;
}
let checks=0;
for(const [H,E] of cubes()){
 const base=Array.from({length:H},(_,i)=>i%2),B=clauses(H,E,base);
 for(let r=0;r<=4;r++)for(let code=0;code<H**r;code++){
   const edits=[];let t=code;
   for(let j=0;j<r;j++){edits.push(t%H);t=Math.floor(t/H);}
   const chi=base.slice();for(const v of edits)chi[v]^=1;
   const C=clauses(H,E,chi);
   for(let ci=0;ci<4*H;ci++)for(let k=0;k<3;k++){
      const flip=k===2 ? (edits.filter(v=>v===Math.floor(ci/4)).length&1) : 0;
      assert.equal(C[ci][k][0],B[ci][k][0]);checks++;
      assert.equal(C[ci][k][1],B[ci][k][1]^flip);checks++;
   }
   assert.equal((chi.reduce((a,b)=>a+b,0)&1),((base.reduce((a,b)=>a+b,0)+r)&1));checks++;
 }
}
for(let r=1;r<=50;r++){
 const u=Array(r).fill(1);
 for(let j=0;j<r;j++){const x=u.slice();x[j]=0;assert.notEqual(x.filter(v=>v===0).length%2,u.filter(v=>v===0).length%2);checks++;}
}
console.log(JSON.stringify({status:'finite control only',checks,all_pass:true}));
