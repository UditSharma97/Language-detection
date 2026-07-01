const API_BASE = "http://127.0.0.1:8000";

// Navigation
const navDetect = document.getElementById('nav-detect');
const navAbout = document.getElementById('nav-about');
const detectPage = document.getElementById('detect-page');
const aboutPage = document.getElementById('about-page');

navDetect.addEventListener('click', ()=>{
  navDetect.classList.add('active');
  navAbout.classList.remove('active');
  detectPage.classList.remove('hidden');
  aboutPage.classList.add('hidden');
});
navAbout.addEventListener('click', ()=>{
  navAbout.classList.add('active');
  navDetect.classList.remove('active');
  aboutPage.classList.remove('hidden');
  detectPage.classList.add('hidden');
});

// Elements
const inputText = document.getElementById('inputText');
const detectBtn = document.getElementById('detectBtn');
const translateBtn = document.getElementById('translateBtn');
const targetLang = document.getElementById('targetLang');
const languageResult = document.getElementById('languageResult');
const translationResult = document.getElementById('translationResult');

// Helpers
async function postJSON(path, payload){
  const res = await fetch(API_BASE + path, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload)
  });
  return await res.json();
}

// Detect
detectBtn.addEventListener('click', async ()=>{
  const text = inputText.value.trim();
  if(!text){ alert('Please enter text'); return }
  languageResult.textContent = 'Detecting...';
  try{
    const data = await postJSON('/detect', {text});
    languageResult.textContent = `${data.language} (confidence: ${data.confidence.toFixed(3)})`;
  }catch(e){
    languageResult.textContent = 'Error: ' + e.message;
  }
});

// Translate
translateBtn.addEventListener('click', async ()=>{
  const text = inputText.value.trim();
  const target = targetLang.value;
  if(!text){ alert('Please enter text'); return }
  translationResult.textContent = 'Translating...';
  try{
    const data = await postJSON('/translate', {text, target_lang: target});
    if(data.error){
      translationResult.textContent = 'Error: ' + (data.error || JSON.stringify(data));
    }else{
      translationResult.textContent = data.translated_text || JSON.stringify(data);
    }
  }catch(e){
    translationResult.textContent = 'Error: ' + e.message;
  }
});

// Shortcut: Ctrl+Enter to translate
inputText.addEventListener('keydown', (e)=>{
  if(e.ctrlKey && e.key === 'Enter'){
    translateBtn.click();
  }
});
