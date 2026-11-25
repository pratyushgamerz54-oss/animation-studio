# THE LAST 10 — EARTH: ZERO · DAY 3–10: EARTH ONE?  Finale v5: longer thriller — survival, suspense (Ryan thread), group drama.
# Builds on v4 (all v4 shots + lines kept) and inserts new sequences. Times computed from dialogue.
import day3_10_v4_data as V4
from day3_10_v4_data import CAST, SCENES, TITLE, est, GAP, TAIL

LOGLINE = """Lab mein pehla 3D <b>Zeno</b> utarta hai, teeno data lekar bachte hain, Kabir ghayal hota hai. Bunker mein paani ka filter phat jaata hai, raashan aadha hota hai
aur jhagde shuru ho jaate hain. Raat ko Ryan ko ajeeb fusfusahatein sunaai deti hain, aur Ananya ke camera mein ek frame ke liye uski gardan par <b>neeli roshni</b> chamakti hai.
Safar mein <b>survival</b> hai: zehreeli raakh ka toofan, khaali supermarket mein paani, aur freezer room mein drone se chhupna jab Ishaan ki ghadi bajne lagti hai.
Pul par pehla yudh hota hai aur Vikram gir jaata hai. Baarish mein Kabir ka ghaav sad jaata hai. Zoya dooba hua hospital mein gota lagati hai, Dev rassi pakde ginti ginta hai.
Phir Ananya footage dikhati hai, <b>Ryan par shak</b> hota hai, Ishaan bhadak jaata hai, aur Aarav faisla karta hai ki Ryan unke saath hi chalega.
Dam mein sach khulta hai (kavach, darwaza, "wo hamein dhoondh rahe the"), aur Commander ki awaaz Ryan ko lalchaati hai: <i>"haath rakho... tumhari crew laut aayegi."</i>
Aakhri yudh mein Ryan lagbhag darwaza khol deta hai. Aarav uska naam pukaar kar use wapas laata hai. Vikram lautta hai, Dev girta hai par bach jaata hai, aur daraar sil jaati hai.
Day 10 ko dhoop lautti hai aur dason zinda hain. Par space mein Commander kehta hai <i>"unmein se ek... ab bhi hamara hai"</i>, Ryan ki gardan phir chamakti hai,
aur Ananya footage rewind karke dekh leti hai. TO BE CONTINUED."""
CORE = V4.CORE + " Aur sabse bada darr: dushman bahar hi nahi, shayad hamare beech bhi hai."
HOOKS = ("Day 3 = pehla Zeno · Day 4 = raashan ka jhagda + Ryan ki neeli roshni (1 frame) · Day 5 = raakh ka toofan, freezer mein drone + bajti ghadi · "
         "Day 6 = pul + Vikram · Day 7 = dooba hospital + Ryan par shak · Day 8 = twist + Commander ki awaaz Ryan ke dimaag mein · "
         "Day 9 = Ryan lagbhag darwaza kholta, Vikram lautta, Dev girta-bachta · Day 10 = dhoop → Commander + pods + Ryan ki roshni + Ananya dekh leti")
NOTES = V4.NOTES.replace("finale v4)</h3><ul>", """finale v5)</h3><ul>
<li><b>v5 = lambi thriller:</b> 3 dhaage saath chalte — (1) <b>Survival</b>: paani, raashan, zehreeli hawa, khaana, dawa, chhupna; (2) <b>Suspense</b>: Ryan ki fusfusahatein + neeli roshni (Day 4 → 10, har baar thoda zyada); (3) <b>Drama</b>: raashan ka jhagda, Ryan par shak, Ishaan ka gussa, Aarav ka bharosa.</li>
<li><b>Survival rules (screen par saaf):</b> paani ki bottlein gin kar, gile kapde ka mask, rassi se bandhe chalna, ginti bol kar ek doosre ko dhoondhna, freezer mein saans ki bhaap chhupana, ghav saaf karna, dawa pehchaanna.</li>""", 1)

