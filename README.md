Language Detection and Translation System Using ML and TransformersAn enterprise-grade, full-stack web application designed to automatically identify the source language of text inputs across 22 supported languages and instantly translate them into fluent, grammatically correct English. The architecture implements a highly optimized hybrid pipeline: a lightweight classical Machine Learning classifier handles high-speed language detection, while state-of-the-art pretrained Transformer networks handle context-aware machine translation.  This decoupled architecture ensures high computational throughput and near-instant processing, making it an ideal infrastructure pattern for globalized, real-time multilingual communication platforms.  🚀 Key FeaturesAutomated Language Identification: Accurately classifies source text across 22 global languages spanning 11 language families and 10 distinct scripts.  Context-Aware Translation: Generates production-ready English translations leveraging sequence-to-sequence neural architectures.  Sub-2-Second Performance Target: The end-to-end processing pipeline executes in under 2 seconds, with the language detection stage completing in less than 100ms.  Intelligent Memory Management: Implements lazy-loading and in-memory caching for heavy transformer checkpoints to minimize memory footprint and eliminate runtime model initialization overhead.  Minimalist Frontend Interface: Framework-free client layout utilizing native browser APIs and compositor-driven CSS animations to achieve a consistent 60 FPS visual state.  🛠️ Technical StackCore Engineering Language: Python 3.8+  Machine Learning Ecosystem: scikit-learn (Multinomial Naive Bayes, CountVectorizer), HuggingFace Transformers, PyTorch, SentencePiece.  Backend REST API: FastAPI, Uvicorn (ASGI Server), Pydantic (Data Validation and Schema Enforcement).  Frontend Client: Native HTML5, CSS3, Vanilla JavaScript (ES6+ Asynchronous Fetch API).  Validation Frameworks: pandas, numpy, pytest, httpx.  📂 System Topology & Directory LayoutThe workspace partitions data-science research, runtime deployment, and user interface concerns in alignment with modern microservice design conventions as documented in the original project report Language_Detection_and_Translation_System_Using_ML_and_Transformers_60pg.docx:  Plaintextlanguage-detection/
│
├── data/
│   └── language.csv              # Balanced training dataset (22,000 target samples)
│
├── research/
│   └── train.ipynb               # Data exploration, feature engineering & model training
│
├── backend/
│   ├── app.py                    # FastAPI application configuration and route orchestration
│   ├── model/
│   │   ├── model.pkl             # Serialized Naive Bayes classification artifact
│   │   └── vectorizer.pkl        # Serialized CountVectorizer vocabulary artifact
│   ├── utils/
│   │   └── language_mapping.py   # Token labels to HuggingFace model identifier lookups
│   └── requirements.txt          # Frozen, version-pinned microservice dependencies
│
└── frontend/
    ├── index.html                # Client presentation layout
    ├── style.css                 # Interface layout and theme stylesheets
    └── script.js                 # Network request lifecycles and dynamic DOM manipulation
🗺️ Supported Language MatrixThe system features an identical 1,000-sample balanced distribution across all of the following 22 languages to eliminate majority-class bias during model optimization:  Latin Scripts: English, Spanish, French, Portuguese, Romanian, Dutch, Swedish, Estonian, Turkish, Indonesian, Latin.  Cyrillic Script: Russian.  Sino-Tibetan & East Asian Scripts: Chinese (Hanzi), Japanese (Kanji/Kana), Korean (Hangul).  South Asian & Brahmic Scripts: Hindi (Devanagari), Tamil.  Southeast Asian Script: Thai.  Perso-Arabic Scripts: Arabic, Persian, Pushto, Urdu (Nastaliq).  ⚙️ Core Pipeline Architecture1. Language Detection EngineThe detection microservice uses a Multinomial Naive Bayes classifier operating over log-space transformations to guarantee numeric stability:  $$ĉ = \text{argmax}_c \left[ \log P(c) + \sum x_i \cdot \log P(w_i | c) \right]$$Text inputs are mapped to sparse token count fields using a CountVectorizer initialized with a (1, 2) n-gram range. Unigrams handle explicit function word signatures while bigrams retain crucial short-range orthographic and lexical structures.  2. Neural Machine TranslationOnce classified, payloads are routed to dedicated sequence-to-sequence Helsinki-NLP OPUS-MT Transformer checkpoints. These utilize a scaled dot-product multi-head self-attention layout to evaluate global context and handle long-range token dependencies:  $$\text{Attention}(Q, K, V) = \text{softmax}\left( \frac{QK^T}{\sqrt{d_k}} \right)V$$🛠️ Local Development & DeploymentStep 1: Install Python DependenciesIsolate your runtime environment and install the required frozen dependency stack from within the backend directory:  Bashcd backend
pip install -r requirements.txt
Step 2: Execute Offline Model OptimizationTrain the classification model and write the required binary inference artifacts to disk:  Bashcd ../research
jupyter notebook train.ipynb
Execute all notebook frames to output model.pkl and vectorizer.pkl directly into the backend/model/ target destination.  Step 3: Bootstrap the FastAPI ServerLaunch the ASGI application container to bind and activate network interfaces:  Bashcd ../backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
The complete interactive OpenAPI specification is instantly accessible for validation at http://localhost:8000/docs.  Step 4: Launch the Frontend Web ClientServe the static assets contained inside the frontend/ directory using your standard web server choice or open index.html within a modern web browser to initiate client tasks.  📡 API Reference SpecificationsGet Service HealthHTTPGET /health
Response (200 OK):JSON{
  "status": "healthy",
  "model_loaded": true,
  "vectorizer_loaded": true
}
Combined Detection and Translation PipelineHTTPPOST /detect-and-translate
Payload Configuration:JSON{
  "text": "こんにちは、元気ですか？"
}
Response (200 OK):JSON{
  "detected_language": "Japanese",
  "translation": "Hello, how are you?"
}
🧪 Automated Test ExecutionThe system features structured unit testing via pytest and FastAPI's isolated mock client layers to guarantee application consistency across builds. Execute the automated validation engine by running:  Bashpytest
The test coverage profiles verify structural validation compliance (HTTP 422), error handling patterns under unmapped locale parameters (HTTP 400), and basic endpoint response structure integrity. 
