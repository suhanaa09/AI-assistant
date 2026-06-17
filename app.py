import streamlit as st
import base64
import io
import re
import time
from PIL import Image

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multimodal AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
  }

  /* Hide default Streamlit header */
  #MainMenu, footer, header { visibility: hidden; }

  /* App background */
  .stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    min-height: 100vh;
  }

  /* Main container */
  .main .block-container {
    padding-top: 2rem;
    max-width: 900px;
  }

  /* Hero banner */
  .hero-banner {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 20px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
  }
  .hero-banner h1 {
    color: #fff;
    font-size: 2rem;
    font-weight: 700;
    margin: 0 0 0.4rem 0;
    letter-spacing: -0.5px;
  }
  .hero-banner p {
    color: rgba(255,255,255,0.82);
    font-size: 0.95rem;
    margin: 0;
  }

  /* Cards */
  .card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(10px);
  }
  .card-label {
    color: rgba(255,255,255,0.5);
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
  }

  /* Mode pill */
  .mode-pill {
    display: inline-block;
    background: linear-gradient(90deg, #667eea, #764ba2);
    color: white;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 3px 12px;
    border-radius: 20px;
    letter-spacing: 0.5px;
    margin-bottom: 1rem;
  }

  /* Answer box */
  .answer-box {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(102,126,234,0.35);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    color: rgba(255,255,255,0.92);
    font-size: 0.97rem;
    line-height: 1.75;
    white-space: pre-wrap;
    word-wrap: break-word;
  }

  /* Web sources box */
  .sources-box {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    color: rgba(255,255,255,0.65);
    font-size: 0.82rem;
    font-family: 'JetBrains Mono', monospace;
    white-space: pre-wrap;
    margin-top: 0.8rem;
  }

  /* Processing animation */
  .processing-container {
    background: rgba(102,126,234,0.12);
    border: 1px solid rgba(102,126,234,0.3);
    border-radius: 14px;
    padding: 2rem;
    text-align: center;
  }
  .processing-step {
    color: rgba(255,255,255,0.8);
    font-size: 0.92rem;
    margin: 0.5rem 0;
    animation: fadeInUp 0.4s ease forwards;
  }
  @keyframes fadeInUp {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  /* Capability badges */
  .badge-row { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.5rem; }
  .badge {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.14);
    color: rgba(255,255,255,0.75);
    font-size: 0.75rem;
    padding: 4px 10px;
    border-radius: 20px;
  }

  /* Sidebar */
  [data-testid="stSidebar"] {
    background: rgba(15,12,41,0.9);
    border-right: 1px solid rgba(255,255,255,0.06);
  }
  [data-testid="stSidebar"] .stMarkdown p,
  [data-testid="stSidebar"] .stMarkdown li,
  [data-testid="stSidebar"] label {
    color: rgba(255,255,255,0.75) !important;
  }
  [data-testid="stSidebar"] h3 {
    color: #667eea !important;
  }

  /* Inputs */
  .stTextArea textarea {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 12px !important;
    color: #fff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
  }
  .stTextArea textarea:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 2px rgba(102,126,234,0.3) !important;
  }
  .stTextArea textarea::placeholder { color: rgba(255,255,255,0.3) !important; }

  /* Buttons */
  .stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.55rem 1.4rem !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 15px rgba(102,126,234,0.3) !important;
  }
  .stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(102,126,234,0.5) !important;
  }
  .stButton > button:active { transform: translateY(0) !important; }

  /* Clear button */
  .stButton.clear-btn > button {
    background: rgba(255,255,255,0.08) !important;
    box-shadow: none !important;
  }

  /* File uploader */
  [data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1.5px dashed rgba(255,255,255,0.15) !important;
    border-radius: 12px !important;
  }
  [data-testid="stFileUploader"] label { color: rgba(255,255,255,0.6) !important; }

  /* Info / warning boxes */
  .stAlert { border-radius: 10px !important; }

  /* Checkbox */
  .stCheckbox label { color: rgba(255,255,255,0.75) !important; }

  /* Divider */
  hr { border-color: rgba(255,255,255,0.08) !important; }

  /* Spinner */
  .stSpinner > div { border-top-color: #667eea !important; }
</style>
""", unsafe_allow_html=True)


# ── Lazy imports & client init ────────────────────────────────────────────────
@st.cache_resource
def get_clients(groq_key: str, tavily_key: str):
    from groq import Groq
    from tavily import TavilyClient
    return Groq(api_key=groq_key), TavilyClient(api_key=tavily_key)


# ── Constants ─────────────────────────────────────────────────────────────────
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
TEXT_MODEL   = "llama-3.3-70b-versatile"

WEB_TRIGGERS = [
    r'\b(latest|recent|current|today|now|2024|2025|news|update)\b',
    r'\b(who is|what is the price|stock|weather|release date)\b',
    r'\b(search|look up|find|google)\b',
]


# ── Core engine ───────────────────────────────────────────────────────────────
def needs_web_search(query: str) -> bool:
    q = query.lower()
    return any(re.search(p, q) for p in WEB_TRIGGERS)


def encode_image(pil_image: Image.Image) -> str:
    buf = io.BytesIO()
    pil_image.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def web_search(tavily_client, query: str, max_results: int = 3) -> str:
    try:
        results = tavily_client.search(
            query=query, search_depth="basic", max_results=max_results
        )
        snippets = []
        for i, r in enumerate(results.get("results", []), 1):
            snippets.append(
                f"[{i}] {r['title']}\n    {r['url']}\n    {r.get('content','')[:300]}..."
            )
        return "\n\n".join(snippets) if snippets else "No results found."
    except Exception as e:
        return f"Web search failed: {e}"


def analyze_image(groq_client, pil_image: Image.Image, question: str) -> str:
    b64 = encode_image(pil_image)
    response = groq_client.chat.completions.create(
        model=VISION_MODEL,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                {"type": "text", "text": question},
            ],
        }],
        max_tokens=1024,
        temperature=0.7,
    )
    return response.choices[0].message.content


def text_qa(groq_client, question: str, context: str = "") -> str:
    system = (
        "You are a helpful, knowledgeable AI assistant. "
        "Give clear, well-structured, and friendly answers. "
        "Use bullet points or numbered lists when helpful. "
        "Be accurate and concise."
    )
    if context:
        system += (
            "\n\nUse the following web search results to answer. Cite sources like [1].\n\n"
            "WEB CONTEXT:\n" + context
        )
    response = groq_client.chat.completions.create(
        model=TEXT_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": question},
        ],
        max_tokens=1024,
        temperature=0.7,
    )
    return response.choices[0].message.content


def combined_query(
    groq_client, tavily_client, question: str,
    pil_image=None, force_web: bool = False,
    status_container=None
) -> dict:
    web_context = ""
    do_web = force_web or needs_web_search(question)
    steps_done = []

    def update_status(icon: str, msg: str):
        steps_done.append(f"{icon} {msg}")
        if status_container:
            with status_container:
                st.empty()
                html = "<div class='processing-container'>"
                html += "<p style='color:rgba(255,255,255,0.5);font-size:0.8rem;margin-bottom:1rem;'>PROCESSING YOUR REQUEST</p>"
                for step in steps_done:
                    html += f"<p class='processing-step'>{step}</p>"
                html += "<p class='processing-step' style='opacity:0.5'>⏳ Please wait...</p>"
                html += "</div>"
                st.markdown(html, unsafe_allow_html=True)

    update_status("🧠", "Understanding your question...")
    time.sleep(0.3)

    if do_web:
        update_status("🌐", f"Searching the web for: *{question[:60]}*")
        web_context = web_search(tavily_client, question)
        update_status("✅", "Web search complete")

    if pil_image is not None:
        update_status("🖼️", "Analyzing your image with Vision AI...")
        vision_answer = analyze_image(groq_client, pil_image, question)

        if do_web:
            mode = "Image + Web Search"
            update_status("💬", "Synthesizing vision & web results...")
            prompt = (
                f"User asked: '{question}'\n\n"
                f"Vision analysis:\n{vision_answer}\n\n"
                f"Web context:\n{web_context}\n\n"
                "Synthesize a comprehensive, friendly answer from both."
            )
            answer = text_qa(groq_client, prompt)
        else:
            mode = "Image Analysis"
            answer = vision_answer
    else:
        mode = "Web Search + LLM" if do_web else "LLM Only"
        update_status("💬", "Generating your answer...")
        answer = text_qa(groq_client, question, context=web_context)

    update_status("✨", "Answer ready!")
    return {"answer": answer, "web_context": web_context, "mode": mode}


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.markdown("---")

    groq_key   = st.text_input("Groq API Key", type="password",
                                placeholder="gsk_...",
                                help="Get yours at console.groq.com")
    tavily_key = st.text_input("Tavily API Key", type="password",
                                placeholder="tvly-...",
                                help="Free at tavily.com — 1000 searches/month")

    st.markdown("---")
    st.markdown("### 🎛️ Options")
    force_web = st.checkbox("Force web search", value=False,
                             help="Always search the web, even for plain questions")

    st.markdown("---")
    st.markdown("### 🤖 Models")
    st.markdown(f"""
<div style='color:rgba(255,255,255,0.55);font-size:0.8rem;line-height:1.8'>
  <b style='color:rgba(255,255,255,0.75)'>Vision</b><br>
  {VISION_MODEL.split('/')[-1]}<br><br>
  <b style='color:rgba(255,255,255,0.75)'>Text</b><br>
  {TEXT_MODEL}
</div>
""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.markdown("""
<div style='color:rgba(255,255,255,0.55);font-size:0.8rem;line-height:1.8'>
  • Ask anything — text, image, or both<br>
  • Mention <i>latest / 2025 / today</i> to trigger web search automatically<br>
  • Upload an image and ask questions about it<br>
  • Check <i>Force web search</i> for any real-time info
</div>
""", unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
  <h1>🤖 Multimodal AI Assistant</h1>
  <p>Ask anything · Upload images · Get intelligent answers powered by Groq</p>
  <div class="badge-row" style="margin-top:1rem">
    <span class="badge">🖼️ Vision QA</span>
    <span class="badge">🌐 Live Web Search</span>
    <span class="badge">💬 LLM Chat</span>
    <span class="badge">⚡ Groq Powered</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ── API key gate ──────────────────────────────────────────────────────────────
if not groq_key or not tavily_key:
    st.markdown("""
<div class="card">
  <div class="card-label">Get Started</div>
  <p style="color:rgba(255,255,255,0.7);margin:0;font-size:0.92rem">
    👈 Enter your <strong style="color:#667eea">Groq</strong> and 
    <strong style="color:#764ba2">Tavily</strong> API keys in the sidebar to begin.
    <br><br>
    • <a href="https://console.groq.com" target="_blank" style="color:#667eea">Get Groq API key (free)</a><br>
    • <a href="https://tavily.com" target="_blank" style="color:#764ba2">Get Tavily API key (free)</a>
  </p>
</div>
""", unsafe_allow_html=True)
    st.stop()


# ── Init clients (cached) ─────────────────────────────────────────────────────
try:
    groq_client, tavily_client = get_clients(groq_key, tavily_key)
except Exception as e:
    st.error(f"Failed to initialise clients: {e}")
    st.stop()


# ── Main interface ────────────────────────────────────────────────────────────
col_main, col_img = st.columns([3, 2], gap="large")

with col_main:
    st.markdown('<div class="card-label">YOUR QUESTION</div>', unsafe_allow_html=True)
    question = st.text_area(
        label="question",
        placeholder="e.g.  What's in this image?\nWhat are the latest AI models in 2025?\nExplain quantum computing simply.",
        height=130,
        label_visibility="collapsed",
        key="question_input",
    )

    btn_col1, btn_col2, btn_col3 = st.columns([2, 1, 3])
    with btn_col1:
        run_btn = st.button("▶ Ask Now", use_container_width=True)
    with btn_col2:
        clear_btn = st.button("🗑 Clear", use_container_width=True)

with col_img:
    st.markdown('<div class="card-label">UPLOAD IMAGE (OPTIONAL)</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        label="image",
        type=["jpg", "jpeg", "png", "webp", "gif"],
        label_visibility="collapsed",
        help="Upload an image to ask questions about it",
    )
    if uploaded_file:
        pil_image = Image.open(uploaded_file).convert("RGB")
        st.image(pil_image, use_container_width=True, caption=f"📎 {uploaded_file.name}")
    else:
        pil_image = None
        st.markdown("""
<div style='text-align:center;padding:2rem 1rem;color:rgba(255,255,255,0.25);font-size:0.85rem;
            border:1.5px dashed rgba(255,255,255,0.1);border-radius:12px;margin-top:0.2rem'>
  🖼️<br>Drop an image here<br>or click to browse
</div>
""", unsafe_allow_html=True)


# ── Clear ─────────────────────────────────────────────────────────────────────
if clear_btn:
    st.session_state.pop("result", None)
    st.session_state.pop("question_input", None)
    st.rerun()


# ── Run query ─────────────────────────────────────────────────────────────────
if run_btn:
    q = question.strip()
    if not q:
        st.warning("⚠️ Please type a question first.")
    else:
        st.markdown("---")
        status_placeholder = st.empty()

        try:
            result = combined_query(
                groq_client=groq_client,
                tavily_client=tavily_client,
                question=q,
                pil_image=pil_image,
                force_web=force_web,
                status_container=status_placeholder,
            )
            st.session_state["result"] = result
            st.session_state["last_question"] = q
        except Exception as e:
            status_placeholder.empty()
            st.error(f"❌ Something went wrong: {e}")
            st.info("Check that your API keys are correct and have sufficient quota.")

        status_placeholder.empty()


# ── Show stored result ────────────────────────────────────────────────────────
if "result" in st.session_state:
    res = st.session_state["result"]
    q   = st.session_state.get("last_question", "")

    st.markdown("---")

    # Question echo
    st.markdown(f"""
<div class="card" style="margin-bottom:0.8rem">
  <div class="card-label">YOUR QUESTION</div>
  <p style="color:rgba(255,255,255,0.85);margin:0;font-size:0.95rem">{q}</p>
</div>
""", unsafe_allow_html=True)

    # Mode badge + answer
    mode_emoji = {
        "LLM Only": "💬",
        "Web Search + LLM": "🌐",
        "Image Analysis": "🖼️",
        "Image + Web Search": "🖼️🌐",
    }.get(res["mode"], "🤖")

    st.markdown(f"""
<div class="card">
  <div class="card-label">ANSWER</div>
  <div class="mode-pill">{mode_emoji} {res["mode"]}</div>
  <div class="answer-box">{res["answer"]}</div>
</div>
""", unsafe_allow_html=True)

    # Web sources (collapsible)
    if res.get("web_context") and res["web_context"] != "No results found.":
        with st.expander("🌐 View Web Sources", expanded=False):
            st.markdown(f'<div class="sources-box">{res["web_context"]}</div>',
                        unsafe_allow_html=True)

    # Copy to clipboard hint
    st.markdown("""
<p style='color:rgba(255,255,255,0.25);font-size:0.75rem;text-align:center;margin-top:0.5rem'>
  Select the answer text above to copy it
</p>
""", unsafe_allow_html=True)
