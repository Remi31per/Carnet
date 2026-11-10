"""Résume les pages d'actions rappn.ch téléchargées (data/raw/*.html) en un seul fichier JSON lisible :
data/raw/actions-brutes.json = {telecharge_le, pages:[{magasin, canton, titre, resume, offres:[{nom, marque, prix, ancien_prix}]}]}"""
import glob, html, json, os, re
pages = []
for f in sorted(glob.glob("data/raw/rappn-*.html")):
    t = open(f, encoding="utf-8", errors="ignore").read()
    m = re.match(r"data/raw/rappn-(.+)-(VD|FR)\.html", f)
    if not m: continue
    offres = []
    for bloc in re.findall(r"<script[^>]*ld\+json[^>]*>(.*?)</script>", t, re.S):
        try: j = json.loads(bloc)
        except Exception: continue
        for g in j.get("@graph", []):
            for it in g.get("itemListElement", []):
                p = it.get("item")
                if not isinstance(p, dict) or p.get("@type") != "Product": continue
                o = p.get("offers") or {}
                spec = o.get("priceSpecification") or {}
                offres.append({"nom": p.get("name"), "marque": (p.get("brand") or {}).get("name"),
                               "prix": o.get("price"), "ancien_prix": spec.get("price"),
                               "region": (o.get("areaServed") or {}).get("name")})
    texte = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
    texte = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", texte))).strip()
    titre = re.search(r"<title>(.*?)</title>", t, re.S)
    pages.append({"magasin": m.group(1), "canton": m.group(2), "titre": html.unescape(titre.group(1)).strip() if titre else "",
                  "resume": texte[:1200], "texte_complet": texte[:40000], "offres": offres})
quand = open("data/raw/telecharge-le.txt").read().strip() if os.path.exists("data/raw/telecharge-le.txt") else ""
json.dump({"telecharge_le": quand, "pages": pages}, open("data/raw/actions-brutes.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print({p["magasin"]+"-"+p["canton"]: len(p["offres"]) for p in pages})
