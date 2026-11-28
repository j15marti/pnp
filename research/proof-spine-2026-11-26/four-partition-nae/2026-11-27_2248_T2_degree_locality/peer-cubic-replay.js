function replay(bundle,data,sha){
 let out=[];for(let item of bundle.items){let p=item.proof,x=data.families.find(x=>x.sha===p.sha);
 if(!x||sha(x.raw)!==p.sha||x.raw.length*8!==item.original_N_bits)throw Error("source auth");
 let lines=x.raw.trimEnd().split("\n"),h=lines.shift().split(" ").map(Number),F=new Set(lines.map(s=>s.split(" ").map(Number).slice(0,-1).sort((a,b)=>a-b).join(","))),used=new Set(),sum=new Map(),checks=0,terms=0;
 const has=c=>{checks++;if(!F.has(c.sort((a,b)=>a-b).join(",")))throw Error("missing source clause")};
 function color(u,c){if(c===0)return [[2*u+1]];if(c===1)return [[2*u+2]];if(c===2)return [[],[2*u+1],[2*u+2]];throw Error("color")}
 for(let [a,b,c,m] of p.proof){if(![a,b,c,m].every(Number.isInteger)||a<0||b<0||a===b||a*3+3>h[2]||b*3+3>h[2]||m<0||m>2*h[2]/3)throw Error("bounds");
 has([-(3*a+c+1),-(3*b+c+1)]);used.add(a);used.add(b);if(m)used.add(Math.floor((m-1)/2));
 for(let u of color(a,c))for(let v of color(b,c)){let ids=[...new Set([...u,...v,...(m?[m]:[])])].sort((a,b)=>a-b),key=ids.join(",");sum.set(key,(sum.get(key)||0)^1);terms++}
 }
 for(let a of used){let u=3*a+1,v=u+1,w=u+2;has([u,v,w]);has([-u,-v]);has([-u,-w]);has([-v,-w]);}
 let nonzero=[...sum].filter(x=>x[1]).map(x=>x[0]);if(nonzero.length!==1||nonzero[0]!=="")throw Error("not constant one");
 out.push({instance:item.instance,instance_id:item.instance_id,N:item.original_N_bits,guard_id:"EMPTY",residual_id:"ROOT",sourceChecks:checks,unreducedProductTerms:terms,constant:1})}
 return out}
if(require.main===module){const fs=require('node:fs'),crypto=require('node:crypto');console.log(JSON.stringify(replay(JSON.parse(fs.readFileSync(process.argv[2],'utf8')),JSON.parse(fs.readFileSync(process.argv[3],'utf8')),s=>crypto.createHash('sha256').update(s).digest('hex')),null,2));}
