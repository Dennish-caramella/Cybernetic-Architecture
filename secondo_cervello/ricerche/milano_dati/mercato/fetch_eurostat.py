"""Scarica indicatori Eurostat (housing cost overburden ecc.) per IT/EU27 e salva CSV piatti.
Uso: python3 fetch_eurostat.py  (scrive eurostat_*.csv nella cartella corrente)"""
import json, urllib.request, itertools, csv, sys
BASE="https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
Q={
 "ilc_lvho07a":"geo=IT&geo=EU27_2020",
 "ilc_lvho07d":"geo=IT&geo=EU27_2020&unit=PC",
 "ilc_lvho07e":"geo=IT&geo=EU27_2020",
 "ilc_lvho07c":"geo=IT&geo=EU27_2020",
 "ilc_di03":"geo=IT",
 "ilc_li01":"geo=IT",
 "nama_10r_2hhinc":"geo=ITC4&geo=IT&geo=ITC",
 "ilc_lvho05a":"geo=IT&geo=EU27_2020",
 "ilc_mded01":"geo=IT&geo=EU27_2020&unit=PC",
 "ilc_lvho07d":"geo=IT&geo=EU27_2020&unit=PC",
}
for ds,q in Q.items():
    url=f"{BASE}{ds}?format=JSON&lang=en&{q}&sinceTimePeriod=2015"
    try:
        d=json.load(urllib.request.urlopen(url,timeout=60))
    except Exception as e:
        print(ds,"ERR",e); continue
    ids=d["id"]; size=d["size"]; dims=[]
    for k in ids:
        cat=d["dimension"][k]["category"]; idx=cat["index"]
        order=sorted(idx,key=idx.get); dims.append([(c,cat.get("label",{}).get(c,c)) for c in order])
    rows=[]
    for n,combo in enumerate(itertools.product(*dims)):
        v=d["value"].get(str(n))
        if v is None: continue
        rows.append([c for c,_ in combo]+[v])
    with open(f"eurostat_{ds}.csv","w",newline="") as f:
        w=csv.writer(f); w.writerow(ids+["value"]); w.writerows(rows)
    labs={k:dict(dl) for k,dl in zip(ids,dims)}
    print(ds,len(rows),"righe;", {k:list(v.items())[:12] for k,v in labs.items() if len(v)>1 and k!="time"})
