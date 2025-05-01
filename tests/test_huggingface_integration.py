import os
import tempfile
import shutil

def test_huggingface_backend():
    os.environ["P2P_LLM_BACKEND"] = "huggingface"
    hf_token = os.environ.get("HF_API_TOKEN")
    if not hf_token:
        print("⚠️  Skipping HuggingFace integration test: HF_API_TOKEN not set.")
        return

    from agents.crew import crew
    session_path = tempfile.mkdtemp(prefix="test_hf_session_")
    prompt = "Resume el siguiente texto en una frase."
    paper_path = os.path.join(os.path.dirname(__file__), "sample.pdf")
    if not os.path.exists(paper_path):
        from PyPDF2 import PdfWriter
        writer = PdfWriter()
        writer.add_blank_page(width=72, height=72)
        with open(paper_path, "wb") as f:
            writer.write(f)
    try:
        crew.run(session_path=session_path, prompt=prompt, paper_path=paper_path)
        prd_path = os.path.join(session_path, "output", "prd.md")
        assert os.path.exists(prd_path)
        with open(prd_path, encoding="utf-8") as f:
            prd_content = f.read()
        assert "# Product Requirements Document" in prd_content
        print("✅ HuggingFace integration test passed.")
    finally:
        shutil.rmtree(session_path)

if __name__ == "__main__":
    test_huggingface_backend()
