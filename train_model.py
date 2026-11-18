"""
Sistema inteligente de detección de fraude en redes blockchain con seguridad post-cuántica
Entrenamiento del motor de IA.

Entrena Regresión logística, Random Forest y SVM sobre el Ethereum Fraud Detection
Dataset (Kaggle), calcula las métricas y exporta a ../data.js un Random Forest ligero
(30 árboles, 8 variables) que la página web ejecuta en el navegador.

Uso:  python train_model.py [ruta/al/transaction_dataset.csv]
"""
import sys, os, json, warnings; warnings.filterwarnings('ignore')
import pandas as pd, numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
CSV = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), 'transaction_dataset.csv')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data.js')
df = pd.read_csv(CSV); df.columns=[c.strip() for c in df.columns]
y = df['FLAG']
X = df.drop(columns=['FLAG']).select_dtypes('number').drop(columns=['Unnamed: 0','Index'],errors='ignore').fillna(0)
Xtr,Xte,ytr,yte = train_test_split(X,y,test_size=0.2,random_state=42)
out={'n':len(df),'fraud':int(y.sum()),'ntrain':len(Xtr),'ntest':len(Xte),'models':{}}
for n,m in {'Regresión logística':LogisticRegression(),'Random Forest':RandomForestClassifier(random_state=42),'SVM':SVC()}.items():
    m.fit(Xtr,ytr); p=m.predict(Xte)
    out['models'][n]={'acc':accuracy_score(yte,p),'prec':precision_score(yte,p,zero_division=0),'rec':recall_score(yte,p),'f1':f1_score(yte,p),'cm':confusion_matrix(yte,p).tolist()}
    if n=='Random Forest': rf=m
imp=sorted(zip(X.columns,rf.feature_importances_),key=lambda t:-t[1])
out['importance']=[[a,float(b)] for a,b in imp[:10]]
print(json.dumps(out,ensure_ascii=False,indent=1)[:3000])
# light model
top=[a for a,_ in imp[:8]]
lite=RandomForestClassifier(n_estimators=30,max_depth=8,random_state=42).fit(Xtr[top],ytr)
p=lite.predict(Xte[top])
lm={'acc':accuracy_score(yte,p),'prec':precision_score(yte,p),'rec':recall_score(yte,p),'f1':f1_score(yte,p)}
print('lite',lm)
trees=[]
for est in lite.estimators_:
    t=est.tree_
    v=t.value[:,0,:]; v=(v/v.sum(1,keepdims=True))[:,1]
    trees.append({'f':t.feature.tolist(),'t':[round(float(x),6) for x in t.threshold],'l':t.children_left.tolist(),'r':t.children_right.tolist(),'v':[round(float(x),4) for x in v]})
# example accounts from test set
proba=lite.predict_proba(Xte[top])[:,1]
te=Xte[top].copy(); te['y']=yte.values; te['p']=proba
ex=[]
for lab,cond in [('fraude',(te.y==1)&(te.p>0.85)),('legit',(te.y==0)&(te.p<0.1)),('fraude2',(te.y==1)&(te.p.between(0.6,0.85))),('legit2',(te.y==0)&(te.p.between(0.15,0.4)))]:
    r=te[cond].head(1)
    if len(r): ex.append({'k':lab,'x':[float(a) for a in r[top].values[0]],'y':int(r.y.values[0]),'p':float(r.p.values[0])})
desc={c:{'min':float(X[c].min()),'med':float(X[c].median()),'max':float(X[c].max()),'q95':float(X[c].quantile(.95))} for c in top}
payload={'summary':out,'lite':lm,'features':top,'trees':trees,'examples':ex,'desc':desc}
with open(OUT,'w',encoding='utf-8') as fh:
    fh.write('// Generado por modelo/train_model.py — no editar a mano\nwindow.FS_DATA = '+json.dumps(payload,ensure_ascii=False,separators=(',',':'))+';\n')
print('Modelo exportado a',OUT)
print(top); print(ex); print(json.dumps(desc,indent=0)[:1500])
