# Language Detection and Translation System

A full-stack web application that automatically detects the language of user input and translates it into English using a hybrid Machine Learning and Transformer-based architecture.

The application combines a **Multinomial Naive Bayes** classifier for fast language detection with **Hugging Face Helsinki-NLP Transformer models** for accurate, context-aware translation.

---

## Features

- Detects text in **22 languages**
- Translates detected text into English
- Fast language detection using Machine Learning
- Context-aware translation using Transformer models
- REST API built with FastAPI
- Clean and responsive web interface
- Input validation using Pydantic
- Automated testing with Pytest

---

## Tech Stack

### Backend
- Python
- FastAPI
- Uvicorn
- Pydantic

### Machine Learning
- Scikit-learn
- Multinomial Naive Bayes
- CountVectorizer

### Translation
- Hugging Face Transformers
- PyTorch
- Helsinki-NLP OPUS-MT Models

### Frontend
- HTML
- CSS
- JavaScript

### Testing
- Pytest
- HTTPX

---

## Project Structure

```
language-detection/
│
├── backend/
│   ├── app.py
│   ├── model/
│   ├── utils/
│   └── requirements.txt
│
├── data/
│   └── language.csv
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── research/
│   └── train.ipynb
│
└── README.md
```

---

## Supported Languages

The system supports 22 languages, including:

- English
- Spanish
- French
- Portuguese
- Romanian
- Dutch
- Swedish
- Estonian
- Turkish
- Indonesian
- Latin
- Russian
- Chinese
- Japanese
- Korean
- Hindi
- Tamil
- Thai
- Arabic
- Persian
- Pushto
- Urdu

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/language-detection.git

cd language-detection
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment.

**Windows**

```bash
.venv\Scripts\activate
```

**Linux/macOS**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
cd backend

pip install -r requirements.txt
```

---

## Train the Model

Run the training notebook inside the `research` folder.

```bash
jupyter notebook train.ipynb
```

The notebook generates:

- `model.pkl`
- `vectorizer.pkl`

These files should be placed inside:

```
backend/model/
```

---

## Run the Application

Start the FastAPI server:

```bash
cd backend

uvicorn app:app --reload
```

The API will be available at:

```
http://localhost:8000
```

Swagger documentation:

```
http://localhost:8000/docs
```

Open `frontend/index.html` in your browser to use the web interface.

---

## API Endpoints

### Health Check

```
GET /health
```

Example response:

```json
{
  "status": "healthy",
  "model_loaded": true,
  "vectorizer_loaded": true
}
```

---

### Detect and Translate

```
POST /detect-and-translate
```

Request:

```json
{
  "text": "こんにちは"
}
```

Response:

```json
{
  "detected_language": "Japanese",
  "translation": "Hello"
}
```

---

## Testing

Run the test suite:

```bash
pytest
```

---

## Future Improvements

- Support translation between multiple target languages
- Docker deployment
- CI/CD pipeline
- Translation history
- Confidence scores for predictions
- Batch translation

---

## License

This project is licensed under the MIT License.
