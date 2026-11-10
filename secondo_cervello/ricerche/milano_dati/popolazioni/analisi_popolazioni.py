"""Popolazioni mancanti (famiglie, studenti, nuovi arrivi) - elaborazioni open data Comune di Milano.
Input (scaricati 10/11/2026 da dati.comune.milano.it, API CKAN package_show, non versionati):
 ds1441 (tipologie famiglie per NIL 1999-2025), ds139 (tipologie con minori 2007-2021),
 ds1457 (censimento 2011 titolo di godimento per NIL), ds71 (movimento anagrafico 1880-2024),
 ds205 (indicatori NIL 2011-2024), ds752 (iscritti universita' milanesi 2017-2025), ds395 (pendolari in entrata 2011).
Uso: python3 -I analisi_popolazioni.py <cartella_input>   (output nella cartella dello script)
"""
import sys, glob, os
import pandas as pd
IN = sys.argv[1]; OUT = os.path.dirname(os.path.abspath(__file__))
def rd(p, **k): return pd.read_csv(glob.glob(os.path.join(IN, p))[0], sep=';', encoding='latin1', **k)
def fix(s): return s.str.replace('Ã¹','u').str.replace('Ã ','a')

# 1. famiglie 2025 (ds1441)
f = rd('z/ds1441_*.csv', usecols=['Anno','Quartiere','Classe_eta_capofamiglia','Numero_componenti','Tipologia_familiare','Cittadinanza','Famiglie'])
for c in ['Classe_eta_capofamiglia','Numero_componenti','Tipologia_familiare']: f[c]=fix(f[c].astype(str))
f['straniera'] = f.Cittadinanza!='Italia'
tot = f.groupby('Anno').Famiglie.sum()
y = f[f.Anno==2025]
rows=[]
for dim in ['Tipologia_familiare','Numero_componenti','Classe_eta_capofamiglia']:
    g=y.groupby(dim).Famiglie.sum()
    for k,v in g.items(): rows.append((dim,k,v,round(100*v/g.sum(),1)))
g=y.groupby('straniera').Famiglie.sum()
for k,v in g.items(): rows.append(('capofamiglia_straniero',k,v,round(100*v/g.sum(),1)))
# anziani soli
mono=y[y.Tipologia_familiare=='Monocomponente']
for k,v in mono.groupby('Classe_eta_capofamiglia').Famiglie.sum().items(): rows.append(('monocomponente_per_eta',k,v,round(100*v/mono.Famiglie.sum(),1)))
# tipologia per eta capofamiglia (giovani <35)
for (a,t),v in y.groupby(['Classe_eta_capofamiglia','Tipologia_familiare']).Famiglie.sum().items(): rows.append(('eta_x_tipologia',f'{a} | {t}',v,None))
pd.DataFrame(rows,columns=['dimensione','modalita','famiglie_2025','quota_%']).to_csv(f'{OUT}/famiglie_2025_milano_ds1441.csv',index=False)
# per NIL
p = y.pivot_table(index='Quartiere',columns='Tipologia_familiare',values='Famiglie',aggfunc='sum',fill_value=0)
p['totale']=p.sum(axis=1)
p['con_figli']=p['Coppia sposata con figli']+p['Monogenitore con uno o piu figli']+p['Monogenitore con uno o piu figli e almeno un convivente']
p['quota_con_figli_%']=(100*p.con_figli/p.totale).round(1)
p['quota_monocomp_%']=(100*p['Monocomponente']/p.totale).round(1)
a80=y[(y.Tipologia_familiare=='Monocomponente')&(y.Classe_eta_capofamiglia.str.startswith(('65','80')))].groupby('Quartiere').Famiglie.sum()
p['soli_65piu']=a80.reindex(p.index).fillna(0).astype(int)
p['under35_capofam']=y[y.Classe_eta_capofamiglia=='Meno di 35 anni'].groupby('Quartiere').Famiglie.sum().reindex(p.index).fillna(0).astype(int)
p.sort_values('totale',ascending=False).to_csv(f'{OUT}/famiglie_2025_per_NIL_ds1441.csv')
# serie
s = f[f.Anno.isin([2005,2010,2015,2020,2021,2025])].pivot_table(index='Anno',columns='Tipologia_familiare',values='Famiglie',aggfunc='sum')
s['totale']=tot.reindex(s.index); s.to_csv(f'{OUT}/famiglie_serie_tipologia_ds1441.csv')

