
import pytest
from pathlib import Path
from reportlab.pdfgen import canvas

from rag.ingestion import load_and_split_pdf


@pytest.fixture
def sample_pdf(tmp_path):
    """Create a temporary PDF for testing."""
    pdf_path = tmp_path / "test_document.pdf"

    pdf = canvas.Canvas(str(pdf_path))
    pdf.drawString(
        100, 750,
        "Northstar Retail generated GBP 12.4 million in revenue."
    )
    pdf.save()

    return pdf_path


def test_pdf_loading(sample_pdf):
    chunks = load_and_split_pdf(str(sample_pdf))

    assert len(chunks) > 0
    assert "Northstar Retail" in chunks[0].page_content


def test_pdf_metadata(sample_pdf):
    chunks = load_and_split_pdf(str(sample_pdf))

    assert chunks[0].metadata["page"] == 0


def test_missing_pdf():
    with pytest.raises(FileNotFoundError):
        load_and_split_pdf("nonexistent_document.pdf")


def test_pdf_chunks_contain_text(sample_pdf):
    chunks = load_and_split_pdf(str(sample_pdf))

    for chunk in chunks:
        assert chunk.page_content.strip() != ""
