import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def ensure_pdf_conversion(file_path: Path) -> Path:
    """Convert file to PDF using ebook-convert if necessary."""
    if file_path.suffix.lower() == ".pdf":
        print(f"File is already PDF: {file_path}")
        return file_path

    # Check for ebook-convert in order:
    # 1. CALIBRE_PATH from .env
    # 2. PATH
    # 3. Common Windows path
    ebook_convert = os.getenv("CALIBRE_PATH")
    if ebook_convert and not Path(ebook_convert).exists():
        ebook_convert = None

    if not ebook_convert:
        ebook_convert = shutil.which("ebook-convert")

    if not ebook_convert:
        common_path = r"C:\Program Files\Calibre2\ebook-convert.exe"
        if Path(common_path).exists():
            ebook_convert = common_path

    if not ebook_convert:
        print("Error: 'ebook-convert' not found in PATH.", file=sys.stderr)
        print("Please install Calibre to enable auto-conversion.", file=sys.stderr)
        return file_path

    output_path = file_path.with_suffix(".pdf")
    print(f"Converting {file_path.name} to PDF...")

    try:
        subprocess.run(
            [ebook_convert, str(file_path), str(output_path)],
            check=True,
            stdout=subprocess.DEVNULL,  # Suppress Calibre's verbose output
            stderr=subprocess.PIPE
        )
        if output_path.exists():
            print(f"Conversion successful: {output_path}")
            return output_path
        else:
            print(f"Conversion command finished but output file missing: {output_path}", file=sys.stderr)
            return file_path
    except subprocess.CalledProcessError as e:
        print(f"Conversion failed: {e}", file=sys.stderr)
        if e.stderr:
            print(f"Error details: {e.stderr.decode('utf-8', errors='ignore')}", file=sys.stderr)
        return file_path


def main():
    # Set console encoding to utf-8 for Windows
    if sys.platform.startswith("win"):
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

    parser = argparse.ArgumentParser(description="Convert ebook files to PDF using Calibre")
    parser.add_argument("file", help="Path to file to convert")
    args = parser.parse_args()

    file_path = Path(args.file).resolve()
    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    result_path = ensure_pdf_conversion(file_path)
    # Output the result path for downstream tools
    print(f"::set-output name=pdf_path::{result_path}")


if __name__ == "__main__":
    main()
