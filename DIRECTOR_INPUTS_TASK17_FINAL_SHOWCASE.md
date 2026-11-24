# TASK 17 — FINAL SHOWCASE CINEMATIC (Director, 24 Nov) — YAAD RAKHNA, ABHI SHURU NAHI

## Director — verbatim
```
Ek baat yaad rakhna save karo kul mera task 17 hai jab ye sab pura ho jaye to mere ko us samay ke liye sare flora aur faun aur sare world aapsa me laar ek cinematic scene banao sabk 8 k me kuch fate na samjhe usme sambkuch ana chiye samjhe na matlab sab kuch jitna bhi kaam hua hai aur janwar apna kaam karte rhega bhale koi hi ya na ho apna din chalega sabkuch hota rhega din badlega sab kuch jaise real world jaise samjhe bas hamko chiye taki story upload kar sku smjhe na 
8 k me sab kuch dubara render karna sab kuch suruwat se lekar task 17 tak mp4 dekar apan 2k me kar lena uske baad aage ka kama kiya jayega
```

## Claude ki samajh (checklist for when TASK 17 starts)
- Total project = **17 tasks**. TASK 17 = jab baaki sab pura ho jaye.
- **Ek cinematic showcase scene/film:** SAARA world (saare regions, terrain, water, sky) + SAARA flora (TASK 06 ecosystem)
  + SAARI fauna (TASK 07 creatures) + baaki jo bhi bana (characters, props, VFX) — **kuch bhi chhootna nahi chahiye**.
- **Living world:** janwar apna kaam khud karte rahein (behaviour baker / RDR2-style: chalna, charna, peena, shikaar, udna,
  tairna, aaram) — koi character ho ya na ho; **din-raat ka chakra** (sunrise → day → sunset → night, roshni + mausam badle),
  hawa, paani, ped-paudhe hilte rahein — sab real-world jaisa (realism + physics rules).
- **Quality:** 8K, kahin bhi pixel "fate" nahi (no blur / tiling / noise / aliasing at 100 % zoom) → LOD0 hero assets,
  8K textures, high samples + denoise, motion blur.
- **Re-render:** TASK 1 se TASK 17 tak ka SAB kuch dobara 8K mein render (sheets, turnarounds, world, flora, fauna, clips).
- **Delivery:** MP4. Yahan (CPU, no GPU) **2K** version banana; 8K master render Director ke GPU PC par
  (Claude render scripts / resume-able `*_finish_pending.sh` dega). 8K/4K masters git mein NAHI (Drive / PC).
- Purpose: Director story / showcase upload karega. Iske baad aage ka kaam.

## Director clarification (24 Nov) — verbatim
```
Abhi 2k me bana smajh task 17 ke baad ye sab kaam karna hai us samay kar lena smajh kyuki abhi gpu nhi hai isi liye
```
**Final decision:** TASK 17 ka showcase + TASK 1–17 ka re-render → **2K mein, yahan (CPU)** banana, TASK 17 ke time par.
8K tab hoga jab GPU milega (baad mein). Assets phir bhi 8K-ready rakhna (sources / LOD0 / 8K textures) taaki baad mein seedha 8K ho sake.
