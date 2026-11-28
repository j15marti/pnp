function audit(z){
 const C=z.C,owners=z.owners,m=Math.max(...owners)+1,A=(1n<<BigInt(m))-1n,rows=C.map((c,i)=>({c,mask:1n<<BigInt(owners[i])}));let reads=0,words=0;
 function check(c,ps){let S=new Set(c.map(l=>-l));for(;;){let change=false;for(let {c} of ps){let q=[];let sat=false;for(let l of c){reads++;if(S.has(l)){sat=true;break}if(!S.has(-l))q.push(l)}if(sat)continue;if(!q.length)return true;if(q.length===1){S.add(q[0]);change=true}}if(!change)return false}}
 for(let x of z.native.proof){if(x.p.some(i=>i>=rows.length||i<0))throw Error("parent");let ps=x.p.map(i=>rows[i]);if(!check(x.c,ps))throw Error("bad proof");let mask=ps.reduce((a,b)=>a|b.mask,0n);words+=ps.length*Math.ceil(m/64);if(mask.toString(16)!==x.mask)throw Error("mask");rows.push({c:x.c,mask})}
 function batch(F,prefix){
 let M=new Map(),dead=0n,passes=0,ops=0,scan=0,changes=0;
 function get(l){return M.get(l)??0n}
 for(;;){let old=changes,oldDead=dead;passes++;
 for(let {c,mask} of F){scan++;let active=A&~mask&~dead;ops+=2;let f=c.map(l=>get(-l)),n=f.length,pre=[active],suf=Array(n+1).fill(A);
 for(let i=0;i<n;i++){pre.push(pre[i]&f[i]);ops++}dead|=pre[n];ops++;
 if(prefix)for(let i=n-1;i>=0;i--){suf[i]=suf[i+1]&f[i];ops++}
 for(let i=0;i<n;i++){let v;if(prefix){v=pre[i]&suf[i+1];ops++}else{v=active;for(let j=0;j<n;j++)if(j!==i){v&=f[j];ops++}}
 v&=~dead;let l=c[i],x=get(l),q=x|v;ops+=2;if(q!==x){M.set(l,q);changes++}dead|=q&get(-l);ops+=2;}
 }if(changes===old&&dead===oldDead)break;
 if(passes>1000)throw Error("pass cap")}
 return {passes,ops,scan,wordOps:ops*Math.ceil(m/64),dead:dead.toString(16),excluded:Array.from({length:m},(_,i)=>i).filter(i=>!!(dead&(1n<<BigInt(i)))),maskPayloadBits:M.size*m};
 }
 let baseline=batch(rows.slice(0,C.length),false),a=batch(rows,false),b=batch(rows,true);if(a.dead!==b.dead)throw Error("batch difference "+a.dead+" "+b.dead);
 let scalar=z.native.results.filter(x=>x.hybrid.status==="UNSAT").map(x=>x.owner);if(JSON.stringify(scalar)!==JSON.stringify(a.excluded))throw Error("scalar difference");
 let noEmpty=batch(rows.filter(x=>x.c.length),true),block=new Set([C.length]);for(let j=0;j<z.native.proof.length;j++)if(z.native.proof[j].p.some(i=>block.has(i)))block.add(C.length+j);let removal=batch(rows.filter((_,i)=>!block.has(i)),true);
 return {reads,words,baseline,plain:a,compressed:b,noEmpty,removal:{...removal,blocked:block.size}};
}
if(typeof module!=="undefined")module.exports={audit};
