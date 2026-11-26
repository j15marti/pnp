"use strict";
function audit(){
  const assert=(b,msg)=>{if(!b)throw Error(msg)};
  let seed=2611260302>>>0,checks=0; const ck=(b,msg)=>{checks++;assert(b,msg)};
  function rng(){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0}
  // Port order N,E,S,W; a table mask is 16 membership bits, bit w is word w.
  const N=8,E=4,S=2,W=1;
  const dec=t=>Number.isInteger(t)&&t>0&&t<=65535&&(t&(t-1))===0?31-Math.clz32(t):-1;
  function edges(k){let a=[];for(let r=0;r<k;r++)for(let c=0;c<k;c++){let u=r*k+c;if(c+1<k)a.push([u,u+1,E,W]);if(r+1<k)a.push([u,u+k,S,N]);}return a}
  function instance(k,bits){let e=edges(k),w=new Array(k*k).fill(0);for(let i=0;i<e.length;i++)if(bits(i)){let [u,v,a,b]=e[i];w[u]|=a;w[v]|=b}return w.map(x=>1<<x)}
  function reference(k,t){if(t.length!==k*k)return false;let w=t.map(dec);if(w.some(x=>x<0))return false;for(let r=0;r<k;r++)for(let c=0;c<k;c++){let x=w[r*k+c];if((r===0&&(x&N))||(r===k-1&&(x&S))||(c===0&&(x&W))||(c===k-1&&(x&E)))return false}return edges(k).every(([u,v,a,b])=>!!(w[u]&a)===!!(w[v]&b))}
  function stream(k,t,p,trace=false){if(t.length!==k*k)return {ok:false};let bad=false,reads=0,peak=0,states=trace?Array.from({length:k*k-1},()=>[]):null;
    for(let h=0;h<p;h++){let lo=Math.floor(h*k/p),hi=Math.floor((h+1)*k/p),buf=new Array(hi-lo).fill(0),east=0;peak=Math.max(peak,buf.length+2);
      for(let r=0;r<k;r++)for(let c=0;c<k;c++){let raw=dec(t[r*k+c]);reads++;if(raw<0)bad=true;let x=Math.max(0,raw);
        if(c===0)east=0;
        if(h===0){if(Number(!!(x&W))!==east)bad=true;if(c===k-1&&(x&E))bad=true}
        east=Number(!!(x&E));
        if(c>=lo&&c<hi){if(Number(!!(x&N))!==buf[c-lo])bad=true;buf[c-lo]=Number(!!(x&S));if(r===k-1&&buf[c-lo])bad=true}
        if(trace&&r*k+c<k*k-1)states[r*k+c].push(`${Number(bad)}${east}${buf.join("")}`);
      }
    }return {ok:!bad,reads,peak,states}}
  function twoOrder(k,t){if(t.length!==k*k)return {ok:false,reads:0};let reads=0,bad=false;for(let order=0;order<2;order++)for(let line=0;line<k;line++){let prior=0;for(let j=0;j<k;j++){let raw=dec(t[order?j*k+line:line*k+j]);reads++;if(raw<0)bad=true;let x=Math.max(0,raw);let incoming=order?N:W,outgoing=order?S:E;if(Number(!!(x&incoming))!==prior)bad=true;prior=Number(!!(x&outgoing));}if(prior)bad=true}return {ok:!bad,reads}}
  let exhaustive=0,yes=0,no=0,transcriptClasses=0,neighbors=0,scales=[];
  // Exhaust all 4 singleton words on 2x2, including inconsistent external flags.
  for(let m=0;m<65536;m++){let t=Array.from({length:4},(_,i)=>1<<((m>>>(4*i))&15)),a=reference(2,t);exhaustive++;a?yes++:no++;for(let p=1;p<=2;p++)ck(stream(2,t,p).ok===a,"exhaustive stream");ck(twoOrder(2,t).ok===a,"exhaustive two order")}
  for(let k of [2,3]){let e=edges(k),M=e.length;
    for(let p=1;p<=k;p++){let maps=Array.from({length:k*k-1},()=>new Map());for(let m=0;m<2**M;m++){let t=instance(k,i=>(m>>>i)&1),r=stream(k,t,p,true);ck(r.ok,"accepted trace");for(let j=1;j<k*k;j++){let pat=e.map(([u,v],i)=>u<j&&v>=j?String((m>>>i)&1):"").join(""),key=r.states[j-1].join("|"),map=maps[j-1];if(map.has(key))ck(map.get(key)===pat,"transcript collision");else map.set(key,pat)}}transcriptClasses+=maps.reduce((a,m)=>a+m.size,0)}
  }
  for(let k of [4,8,16,32,64,128]){let e=edges(k),a=Math.ceil(k*k/3),b=Math.floor(2*k*k/3),total=0,min=Infinity,counts=new Array(k*k).fill(0);let groups=Array.from({length:k},()=>new Set());
    for(let i=0;i<e.length;i++){let [u,v]=e[i];for(let j=Math.max(a,u+1);j<=Math.min(b,v);j++){counts[j]++;let s=groups[j%k];ck(!s.has(i),"residue overlap");s.add(i)}}
    for(let j=a;j<=b;j++){min=Math.min(min,counts[j]);total+=counts[j]}ck(min>=k,"balanced prefix");ck(total===groups.reduce((x,s)=>x+s.size,0),"union tariff");
    let jobs=0;for(let rep=0;rep<4;rep++){let t=instance(k,()=>rng()&1);let [u,v,a,b]=e[rng()%e.length];let z=t.slice();z[u]=1<<(dec(z[u])^a);for(let [x,expect] of [[t,true],[z,false]]){ck(reference(k,x)===expect,"source");let q=twoOrder(k,x);ck(q.ok===expect&&q.reads===2*k*k,"two order");for(let p of new Set([1,2,Math.min(4,k),k])){let r=stream(k,x,p);ck(r.ok===expect&&r.reads===p*k*k&&r.peak<=Math.ceil(k/p)+2,"stream");jobs++}neighbors++}}
    let t=instance(k,()=>rng()&1);t[0]=3;ck(!stream(k,t,1).ok&&!twoOrder(k,t).ok&&!reference(k,t),"malformed nonsingleton");scales.push({k,table_bits:16*k*k,balanced_cuts:b-a+1,min_crossing:min,total_crossing:total,stream_jobs:jobs,two_order_reads:2*k*k})
  }
  return {seed:2611260302,checks,exhaustive_2x2:exhaustive,yes_2x2:yes,no_2x2:no,transcript_classes:transcriptClasses,large_label_jobs:neighbors,scales}
}
console.log(JSON.stringify(audit(),null,2));