# new shots: (id, scene, vmin, cam, action, acting, transition, sound) — inserted AFTER the given v4 shot id
NEW = {
 "4C": [
  ("4D", 4, 14, "Bunker raat, lantern medium → group", "Pump room: phati membrane; Kabir haath mein tukda; sab ikattha; paani ke drum par chalk se nishaan",
   "Lantern ki roshni neeche se, lambi parchhaiyan; Ishaan ka pet gurraata, wo sharminda; Vikram drum par haath rakh kar khada jaise pehredaar; Zoya Kabir ke maathe par haath (bukhaar chec)", "—", "Paani tapakna, pump ki aakhri ghurghurahat, dhadkan"),
  ("4E", 4, 12, "Corridor, Ryan akela → Ananya ke camera ka POV", "Ryan diwaar se sir tikaye; fusfusahat; Ananya aati; camera ki screen par 1 frame ke liye Ryan ki gardan neeli",
   "Ryan aankhein bheench kar kanpatti dabata, saans tez; Ananya ki awaaz par jhatke se seedha hota, muskaan banata; Ananya jaate hue ruk kar camera rewind karti, bhauein sikudti", "dip", "Bunker hum, distorted alien fusfusahat (sirf Ryan sunta), camera beep"),
 ],
 "5A": [
  ("5S1", 5, 16, "Wide → close, raakh ka toofan", "Narangi-grey raakh ki deewar aati; sab rassi pakad kar chalte; kuch nahi dikhta",
   "Gile kapde munh par baandhte; aankhein sikod kar, ek haath rassi par, doosra aage tatolta; Ishaan khaansi mein jhukta; Vikram ki awaaz par sab sir ghumaate", "—", "Toofan ki seeti, khaansi, rassi ki khinchaav"),
  ("5S2", 5, 16, "Khaali supermarket, medium → wide", "Ulti trolleys, khaali shelves; ek shelf par paani ki bottlein; shelf girti",
   "Ishaan bottle seene se lagata jaise khazana; Kabir biscuit ka packet soongh kar khaata; Dev farsh par pair rakh kar daraar sunta; shelf girte hi sab jam jaate, phir aankhein darwaze par", "—", "Goonj, plastic ki khadkhad, shelf crash, door drone"),
  ("5S3", 5, 22, "Freezer room, tight → glass ke paar drone", "Sab chipke khade; glass ke bahar hunter drone ki laal aankh scan karti; Ishaan ki ghadi beep",
   "Saans ki bhaap chhupane ke liye munh par haath; Zoya jhapat kar Ishaan ki ghadi mutthi mein dabati; drone ki roshni chehron par se guzarti, sab aankhein mund lete; drone jaane par sab ghutno par jhuk kar saans lete", "dissolve", "Drone hum, ek beep, poori khamoshi, phir saans"),
 ],
 "7A": [
  ("7S1", 7, 14, "Tooti bus stop ki chhat ke neeche, close-ups", "Kabir bukhaar mein kaanpta; Zoya ghaav kholti; saamne aadha dooba hospital",
   "Kabir ke maathe par pasina, aankhein ghoomti; Zoya ki ungliyan kaanpti par kaam karti; Dev hospital ki taraf dekh kar rassi kholta", "—", "Baarish, Kabir ki tez saans, door paani"),
  ("7S2", 7, 22, "Paani ke andar (underwater) ↔ upar Dev", "Zoya gota lagati, dooba pharmacy; darwaza atakta; rassi kheechti; Dev kheench kar nikaalta",
   "Paani mein baal tairte, bulbule; Zoya darwaze par paon tika kar kheenchti; hawa khatam, aankhein phailti, rassi do baar kheenchti; upar Dev ke haath par rassi ka nishaan; Zoya bahar aakar haanpti, phir hasti", "—", "Paani ke andar dabi awaaz, dhadkan tez, bahar aate hi saans + baarish"),
  ("7S3", 7, 26, "Group circle, baarish, tense drift", "Ananya camera ki screen dikhati: pul par Ryan ki gardan neeli; sab Ryan se ek kadam door",
   "Sab ki nazrein Ryan par; Ishaan ki mutthi bandhi, aage badhta, Dev beech mein; Ryan apni gardan chhoota, haath kaanpta; Aarav dheere se Ryan ke bagal mein jaakar khada hota", "—", "Baarish, low drone, dhadkan"),
 ],
 "8B": [
  ("8C2", 8, 14, "Node ke paas, Ryan akela → Sara", "Raat ko Ryan neend mein chalta hua node ki taraf; haath uthta; Sara dekh leti",
   "Ryan ki aankhein khuli par khaali, chaal dheemi jaise koi kheench raha; node ki roshni uski gardan ke saath dhadakti; Sara ki awaaz par Ryan ladkhadata, apne haath ko ajeeb nazar se dekhta", "dip", "Alien fusfusahat, node ki dhadkan, khamoshi"),
 ],
 "9B": [
  ("9C0", 9, 18, "Node ke saamne, Ryan ↔ Aarav close-ups", "Yudh ke beech Ryan ka haath node ki taraf; Aarav pakadta; Ryan ki aankhon mein neeli chamak ladti",
   "Ryan ki baanh kaanpti, do taaqatein khinch rahi; Aarav uska chehra dono haathon se pakad kar apni taraf karta; naam bolte hi Ryan ki aankh mein roshni bujhti, aansu", "—", "Alien awaaz + battle muffle, phir saaf"),
 ],
}
NEWL = {
 "4D": [("Kabir", "Filter गया। Pump की membrane फट गई।", "Thaka, tukda dikhaate hue.", 1.0),
        ("Dr. Meera", "कितना पानी बचा है?", "Dheemi, darr chhupate hue."),
        ("Kabir", "दस लोगों के लिए... दो दिन। अगर कोई नहाने की ज़िद न करे।", "Thaka sarcasm."),
        ("Vikram", "आज से राशन आधा। सबके लिए।", "Sakht, final."),
        ("Ishaan", "आधा? पहले ही भूख से चक्कर आ रहे हैं!", "Gussa, pet par haath."),
        ("Vikram", "चक्कर से कोई नहीं मरता। प्यास से मरता है।", "Thanda sach."),
        ("Zoya", "Kabir का हिस्सा मत काटो। Infection से लड़ने के लिए पानी चाहिए।", "Fikar, doctor ki zid."),
        ("Kabir", "नहीं... मेरा भी आधा। मैं special नहीं हूँ।", "Muskaan, par aankhein thaki."),
        ("Dev", "मेरा आधा उसे दे दो। मैं ऊँट हूँ, आदत है।", "Halki hasi, baat khatam karte hue.")],
 "4E": [("Ryan", "फिर से... ये आवाज़ें...", "(khud se) Kanpatti dabate hue, dard.", 1.5),
        ("Zeno Commander", "...दरवाज़ा... खोलो...", "Distorted fusfusahat — sirf Ryan sunta hai.", 0.8),
        ("Ananya", "Ryan? तुम ठीक हो?", "Narm, chinta."),
        ("Ryan", "सिर दर्द। Space की पुरानी आदत।", "Jhooti muskaan."),
        ("Ananya", "...ये रोशनी कैसी थी?", "(khud se) Camera rewind karte hue, shak.", 1.5)],
 "5S1": [("Sara", "हवा का रंग देखो... ये धूल नहीं, राख है। ज़हरीली।", "Chinta, haath mein raakh masal kar.", 1.0),
         ("Dev", "कपड़ा गीला करो, नाक-मुँह पर बाँधो। रस्सी मत छोड़ना!", "Tez hukm, hawa ke upar."),
         ("Ishaan", "कुछ... कुछ दिख नहीं रहा...", "Khaanste hue, ghabrahat."),
         ("Vikram", "मेरी आवाज़ सुनो! Ishaan, गिनती बोल!", "Poori awaaz, shaant."),
         ("Ishaan", "एक... दो... तीन...", "Kaanpti awaaz, dheere mazboot hoti."),
         ("Aarav", "सब गिनो! दस तक! कोई चुप नहीं रहेगा!", "Chillaate hue, leader.")],
 "5S2": [("Ishaan", "पानी! बोतलें! पूरी shelf भरी है!", "Khushi se chillaata, phir khud munh dabata.", 1.0),
         ("Kabir", "और biscuit... expire हो चुके हैं। पर कौन देख रहा है।", "Khaate hue, muskaan."),
         ("Dev", "धीरे! फ़र्श कमज़ोर है।", "Fusfusahat, haath utha kar."),
         ("Ryan", "शोर... उन्होंने सुना होगा।", "Shelf girne ke baad, darr.", 2.0),
         ("Vikram", "Freezer room में! सब! अभी!", "Dabi hui cheekh.")],
 "5S3": [("Aarav", "कोई साँस भी ज़ोर से नहीं लेगा।", "Fusfusahat.", 1.0),
         ("Ishaan", "प्लीज़... प्लीज़ बजना मत...", "(khud se) Ghadi dekhte hue, kaanpte honth.", 2.5),
         ("Kabir", "मेरी जान... आधी निकल गई।", "Drone jaane ke baad, fusfusahat, haanfte.", 5.0),
         ("Sara", "बाकी आधी पानी के लिए बचा के रखो।", "Thaki muskaan."),
         ("Zoya", "अगली बार ये ghadi मैं तोड़ दूँगी।", "Ishaan ko ghoor kar, aadha mazaak.")],
 "7S1": [("Zoya", "बुखार बहुत तेज़ है... घाव में infection है। Antibiotic के बिना... कल तक नहीं।", "Darr, par saaf.", 1.0),
         ("Kabir", "माँ... फ़ोन उठा रहा हूँ... रुको...", "Bukhaar mein bad-badaate hue. Dil todne wala.", 1.0),
         ("Dev", "सामने hospital है। आधा पानी में डूबा।", "Dheemi, faisla soch kar."),
         ("Zoya", "मैं जाऊँगी। दवा मुझे पहचाननी है।", "Pakki, aansu poch kar."),
         ("Dev", "तो रस्सी मैं पकड़ूँगा। इस बार हाथ नहीं छूटेगा।", "Zoya ki kalai ki gaanth dekh kar.")],
 "7S2": [("Zoya", "डरना मत, Zoya... बस एक साँस।", "(khud se) Gota lagane se pehle.", 1.0),
         ("Dev", "बीस... पच्चीस... तीस... चल बेटा, ऊपर आ...", "(khud se) Rassi pakde, ginti, darr badhta.", 5.0),
         ("Dev", "अब!", "Rassi ke do jhatke par, poora zor.", 2.0),
         ("Zoya", "मिल गई! Antibiotic... पूरा डिब्बा!", "Haanfte hue, hasi.", 2.0),
         ("Dev", "आज फिर किसी का हाथ नहीं छूटा।", "Aankhein geeli, muskaan.")],
 "7S3": [("Ananya", "Aarav... ये देखो। पुल पर... Ryan की गर्दन।", "Dheemi, kaanpte haath.", 1.0),
         ("Aarav", "ये... नीली रोशनी?", "Hairani."),
         ("Ishaan", "तो इसलिए वो हर बार हमें ढूंढ लेते हैं! ये signal भेज रहा है!", "Gussa, ungli Ryan par."),
         ("Ryan", "मुझे नहीं पता ये क्या है! क़सम से... मुझे नहीं पता।", "Toot-ti awaaz, darr."),
         ("Dr. Meera", "शांत! अभी किसी पर इल्ज़ाम नहीं।", "Beech mein aakar."),
         ("Ishaan", "Vikram मर गया, Meera! किसी की तो ग़लती है!", "Aansu aur gussa, cheekh."),
         ("Aarav", "बस!", "Ek shabd, sab chup.", 0.8),
         ("Aarav", "Ryan हमारे साथ चलेगा। मेरे बगल में।", "Shaant, bharosa.", 1.2),
         ("Ryan", "अगर मैं ख़तरा बना... तो रुकना मत, Aarav।", "Dheemi, sachchi."),
         ("Aarav", "तब तक तू हमारा है।", "Uska kandha pakad kar.")],
 "8C2": [("Zeno Commander", "हाथ रखो... और तुम्हारी crew लौट आएगी।", "Distorted, meethi lalach bhari fusfusahat.", 2.0),
         ("Ryan", "मेरी crew... ज़िंदा है?", "(khud se) Neend mein, umeed."),
         ("Sara", "Ryan! वहाँ से हटो!", "Tez, darr.", 0.8),
         ("Ryan", "मैं... मैं यहाँ कैसे आया?", "Jaag kar, apne haath dekhte hue, darr.")],
 "9C0": [("Zeno Commander", "अभी, Ryan। खोलो।", "Distorted hukm.", 0.8),
         ("Aarav", "Ryan! मेरी तरफ़ देख! तेरा नाम क्या है?", "Chehra pakad kar, chillaate hue."),
         ("Ryan", "Ryan... मैं... Ryan हूँ...", "Ladte hue, toot-ti awaaz."),
         ("Aarav", "और तू किसके साथ है?", "Aankhon mein aankhein daal kar."),
         ("Ryan", "...तुम्हारे साथ।", "Roshni bujhti, aansu. Wapas aata hai.")],
}
EXTRA = {  # extra lines appended to existing v4 shots
 "8A": [("Kabir", "दवा काम कर गई... अब बस ये dam मुझे न खा जाए।", "Halki hasi, ab theek.")],
 "10C": [("Ananya", "...फिर से।", "(khud se) Dam par footage rewind karke Ryan ki gardan dekhti. Shak waapas.", 1.5)],
}

SHOTDEF, L = [], {}
for sd in V4.SHOTDEF:
    SHOTDEF.append(sd); L[sd[0]] = list(V4.L.get(sd[0], [])) + EXTRA.get(sd[0], [])
    for nd in NEW.get(sd[0], []):
        SHOTDEF.append(nd); L[nd[0]] = NEWL[nd[0]]
SHOTS, LINES, t = [], [], 0.0
for sid, sc, vmin, cam, act, acting, tr, snd in SHOTDEF:
    cur = t
    for item in L.get(sid, []):
        who, x, n = item[:3]; pre = item[3] if len(item) > 3 else GAP
        cur += pre; LINES.append((round(cur, 1), who, x, n, sid)); cur += est(x)
    dur = max(vmin, cur - t + (TAIL if L.get(sid) else 0))
    SHOTS.append((sid, sc, round(t, 1), round(t + dur, 1), cam, act + (" — ACTING: " + acting if acting != "—" else ""), tr, snd))
    t = round(t + dur, 1)
DUR = t
SERIES_LINE = f"~{int(DUR // 60)}:{int(DUR % 60):02d} · Day 3 se Day 10 · thriller: survival + suspense + drama · long form mein DAY card nahi · 3D Zeno + 2 yudh · suspense ending"
