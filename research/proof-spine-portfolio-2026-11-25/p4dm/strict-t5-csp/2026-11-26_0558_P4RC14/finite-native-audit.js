/* Standalone exact local rotation and 48-tuple source boundary verifier. Run: node finite-native-audit.js */
const T=[[0,3,2,0],[2,0,1,2],[15,3,0,1],[3,2,1,2],[0,1,2,3],[2,2,0,2],[0,1,3,0],[1,1,3,3],[3,2,0,1],[2,5,2,3],[1,3,3,0],[3,0,1,1],[4,4,4,5],[5,4,5,5],[7,5,5,5],[5,5,5,4],[4,0,4,4],[5,4,4,4],[7,6,6,7],[6,6,7,7],[9,6,7,6],[6,7,6,7],[1,7,6,6],[6,7,7,6],[8,11,10,8],[10,8,9,10],[15,11,8,9],[11,10,9,10],[8,9,10,11],[10,10,8,10],[8,9,11,8],[9,9,11,11],[11,10,8,9],[10,13,10,11],[9,11,11,8],[11,8,9,9],[12,12,12,13],[13,12,13,13],[7,13,13,13],[13,13,13,12],[12,8,12,12],[13,12,12,12],[15,14,14,15],[14,14,15,15],[12,14,15,14],[14,15,14,15],[4,15,14,14],[14,15,15,14]];
function assert(x,m){if(!x)throw Error(m)}
function words(d){return Array.from({length:2**d},(_,i)=>Array.from({length:d},(_,j)=>(i>>j)&1))}
function perms(a){return a.length?a.flatMap((x,i)=>perms(a.filter((_,j)=>i!==j)).map(p=>[x,...p])):[[]]}
function dot(a,b){return a.reduce((s,x,i)=>s+x*b[i],0)}
function meet(W,s){const d=s.length,O=W.map(w=>Array.from({length:d},(_,j)=>dot(w.slice(0,j),s.slice(0,j)))),S=new Set(O.map(x=>x.join(',')));for(const a of O)for(const b of O)for(let t=-2*d;t<=2*d;t++){const z=a.map((x,i)=>Math.min(x,b[i]+t));if(!S.has(z.map(x=>x-z[0]).join(',')))return false}return true}
function audit(){
 let counts=[],fails=0;
 for(let d=1;d<=4;d++){let n=0;for(const signs of words(d).map(x=>x.map(y=>2*y-1))){const ws=words(d);for(const c of new Set(ws.map(w=>dot(w,signs)))){const L=ws.filter(w=>dot(w,signs)===c);for(let z=1;z<2**L.length;z++){const W=L.filter((_,j)=>(z>>j)&1);n++;if(!meet(W,signs))fails++;assert(perms(Array.from({length:d},(_,i)=>i)).some(p=>meet(W.map(w=>p.map(i=>w[i])),p.map(i=>signs[i]))),'local rotation failure')}}}counts.push(n)}
 assert(counts.join(',')==='4,20,128,1520'&&fails===240,'unexpected counts');
 const rows=Array.from({length:64},(_,i)=>T.map((t,j)=>t[Math.floor(i/16)]===i%16?j:-1).filter(j=>j>=0));assert(new Set(T.map(t=>t.join(','))).size===48&&rows.every(r=>r.length===3),'native encoding');
 const ports=[44,46,2,26];
 function local(which,w){const ids=Array.from({length:48},(_,i)=>i).filter(i=>which===0?i<42:i>=42),rs=rows.filter((_,i)=>which===0?i%16<14:i%16>=14),a=Array(48).fill(-1);ports.forEach((j,i)=>a[j]=w[i]);function rec(q){for(;;){let change=false;for(const r of rs){const one=r.filter(j=>q[j]===1).length,free=r.filter(j=>q[j]===-1);if(one>1||one+free.length<1)return null;if(one===1)for(const j of free){q[j]=0;change=true}else if(free.length===1){q[free[0]]=1;change=true}}if(!change)break}const j=ids.find(j=>q[j]===-1);if(j===undefined)return ids.filter(j=>q[j]===1);for(const x of [0,1]){const p=q.slice();p[j]=x;const s=rec(p);if(s)return s}return null}return rec(a)}
 const L=[],R=[],lifts=[];for(const w of words(4)){const a=local(0,w),b=local(1,w);if(a)L.push(w.join(''));if(b)R.push(w.join(''));if(a&&b){const s=new Set([...a,...b]);assert(rows.every(r=>r.filter(j=>s.has(j)).length===1),'lift');lifts.push(w.join(''))}}
 assert(L.sort().join(',')==='0000,0101,1010','inside support');assert(R.sort().join(',')==='0000,0101,0110,1001,1010','outside support');assert(lifts.sort().join(',')===L.join(','),'global support');assert(!local(0,[0,0,0,1]),'guard negative');
 return {signedCases:counts,initialFailures:fails,postRotationFailures:0,nativeTupleCount:T.length,nativeSupport:L,complementSupport:R,verifiedGlobalSupport:lifts,guardedNegative:true,planarityAndConnectivity:'verified in Python, not by this JS checker'}
}
console.log(JSON.stringify(audit(),null,2));
