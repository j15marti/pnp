"use strict";
console.log(JSON.stringify((function study(){
"use strict";
const REV="TMR2_CANCEL_CERT064_v1",SEED=20261116;let seed=SEED>>>0,cases=0,exhaustive=0,rejects=0,characters=0;
function rand(){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return(seed>>>0)/4294967296;}
function ok(p,m){if(!p)throw Error(m);}
function num(s){ok(/^(0|[1-9]\d*)$/.test(s),"number");let n=Number(s);ok(Number.isSafeInteger(n),"unsafe number");return n;}
function bit(z,i){return(z>>BigInt(i))&1n;}
function toggle(S,x){if(S.has(x))S.delete(x);else S.add(x);}
function xor(A,B){let C=new Set(A);for(let x of B)toggle(C,x);return C;}
function prod(A,B){let C=new Set();for(let x of A)for(let y of B)toggle(C,x|y);return C;}
function pc(z){let n=0;while(z){z&=z-1n;n++;}return n;}
function parse(src){
 ok(typeof src==="string"&&/^[\x0A\x20-\x7E]+$/.test(src)&&src.endsWith("\n"),"ASCII LF");
 let lines=src.slice(0,-1).split("\n"),h=lines.shift().split(" ");
 ok(h.length===7&&h[0]==="p"&&h[1]==="d2poly","header");
 let[n,a,b,g,root]=h.slice(2).map(num);
 ok(a>=1&&b>=1&&n===a+b&&g>=1&&n<=2*g&&g<=src.length&&root<g&&lines.length===g,"header bounds");
 let r=new Array(g);
 for(let line of lines){
  ok(line&&line===line.trim()&&!line.includes("  "),"line");
  let t=line.split(" "),op=t[0];ok({I:3,N:3,A:4,O:4,P:4}[op]===t.length,"d0 opcode/arity");
  let id=num(t[1]),a=t.slice(2).map(num);ok(id<g&&!r[id],"id");
  if(op==="I")ok(a[0]<n,"input ref");else ok(a.every(x=>x<g),"wire");
  r[id]={op,a};
 }
 ok(r.every(Boolean),"missing ids");
 let order=[],state=new Uint8Array(g),used=new Set();
 function visit(i){ok(state[i]!==1,"cycle");if(state[i]===2)return;state[i]=1;
  let q=r[i];if(q.op==="I")used.add(q.a[0]);else for(let c of q.a)visit(c);
  state[i]=2;order.push(i);
 }
 visit(root);ok(order.length===g&&used.size===n,"reachability/input coverage");
 return{n,g,root,r,order,N:src.length};
}
function normal(s){
 let nodes=[],cache=new Map(),v=Array(s.g),attempts=0;
 function atom(key,entry){let id=cache.get(key);if(id===undefined){id=nodes.length;cache.set(key,id);nodes.push(entry);}return 1n<<BigInt(id+1);}
 function degree(vec){let d=0,j=0,z=vec>>1n;while(z){if(z&1n)d=Math.max(d,nodes[j].d);j++;z>>=1n;}return d;}
 function and(x,y){attempts++;if(!x||!y)return 0n;if(x===1n)return y;if(y===1n)return x;if(x===y)return x;if((x^y)===1n)return 0n;
  if(x>y)[x,y]=[y,x];return atom("A"+x.toString(16)+"/"+y.toString(16),{op:"A",x,y,d:Math.min(3,degree(x)+degree(y))});
 }
 for(let id of s.order){
  let{op,a}=s.r[id];if(op==="I")v[id]=atom("I"+a[0],{op:"I",index:a[0],d:1});
  else if(op==="N")v[id]=v[a[0]]^1n;
  else if(op==="P")v[id]=v[a[0]]^v[a[1]];
  else if(op==="A")v[id]=and(v[a[0]],v[a[1]]);
  else if(op==="O")v[id]=v[a[0]]^v[a[1]]^and(v[a[0]],v[a[1]]);
 }
 let root=v[s.root],d=degree(root),active=new Set();
 function visit(z){let j=0,w=z>>1n;while(w){if((w&1n)&&!active.has(j)){active.add(j);if(nodes[j].op==="A"){visit(nodes[j].x);visit(nodes[j].y);}}w>>=1n;j++;}}
 visit(root);let keep=[...active].sort((a,b)=>a-b);
 ok(keep.every(j=>nodes[j].d<=d),"cert monotone");
 return{nodes,root,d,keep,attempts,eliminated:nodes.length-keep.length};
}
function poly(s,f){
 ok(f.d<=2,"degree>2 after normalization");
 let P=new Array(f.nodes.length);
 function value(z){let out=(z&1n)?new Set([0n]):new Set(),j=0,w=z>>1n;while(w){if(w&1n)out=xor(out,P[j]);w>>=1n;j++;}return out;}
 for(let id of f.keep){let q=f.nodes[id];P[id]=q.op==="I"?new Set([1n<<BigInt(q.index)]):prod(value(q.x),value(q.y));
  ok([...P[id]].every(x=>pc(x)<=2),"polynomial out of range");
 }return value(f.root);
}
function H(poly,n){characters++;let P=new Set(poly),pairs=0;
 while(true){
  let edge=null;for(let m of P)if(pc(m)===2){edge=m;break;}
  if(edge===null){if([...P].some(x=>pc(x)===1))return 0n;return(P.has(0n)?-1n:1n)*(1n<<BigInt(n-pairs));}
  let i=-1,j=-1;for(let k=0;k<n;k++)if(bit(edge,k)){if(i<0)i=k;else{j=k;break;}}
  let bi=1n<<BigInt(i),bj=1n<<BigInt(j),A=new Set(),B=new Set(),R=new Set();
  for(let m of P){if(m&bi){if(m&bj){ok(m===edge,"quadratic pair");continue;}toggle(A,m^bi);}else if(m&bj)toggle(B,m^bj);else toggle(R,m);}
  P=xor(R,prod(A,B));pairs++;ok(pairs<=n/2,"pair limit");
 }
}
function count(text){let s=parse(text),f=normal(s),p=poly(s,f),h=H(p,s.n),total=1n<<BigInt(s.n);ok((total-h)%2n===0n,"parity");let c=(total-h)/2n;ok(c>=0n&&c<=total,"count range");
 return{answer:c.toString(),n:s.n,g:s.g,N:s.N,degree:f.d,atoms:f.nodes.length,active:f.keep.length,eliminated:f.eliminated};
}
function direct(s,z){let vals=Array(s.g);for(let id of s.order){let{op,a}=s.r[id];if(op==="I")vals[id]=bit(z,a[0])===1n;else if(op==="N")vals[id]=!vals[a[0]];else if(op==="A")vals[id]=vals[a[0]]&&vals[a[1]];else if(op==="O")vals[id]=vals[a[0]]||vals[a[1]];else vals[id]=vals[a[0]]!==vals[a[1]];}return vals[s.root];}
function brute(s){let v=0n;for(let z=0n;z<(1n<<BigInt(s.n));z++)if(direct(s,z))v++;return v;}
function build(n,fn){let rec=[];function add(op,...a){let id=rec.length;rec.push([op,id,...a].join(" "));return id;}let root=fn(add),g=rec.length,ord=Array.from({length:g},(_,i)=>i);
 for(let i=g-1;i>0;i--){let j=Math.floor(rand()*(i+1));[ord[i],ord[j]]=[ord[j],ord[i]];}
 let a=Math.floor(n/2);return `p d2poly ${n} ${a} ${n-a} ${g} ${root}\n`+ord.map(i=>rec[i]).join("\n")+"\n";
}
function heavy(n,duplicate){return build(n,add=>{let I=Array.from({length:n},(_,i)=>add("I",i));
 let h=add("A",I[0],I[1]);for(let i=2;i<n;i++)h=add("A",h,I[i]);
 let k=h;if(duplicate){k=add("A",I[0],I[1]);for(let i=2;i<n;i++)k=add("A",k,I[i]);}
 let q=add("A",I[0],I[n-1]);return add("P",add("P",h,k),q);
});}
function check(src,expected=null){let out=count(src),s=parse(src);if(s.n<=10){ok(BigInt(out.answer)===brute(s),"exhaustive count discrepancy");exhaustive++;}
 if(expected!==null)ok(BigInt(out.answer)===BigInt(expected),"expected count");cases++;return out;}
let examples=[];
examples.push({name:"shared_cubic",...check(heavy(6,false))});
examples.push({name:"distinct_duplicate_cubic",...check(heavy(8,true))});
for(let i=0;i<80;i++){let n=5+i%5,r=check(heavy(n,i%2===0));if(i<2)examples.push({name:"random_regression",...r});}
let extra=build(8,add=>{let I=Array.from({length:8},(_,i)=>add("I",i)),h=add("A",add("A",I[0],I[1]),I[2]);
 let high=add("O",h,add("A",h,I[3])),bad=add("P",high,high),low=add("P",add("A",I[4],I[5]),add("A",I[6],I[7]));
 return add("P",bad,low);
});examples.push({name:"OR_HIGH_CANCEL",...check(extra)});
examples.push({name:"large64",...check(heavy(64,true))});
let cubic=build(4,add=>{let I=Array.from({length:4},(_,i)=>add("I",i));return add("A",add("A",I[0],I[1]),add("A",I[2],I[3]));});
try{count(cubic);throw Error("wrongly accepted high degree");}catch(e){ok(String(e).includes("degree>2"),"high degree rejection");rejects++;}
try{parse(cubic.replace("p d2poly","p d3poly"));throw Error("wrongly accepted header");}catch(e){ok(String(e).includes("header"),"bad header");rejects++;}
let unsat=build(6,add=>{let I=Array.from({length:6},(_,i)=>add("I",i)),bad=add("A",I[0],add("N",I[0]));
 let other=add("A",add("A",I[3],I[4]),I[5]);return add("A",bad,add("A",other,add("P",I[1],I[2])));});
examples.push({name:"unsat_complement",...check(unsat,0)});
function derivative(s,vars,context){let v=0;for(let mask=0;mask<8;mask++){let z=context;for(let j=0;j<3;j++)if(mask>>j&1)z^=1n<<BigInt(vars[j]);v^=Number(direct(s,z));}return v;}
ok(derivative(parse(cubic),[0,1,2],8n)===1,"positive derivative");
ok(derivative(parse(unsat),[3,4,5],0n)===0,"negative derivative");
return {revision:REV,seed:SEED,cases,exhaustive,rejects,characters,failures:0,examples};
})(),null,2));
