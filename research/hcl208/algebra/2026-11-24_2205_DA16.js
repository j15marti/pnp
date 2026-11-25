// Run: node 2026-11-24_2205_DA16.js
const main = function(){
  const pc=(x)=>{let a=0;while(x){x&=x-1;a++}return a};
  const bit=k=>1n<<BigInt(k);
  const top=p=>p.toString(2).length-1;
  const times=(a,b,n)=>{let p=0n;for(let i=0;i<(1<<n);i++)if(a&bit(i))for(let j=0;j<(1<<n);j++)if(b&bit(j))p^=bit(i|j);return p};
  const linear=(mask,rhs,n)=>{let p=BigInt(rhs);for(let j=0;j<n;j++)if(mask&(1<<j))p^=bit(1<<j);return p};
  const nae=(t,s,n)=>times(linear((1<<t[0])^(1<<t[1]),1^((s>>0&1)^(s>>1&1)),n),linear((1<<t[0])^(1<<t[2]),1^((s>>0&1)^(s>>2&1)),n),n);
  const ind=(t,w,n)=>t.reduce((p,v,j)=>times(p,linear(1<<v,1^(w>>j&1),n),n),1n);
  const evalp=(p,x,n)=>{let b=0;for(let m=x;;m=(m-1)&x){if(p&bit(m))b^=1;if(!m)break}return b};
  const parity=x=>pc(x)&1;
  let checks=0,scans=0,forced=0,insertions=0,rounds=0,products=0;
  const check=(x,msg)=>{checks++;if(!x)throw Error(msg)};
  const all=n=>Array.from({length:1<<n},(_,i)=>i);
  function closure(n,polys,guards){
    let a=all(n).filter(x=>guards.every(([m,b])=>parity(x&m)===b));
    const original=a.filter(x=>polys.every(p=>!evalp(p,x,n)));
    while(a.length){
      scans++;let changed=false;
      for(const p of polys){
        const s=a.filter(x=>!evalp(p,x,n));
        if(!s.length){a=[];changed=true;break}
        const h=[0];let set=new Set(h);
        for(const x of s){let d=x^s[0];if(!set.has(d)){const extra=h.map(y=>y^d);h.push(...extra);set=new Set(h)}}
        const next=a.filter(x=>set.has(x^s[0]));
        if(next.length<a.length){forced++;a=next;changed=true;break}
      }
      if(!changed)break;
    }
    check(original.every(x=>a.includes(x)),"unsound singleton hull");
    return a.length;
  }
  function calc(n,polys,d,guards=[]){
    const N=1<<n;let allowed=0n;const contains=Array(n).fill(0n);
    for(let m=0;m<N;m++){if(pc(m)<=d)allowed|=bit(m);for(let j=0;j<n;j++)if(m&(1<<j))contains[j]|=bit(m)}
    let basis=Array(N).fill(0n),changed=false;
    function insert(p){while(p){const h=top(p);if(basis[h])p^=basis[h];else{basis[h]=p;insertions++;changed=true;return}}}
    for(const p of [...polys,...guards.map(([m,b])=>linear(m,b,n))]){if(p&~allowed)throw Error("degree cap below axiom");insert(p)}
    if(basis[0])return {unsat:true,rank:basis.filter(Boolean).length};
    do{
      changed=false;rounds++;
      for(let j=0;j<n;j++){
        let hi=Array(N).fill(0n);
        for(const p of basis.filter(Boolean)){
          products++;
          let q=(p&contains[j])^((p&~contains[j])<<BigInt(1<<j));
          while(q&~allowed){let k=top(q&~allowed);if(hi[k])q^=hi[k];else{hi[k]=q;break}}
          if(!(q&~allowed))insert(q);
          if(basis[0])return {unsat:true,rank:basis.filter(Boolean).length};
        }
      }
    }while(changed);
    return {unsat:false,rank:basis.filter(Boolean).length};
  }
  const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
  const plane=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,7],[1,5,6],[2,3,8]];
  // Use actual four perfect partitions of affine plane F3^2, not the illustrative incomplete array above.
  const ap=[];for(let j=0;j<3;j++)ap.push([3*j,3*j+1,3*j+2]);for(let a=0;a<3;a++)for(let b=0;b<3;b++)ap.push([0,1,2].map(x=>3*x+(a*x+b)%3));
  const results={cases:[],guarded:{},compiler:0};
  function run(name,n,polys,degrees,expect,guard=[]){
    const cnt=all(n).filter(x=>guard.every(([m,b])=>parity(x&m)===b)&&polys.every(p=>!evalp(p,x,n))).length;
    check(cnt===expect,name+" count");
    const ambient=closure(n,polys,guard);
    const r=degrees.map(d=>({d,...calc(n,polys,d,guard)}));
    check(!cnt||r.every(z=>!z.unsat),name+" false rejection");
    results.cases.push({name,n,models:cnt,closureWords:ambient,degree:r});
    return r;
  }
  const F=fano.map(t=>nae(t,0,7));
  const f=run("Fano",7,F,[2,3,4],0);
  for(let i=0;i<7;i++)for(let s=1;s<=3;s++){const p=F.slice();p[i]=nae(fano[i],s,7);run("Fano sign "+i+":"+s,7,p,[2,3],10)}
  for(let i=0;i<7;i++)for(const w of [0,7]){const p=F.slice();p[i]=ind(fano[i],w,7);run("Fano budget "+i+":"+w,7,p,[3],5)}
  run("Affine plane four partitions",9,ap.map(t=>nae(t,0,9)),[2,3,4],0);
  // Test case-discharge bound using all relative one-bit guards and actual degree-limited closures.
  for(let m=1;m<128;m++)if(parity(m)===0){
    const pair=[0,1].map(b=>{closure(7,F,[[m,b]]);return calc(7,F,2,[[m,b]]).unsat});
    const key=pair.filter(Boolean).length;results.guarded[key]=(results.guarded[key]||0)+1;
    if(key===2)check(f.find(z=>z.d===3).unsat,"case discharge bound");
  }
  // Clause-local substitution: y=(1+l1)(1+l2), z=0.
  for(let sign=0;sign<8;sign++)for(let x=0;x<8;x++){
    const l=[0,1,2].map(j=>(x>>j&1)^(sign>>j&1));const y=(1^l[0])&(1^l[1]);
    const bad=(a,b,c)=>Number(a===b&&b===c);
    check(bad(l[0],l[1],y)===0,"first gadget");
    check(bad(1^y,l[2],0)===((1^l[0])&(1^l[1])&(1^l[2])),"second gadget");
    results.compiler++;
  }
  // Switched Fano equality gadget, zero and one are legal, deleted terminals equal.
  let legal=0;
  const switchWord=0b1111000;
  for(let x=0;x<128;x++){const v=x^switchWord;const ok=fano.slice(1).every(t=>{const a=t.map(j=>v>>j&1);return !(a[0]===a[1]&&a[1]===a[2])});if(ok){legal++;check((x&7)===0||(x&7)===7,"equality gadget")};if(x===0||x===127)check(ok,"constant lift")}
  results.equalityModels=legal;
  results.ledger={checks,scans,forced,insertions,rounds,products};
  return results;
};
console.log(JSON.stringify(main(),null,2));
