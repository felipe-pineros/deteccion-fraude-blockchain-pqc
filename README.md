# Sistema inteligente de detección de fraude en redes blockchain con seguridad post-cuántica

El sistema analiza el historial de cada cuenta de Ethereum con Machine Learning, bloquea las transacciones de cuentas sospechosas y firma las legítimas con criptografía resistente a computadoras cuánticas antes de encadenarlas en bloques con SHA-256.

## Demo

La página es estática: no necesita servidor, base de datos ni instalación.

- **Local:** abre `index.html` con doble clic.
- **GitHub Pages:** en el repositorio ve a *Settings → Pages*, elige la rama `main` y la carpeta `/ (root)`, y guarda. La página queda en `https://<tu-usuario>.github.io/<nombre-del-repo>/`.

### Qué se puede probar

1. **Motor de IA.** Carga una cuenta real del conjunto de prueba o escribe tus propios valores. Un Random Forest de 30 árboles calcula en el navegador la probabilidad de fraude y muestra el voto de cada árbol.
2. **Blockchain post-cuántica.** Al enviar una transacción, el sistema hace cuatro pasos:
   1. La IA revisa la cuenta que envía y bloquea la transacción si parece fraudulenta.
   2. Genera un par de llaves de Lamport (firma basada en hash, resistente a ataques cuánticos).
   3. Firma la transacción y verifica la firma.
   4. Mina el bloque con prueba de trabajo (el hash debe empezar por `000`).

   Con el botón **«Alterar monto»** se simula un ataque, y la validación detecta tanto el hash roto como la firma inválida.
3. **Rendimiento.** Comparación de modelos, matriz de confusión e importancia de variables.

## Resultados

Ethereum Fraud Detection Dataset (Kaggle): 9.841 cuentas, 22 % fraudulentas. Partición 80/20 con `random_state = 42`.

| Modelo | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| Regresión logística | 81,4 % | 98,4 % | 14,3 % | 24,9 % |
| **Random Forest** | **95,9 %** | **94,4 %** | **86,4 %** | **90,2 %** |
| SVM | 78,3 % | 0,0 % | 0,0 % | 0,0 % |

El modelo ligero que corre en el navegador (30 árboles, 8 variables) obtiene 94,7 % de accuracy y 86,7 % de F1.

Con la configuración por defecto y el dataset desbalanceado, el SVM clasifica todas las cuentas como legítimas. Por eso su recall es 0.

## Estructura

```
deteccion-fraude-blockchain-pqc/
├── index.html              # Página web (HTML, CSS y JavaScript)
├── data.js                 # Modelo exportado y métricas (lo genera el script)
├── modelo/
│   ├── train_model.py      # Entrena los modelos y genera data.js
│   └── requirements.txt
├── .gitignore
└── README.md
```

## Reentrenar el modelo

1. Descarga `transaction_dataset.csv` del [Ethereum Fraud Detection Dataset](https://www.kaggle.com/datasets/vagifa/ethereum-frauddetection-dataset) y colócalo en `modelo/`. El `.gitignore` evita que el CSV se suba al repositorio.
2. Ejecuta:

```bash
cd modelo
pip install -r requirements.txt
python train_model.py
```

El script imprime las métricas de los tres modelos y sobrescribe `data.js`. Al recargar la página se usa el modelo nuevo.

## Tecnologías

- **IA:** Python, pandas, scikit-learn (Regresión logística, Random Forest, SVM).
- **Web:** HTML, CSS y JavaScript sin frameworks.
- **Criptografía:** Web Crypto API (SHA-256) y firmas de Lamport.

Las firmas de Lamport pertenecen a la familia de firmas basadas en hash que el NIST estandarizó en 2024 como SLH-DSA (FIPS 205). La implementación de esta demo es educativa: cada par de llaves se usa una sola vez y no está pensada para producción.

## Referencias

- S. Nakamoto, *Bitcoin: A Peer-to-Peer Electronic Cash System*, 2008.
- M. Conti et al., “A Survey on Security and Privacy Issues of Bitcoin,” *IEEE Communications Surveys & Tutorials*, 2018.
- T. M. Fernández-Caramés y P. Fraga-Lamas, “Towards Post-Quantum Blockchain,” 2024.
- NIST, *Post-Quantum Cryptography Project*.
- IEEE Computer Society, *SWEBOK Guide v4.0*, 2024.

## Equipo

Sharon Gómez S. · Andrés Piñeros L.
