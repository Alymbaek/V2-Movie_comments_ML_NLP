🎬 Spoiler Detection in Russian Movie Comments (NLP) — v2
📬 Contacts

Alymbek Ibragimov
LinkedIn: https://www.linkedin.com/in/alymbek-ibragimov-447876336/

Goal. Detect whether a Russian movie comment contains a spoiler or no_spoiler.
Stack. Python · scikit-learn · NLTK · razdel · Mystem · Django REST Framework · Gradio

This is v2: adds lemmatization + TF-IDF n-grams, a small Gradio demo (with API), and a cleaner repo structure.

✨ What’s new in v2

🧠 Text processing: lowercasing → Russian stop-words → lemmatization (Mystem)

🔠 Features: TF-IDF, n-grams (1–2)

📈 Evaluation: train/test split + (optional) cross-validation

🧩 Artifacts: spoiler_detector.pkl (model), vec.pkl (vectorizer)

🧪 Demo: Gradio UI + programmatic access via gradio_client

🧰 DRF integration: minimal classifier endpoint (example below)

📂 Repository structure
.
├── Movie_comments_NLP_v2.ipynb        # training & evaluation (v2)
├── movie_comments.csv                 # sample dataset (text,label)
├── spoiler_detector.pkl               # trained classifier
├── vec.pkl                            # TF-IDF vectorizer (with lemmatizer analyzer)
├── moviesite/                         # Django REST backend (DRF)
│   └── movie/
│       ├── serializers.py             # uses model + vectorizer
│       └── nlp_utils.py               # lemma_tokens() (recommended)
├── demo_app.py                        # simple Gradio demo (optional)
├── requirements.txt
└── README.md


⚠️ If your vectorizer was trained with a custom analyzer (e.g. lemma_tokens), 
keep the same function available at load time. 
Best practice: put it in movie/nlp_utils.py and import from there both in training and serving.

📊 Dataset

CSV with columns: text, label where label ∈ {spoiler, no_spoiler}

Language: Russian

Class balance: ~50/50

Example rows:

text,label
"Фильм отличный, но в конце герой...",spoiler
"Очень красивая картинка, саунд супер",no_spoiler
"Антагонист на самом деле отец главного героя",spoiler


Dataset file: movie_comments.csv

🧪 Method (v2)

Preprocessing: lowercasing, NLTK Russian stop-words, lemmatization (Mystem + razdel)

Features: TF-IDF, n-grams (1, 2)

Model: MultinomialNB (baseline)

Split: train_test_split(test_size=0.2, random_state=42)

(Optional) Cross-validation for more robust estimates

Note: very high scores may indicate an easy dataset or leakage; prefer CV and additional tests.

🚀 Quickstart
1) Create environment & install deps
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt


If you trained on a specific scikit-learn version, pin it (e.g. scikit-learn==1.7.0) to avoid unpickle warnings.

2) Run the Gradio demo locally (optional)

demo_app.py (already in repo — or create):

import sys, joblib, gradio as gr
from movie.nlp_utils import lemma_tokens  # the SAME function used in training

# Make the analyzer importable if pickled as __main__.lemma_tokens
sys.modules['__main__'].lemma_tokens = lemma_tokens

vec = joblib.load('vec.pkl')
clf = joblib.load('spoiler_detector.pkl')

def predict(text: str):
    return clf.predict(vec.transform([text]))[0]

demo = gr.Interface(
    fn=predict,
    inputs=gr.Textbox(label="Comment (RU)"),
    outputs=gr.Label(label="Prediction"),
    title="Spoiler Detection (RU)"
)
demo.launch(share=True)  # share=True gives a temporary public URL


Run:

python demo_app.py


You’ll see a local UI and (with share=True) a temporary public URL like https://xxxx.gradio.live.

3) Call the demo programmatically (gradio_client)
from gradio_client import Client

client = Client("https://YOUR-SHARE-LINK.gradio.live/")
result = client.predict(
    text="Он умирает в финале...",  # your comment text
    api_name="/predict"            # keep as shown in the notebook/Demo
)
print(result)


The share link expires in ~1 week. For a permanent URL, deploy to Hugging Face Spaces (or your own host).

🧩 Django REST API (DRF)

Put artifacts (spoiler_detector.pkl, vec.pkl) into the Django project base dir (or adjust paths in serializers.py).

Ensure your analyzer function is importable in Django:

moviesite/movie/nlp_utils.py (example)

import re
from razdel import tokenize
from pymystem3 import Mystem

_mystem = Mystem()

def lemma_tokens(text: str):
    text = text.lower()
    toks = []
    for t in tokenize(text):
        w = t.text
        if re.match(r'^[а-яё-]+$', w):
            lem = _mystem.lemmatize(w)
            if lem:
                toks.append(lem[0].strip())
    return toks


moviesite/movie/serializers.py (key part)

import os, sys, joblib
from django.conf import settings
from rest_framework import serializers
from .models import Rating
from .nlp_utils import lemma_tokens

# If pickled under __main__, also expose it
sys.modules['__main__'].lemma_tokens = lemma_tokens

BASE = settings.BASE_DIR
vec  = joblib.load(os.path.join(BASE, 'vec.pkl'))
clf  = joblib.load(os.path.join(BASE, 'spoiler_detector.pkl'))

class RatingsSimpleSerializer(serializers.ModelSerializer):
    check_comment = serializers.SerializerMethodField()

    class Meta:
        model = Rating
        fields = ['id', 'user', 'parent', 'text', 'check_comment']

    def get_check_comment(self, obj):
        return clf.predict(vec.transform([obj.text]))[0]


Run the server:

cd moviesite
python manage.py migrate
python manage.py runserver


Example request (adjust to your actual endpoint):

curl -X POST http://127.0.0.1:8000/api/check_comment/ \
  -H "Content-Type: application/json" \
  -d '{"text": "Он умирает в финале..."}'


Example response:

{"label": "spoiler"}

Accuracy ~1.00 on this small dataset; will validate with cross-validation and harder test sets in the next iteration.

🔗 Programmatic Demo (from Colab)

When launching Gradio in Colab with share=True, Colab prints a temporary public URL.
Use it with gradio_client as shown above; the api_name (usually "/predict") is printed in the cell (“Install the Python client…” card).

🧭 Roadmap

Cross-validation + additional metrics (F1, ROC-AUC)

Better cleaning/normalization, emoji/punctuation handling

Try fastText/Sentence-BERT embeddings

Optional context-aware variant (comment + short plot summary)


Tips

If you see InconsistentVersionWarning on unpickle, either:

pin the same scikit-learn version used for training, or

retrain and resave artifacts with your current version.

To avoid custom-function pickle issues, you can save a single Pipeline (Pipeline([('vec', vectorizer), ('clf', model)])) instead of separate files.
