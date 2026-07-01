from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import langid
from transformers import MarianMTModel, MarianTokenizer
from typing import Dict
import torch

# ----------------------
# FastAPI setup
# ----------------------
app = FastAPI(title="Language Detection + Translation API")

# Allow CORS for local development (change in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------
# Request models
# ----------------------
class TextRequest(BaseModel):
    text: str
    target_lang: str = "en"  # e.g. 'en', 'hi', 'es', 'fr'

# ----------------------
# Model management / cache
# ----------------------
# We'll lazily load translation models and cache them in memory.
MODEL_CACHE: Dict[str, Dict[str, object]] = {}

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

def load_translation_model(model_name: str):
    """Load tokenizer+model for given HF model name and cache them."""
    if model_name in MODEL_CACHE:
        return MODEL_CACHE[model_name]

    print(f"Loading model: {model_name}")
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    model.to(DEVICE)
    MODEL_CACHE[model_name] = {"tokenizer": tokenizer, "model": model}
    return MODEL_CACHE[model_name]

def get_model_name_for_pair(src: str, tgt: str):
    """Return a likely Helsinki-NLP model name for src->tgt or None if not found.
    We try a few heuristics. This function doesn't check model existence remotely —
    transformers will throw if model name isn't valid.
    """
    # direct pair
    direct = f"Helsinki-NLP/opus-mt-{src}-{tgt}"
    return direct

# A utility translation function using a specific HF model
def translate_with_model(texts, tokenizer, model, max_length=512):
    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=max_length)
    inputs = {k: v.to(DEVICE) for k, v in inputs.items()}
    translated = model.generate(**inputs, max_length=max_length)
    outputs = [tokenizer.decode(t, skip_special_tokens=True) for t in translated]
    return outputs

# ----------------------
# Endpoints
# ----------------------
@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/detect")
async def detect_language(req: TextRequest):
    text = req.text or ""
    lang, score = langid.classify(text)
    return {"language": lang, "confidence": float(score)}

@app.post("/translate")
async def translate(req: TextRequest):
    text = req.text or ""
    target = req.target_lang or "en"

    # Detect source language first
    src_lang, _ = langid.classify(text)

    # Quick path: translate any -> English using the multilingual->en model
    if target == "en":
        model_name = "Helsinki-NLP/opus-mt-mul-en"
        m = load_translation_model(model_name)
        out = translate_with_model([text], m["tokenizer"], m["model"])
        return {"source": src_lang, "target": target, "translated_text": out[0]}

    # If source is English and target != en, try en->target
    if src_lang == "en":
        model_name = f"Helsinki-NLP/opus-mt-en-{target}"
        try:
            m = load_translation_model(model_name)
            out = translate_with_model([text], m["tokenizer"], m["model"])
            return {"source": src_lang, "target": target, "translated_text": out[0]}
        except Exception as e:
            # model may not exist — fall back to en->* via an error message
            return {"error": f"No direct en->{target} model available (tried {model_name}).", "details": str(e)}

    # If source != en and target != en, attempt two-step: src -> en -> tgt
    try:
        model_src_en = "Helsinki-NLP/opus-mt-mul-en"
        m1 = load_translation_model(model_src_en)
        mid = translate_with_model([text], m1["tokenizer"], m1["model"])[0]

        # try en->target
        model_en_tgt = f"Helsinki-NLP/opus-mt-en-{target}"
        try:
            m2 = load_translation_model(model_en_tgt)
            final = translate_with_model([mid], m2["tokenizer"], m2["model"])[0]
            return {"source": src_lang, "target": target, "translated_text": final}
        except Exception as e:
            # If we cannot find en->target, return the intermediate English translation
            return {"source": src_lang, "target": target, "translated_text": mid, "note": "Partial translation (source -> English). Failed to find English->target model.", "details": str(e)}

    except Exception as e:
        return {"error": "Translation failed", "details": str(e)}
