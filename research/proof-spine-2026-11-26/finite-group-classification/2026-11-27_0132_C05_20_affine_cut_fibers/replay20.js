// C05-20 independent BigInt replay; no Python, matching, or planarity library.
const C = [[1,0,0,1],[2,0,0,2],[5,0,1,2],[8,1,0,2],[9,1,1,0],[13,2,2,1],[14,2,2,3],[17,2,3,3],[20,3,2,3],[21,3,3,0]];
function assert(b,m){if(!b)throw Error(m||"assertion failed")}
function mask(t,n){return (1n<<BigInt(t[1]))|(1n<<BigInt(n+t[2]))|(1n<<BigInt(2*n+t[3]))}
function piv(x){return x.toString(2).length-1}
function add(B,x){while(x){let i=piv(x);if(B.has(i))x^=B.get(i);else{B.set(i,x);return}}}
function span(B,x){while(x){let i=piv(x);if(!B.has(i))return false;x^=B.get(i)}return true}
function rank(A){let B=new Map;for(let a of A)add(B,a);return B.size}
function brute(A,target){let count=0,aff=0;function visit(i,s,x,ok){if(i===A.length){if(x===target)aff++;if(ok&&s===target)count++;return}visit(i+1,s,x,ok);visit(i+1,s|A[i],x^A[i],ok&&!(s&A[i]))}visit(0,0n,0n,true);return {count,aff}}
function build(k,l){
 let T=new Map(C.map(t=>[t[0],t.slice()]));let idx=(j,s)=>100+2*j+s;let counter=[4,4,4];let A=[],B=[];
 for(let j=0;j<2*k;j++)for(let s=0;s<2;s++){let id=idx(j,s);T.set(id,[id,-1,-1,-1]);((j+s)%2?B:A).push(id)}
 for(let s=0;s<2;s++)for(let j=0;j<2*k;j++){let c=j%2,z=counter[c]++;T.get(idx(j,s))[1+c]=z;T.get(idx((j+1)%(2*k),s))[1+c]=z}
 for(let j=0;j<2*k;j++){let z=counter[2]++;T.get(idx(j,0))[3]=z;T.get(idx(j,1))[3]=z}
 function swap(u,v){[T.get(u)[3],T.get(v)[3]]=[T.get(v)[3],T.get(u)[3]]}
 swap(1,100);let base=4+2*k,last=200+4*k;let extra=[];
 for(let a=0;a<l;a++){for(let b=0;b<8;b++){let id=last+8*a+b;T.set(id,[id,base+2*a+(b>>2),base+2*a+((b>>1)&1),base+2*a+(b&1)])}
 swap(a===0?102:last+8*(a-1)+(a%2?7:0),last+8*a+(a%2?7:0))}
 for(let a=l-1;a>=0;a--)for(let b=0;b<8;b++)extra.push(last+8*a+b)
 let order=[...extra,...A,...B,...C.map(t=>t[0])],n=base+2*l;
 return {T,order,n,cut:extra.length+A.length,base,last}
}
function replay(T,order,n,mode,cap=64){
 let cols=order.map(i=>mask(T.get(i),n)),m=cols.length,target=(1n<<BigInt(3*n))-1n;
 let suf=Array(m+1),U=Array(m+1);suf[m]=new Map;U[m]=0n;
 for(let j=m-1;j>=0;j--){suf[j]=new Map(suf[j+1]);add(suf[j],cols[j]);U[j]=U[j+1]|cols[j]}
 let B=new Map,ws=[],seams=[],pre=0n,states=new Map([[0n,1n]]),peak=1,attempt=0,status=null;
 function pop(x){let z=0;while(x){x&=x-1n;z++}return z}
 for(let j=0;j<=m;j++){
 if(j){add(B,cols[j-1]);pre|=cols[j-1]}
 let w=B.size+suf[j].size-suf[0].size;ws.push(w);seams.push(pop(pre&U[j]));
 if(!j||status!==null)continue;
 let next=new Map,v=cols[j-1];
 for(let [s,c] of states){for(let z of ((s&v)?[s]:[s,s|v])){
 attempt++;if((target^z)&~U[j])continue;
 if(mode==="rank"&&!span(suf[j],target^z))continue;
 next.set(z,(next.get(z)||0n)+c);
 if(next.size>cap){status="UNKNOWN";break}
 }if(status)break}
 states=next;peak=Math.max(peak,next.size);
 if(mode==="rank")assert(next.size<=2**w,"cut cardinality");
 if(!next.size)status="NO";
 }
 if(status===null)status=states.has(target)?"YES":"NO";
 return {status,peak,attempt,ws,seams,nullity:m-suf[0].size,count:status==="UNKNOWN"?null:Number(states.get(target)||0n)}
}
function main(){
 const core=C.map(t=>mask(t,4)),c=brute(core,4095n);assert(c.count===0&&c.aff===2,"core");assert(rank(core)===9);
 let rows=[];for(let k of [2,4,8,16,32,64]){
 let {T,order,n,cut,base,last}=build(k,k);let m=T.size;
 assert(new Set(order).size===m);
 let R=replay(T,order,n,"rank"),D=replay(T,order,n,"raw");
 assert(R.status==="NO"&&R.peak===7&&Math.max(...R.ws)===4&&R.nullity===1+3*k);
 assert(R.ws[cut]===1&&R.seams[cut]===6*k);
 assert(D.status===(k===2?"NO":"UNKNOWN"));
 for(let a=-1;a<k;a++){
 let ids=new Set(C.map(t=>t[0]));if(a>=0){for(let id of T.keys())if(id>=100&&id<100+4*k)ids.add(id);for(let b=0;b<a;b++)for(let j=0;j<8;j++)ids.add(last+8*b+j)}
 let end=a<0?4:base+2*a;let x=0,y=0;for(let [i,t] of T){if(ids.has(i)&&t[3]>=end)x++;if(!ids.has(i)&&t[3]<end)y++}assert(x===1&&y===1,"seam")
 }
 rows.push({k,m,nullity:R.nullity,width:Math.max(...R.ws),crossing:R.seams[cut],cutRank:R.ws[cut],rankPeak:R.peak,rankAttempts:R.attempt,raw:D.status,rawPeak:D.peak});
 }
 let controls=0;
 let cube=Array.from({length:8},(_,i)=>[i,i>>2,(i>>1)&1,i&1]);
 for(let b=0;b<256;b++){let T=new Map(cube.filter(t=>b>>t[0]&1).map(t=>[t[0],t]));let A=[...T.values()].map(t=>mask(t,2));let ref=brute(A,63n).count;for(let mode of ["raw","rank"]){let r=replay(T,[...T.keys()],2,mode);assert(r.count===ref,"cube count");controls++}}
 return {core:c,rows,controls};
}
const result=main();
if(typeof console!=="undefined")console.log(JSON.stringify(result,null,2));