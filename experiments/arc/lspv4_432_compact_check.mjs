// LSPV-4/432 compact independent finite control, Node.js. Not a native FLMV machine.
// Complete Python producer and independent SHA/checker are in the run's reproducibility ZIP.
import assert from 'node:assert/strict';

function graphs() {
  const k4 = [];
  for (let u=0;u<4;u++) for (let v=u+1;v<4;v++) k4.push([u,v]);
  const cube = [];
  for (let u=0;u<8;u++) for (let v=u+1;v<8;v++) {
    const t=u^v; if((t&(t-1))===0)cube.push([u,v]);
  }
  const e = new Map();
  const add=(u,v)=>{let a=Math.min(u,v),b=Math.max(u,v);e.set(a+','+b,[a,b]);};
  for(let i=0;i<5;i++){add(i,(i+1)%5);add(5+i,5+(i+2)%5);add(i,5+i);}
  return [['K4',4,k4],['Cube',8,cube],['Petersen',10,[...e.values()].sort((x,y)=>x[0]-y[0]||x[1]-y[1])]];
}
function enc(h,edges,charge) {
  const m=edges.length,w=Math.max(1,Math.floor(Math.log2(m))+1);
  const slots=Array.from({length:h},()=>[]);
  edges.forEach(([u,v],i)=>{slots[u].push(i);slots[v].push(i)});
  assert.ok(slots.every(z=>z.length===3));
  let s='10100111'+'1'.repeat(h)+'0'+'1'.repeat(m)+'0';
  for(const [u,v] of edges)s+=u.toString(2).padStart(w,'0')+v.toString(2).padStart(w,'0');
  let piv=[];
  for(let v=0;v<h;v++){
    const [a,b,c]=slots[v].sort((x,y)=>x-y);let d=[];
    for(const p of [0,1])for(const q of [0,1]){
      const parts=[[p,a],[q,b],[p^q^1^charge[v],c]];
      parts.forEach(([sg,e],j)=>{
        if(j===2)d.push(s.length);
        s+=sg+e.toString(2).padStart(w,'0');
      });
    }
    piv.push(d);
  }
  return [s+'00',piv];
}
let checks=0,groups=[];
for(const [name,h,edges] of graphs()){
  const m=edges.length;
  const zero=new Array(h).fill(0);
  const [base,piv]=enc(h,edges,zero);
  const N=base.length;
  for(let bits=0;bits<2**h;bits++){
    const charge=Array.from({length:h},(_,i)=>(bits>>i)&1);
    const [src,p]=enc(h,edges,charge);
    assert.equal(src.length,N);checks++;
    for(let v=0;v<h;v++){
      const cp=charge.slice();cp[v]^=1;
      const [changed,p2]=enc(h,edges,cp);
      const diff=[];
      for(let i=0;i<src.length;i++)if(src[i]!==changed[i])diff.push(i);
      assert.deepEqual(diff,p[v]);assert.deepEqual(p[v],p2[v]);checks+=2;
      assert.equal(charge.reduce((a,b)=>a^b,0),1^cp.reduce((a,b)=>a^b,0));checks++;
    }
  }
  const q=2*h+5;
  for(const baseparity of [0,1]){
    const chi=[baseparity,...new Array(h-1).fill(0)];
    const [source,positions]=enc(h,edges,chi);
    for(let k=0;k<q;k++){
      const v=(3*k+1)%h;
      const child=source.split('');
      for(const p of positions[v]) child[p]=child[p]==='1'?'0':'1';
      const cc=chi.slice();cc[v]^=1;
      assert.equal(child.join(''),enc(h,edges,cc)[0]);checks++;
    }
  }
  groups.push({graph:name,H:h,N,q,raw_lower:q*h,delta_read_symbols:h+q});
}
console.log(JSON.stringify({checks,groups},null,2));