# 1b. famiglie con minori 2021 (ds139)
m = rd('z139/ds139_*.csv'); m.columns=[c.replace('ï»¿','') for c in m.columns]
m21 = m[m.Anno==2021]
mm = m21.groupby('Tipologia_familiare').Famiglie.sum()
mm.to_csv(f'{OUT}/famiglie_2021_con_minori_ds139.csv')
mn = m21.pivot_table(index='NIL',columns='Tipologia_familiare',values='Famiglie',aggfunc='sum',fill_value=0)
mn['con_minori']=mn[[c for c in mn.columns if 'minorenne' in c]].sum(axis=1)
mn['monogen_minori']=mn['Monogenitore con almeno un figlio minorenne']
mn['totale']=mn[[c for c in mn.columns if c not in('con_minori','monogen_minori')]].sum(axis=1)
mn['quota_con_minori_%']=(100*mn.con_minori/mn.totale).round(1)
mn[['totale','con_minori','monogen_minori','quota_con_minori_%']].sort_values('con_minori',ascending=False).to_csv(f'{OUT}/famiglie_2021_con_minori_per_NIL_ds139.csv')

# 1c. titolo di godimento 2011 per NIL (ds1457)
t = rd('ds1457*titolo_di_godimento*.csv'); t.columns=['NIL','proprieta','affitto','altro']
t['totale']=t[['proprieta','affitto','altro']].sum(axis=1)
for c in ['proprieta','affitto','altro']: t[f'{c}_%']=(100*t[c]/t.totale).round(1)
t.sort_values('totale',ascending=False).to_csv(f'{OUT}/titolo_godimento_2011_per_NIL_ds1457.csv',index=False)
print('TENURE 2011', t[['proprieta','affitto','altro','totale']].sum().to_dict())

# 3. migrazioni (ds71, ds205)
mv = rd('ds71*.csv'); mv.columns=['anno','nati','morti','immigrati','emigrati','aggiust','pop']
mv=mv[mv.anno>=2010]; mv['saldo_migratorio']=mv.immigrati-mv.emigrati; mv['saldo_naturale']=mv.nati-mv.morti
mv.to_csv(f'{OUT}/movimento_anagrafico_2010_2024_ds71.csv',index=False)
q = rd('ds205*.csv'); q24=q[q.Anno==q.Anno.max()]
q24[['Anno','Quartiere','NIL','Totale','Minori','Stranieri','Immigrati','Emigrati','65 e +','80 e +','80 e + soli fam registrate in anagrafe','Famiglie registrate in anagrafe']].sort_values('Immigrati',ascending=False).to_csv(f'{OUT}/nil_immigrati_emigrati_minori_ds205.csv',index=False)

# 2. studenti (ds752)
rows=[]
for fn in sorted(glob.glob(os.path.join(IN,'ds752*.csv'))):
    u=pd.read_csv(fn,sep=None,engine='python',encoding='latin1')
    u.columns=[c.strip().replace('ï»¿','') for c in u.columns]
    g=u.groupby(['AnnoA','AteneoNOME']).Isc.sum().reset_index(); rows.append(g)
st=pd.concat(rows); st.to_csv(f'{OUT}/iscritti_universita_milanesi_ds752.csv',index=False)
print(st.pivot_table(index='AteneoNOME',columns='AnnoA',values='Isc',aggfunc='sum').to_string())

# 3b. pendolari in entrata 2011 (ds395)
pe = rd('z/395_*.csv', decimal=','); pe.columns=['sesso','regione','provincia','comune','motivo','mezzo','orario','tempo','n']
pe.groupby(['motivo','provincia']).n.sum().sort_values(ascending=False).to_csv(f'{OUT}/pendolari_entrata_2011_motivo_provincia_ds395.csv')
print('PENDOLARI 2011', pe.groupby('motivo').n.sum().to_dict(), pe.n.sum())
print(pe.groupby('mezzo').n.sum().sort_values(ascending=False).head(6).to_dict())
print(pe.groupby('tempo').n.sum().to_dict())
