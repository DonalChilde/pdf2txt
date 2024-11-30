"""Extract text from pdf file."""

from pathlib import Path

from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams

from pfmsoft.pdf2txt.snippets.check_file import check_file


def extract_text_from_pdf_to_file(
    file_in: Path,
    file_out: Path,
    overwrite: bool = False,
    la_params: LAParams | None = None,
):
    """Extract text from a pdf file."""
    check_file(path_out=file_out, ensure_parents=True, overwrite=overwrite)
    with (
        open(file_out, mode="w", encoding="utf-8") as fp_out,
        open(file_in, mode="rb") as fp_in,
    ):
        if la_params is None:
            la_params = LAParams()
        extract_text_to_fp(fp_in, fp_out, laparams=la_params)
