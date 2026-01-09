"""
File reader utilities for different file formats.
"""
from pathlib import Path
from typing import Optional


def read_file_content(file_path: Path) -> Optional[str]:
    """
    Read content from various file formats.

    Supports:
    - Plain text (.txt, .md)
    - Microsoft Word (.docx)

    Args:
        file_path: Path to file to read

    Returns:
        File content as string, or None if unsupported/unreadable
    """
    suffix = file_path.suffix.lower()

    # Plain text files
    if suffix in ['.txt', '.md', '']:
        try:
            return file_path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                return file_path.read_text(encoding='latin-1')
            except Exception:
                return None
        except Exception:
            return None

    # Microsoft Word documents
    elif suffix == '.docx':
        try:
            import docx
            doc = docx.Document(str(file_path))
            paragraphs = [para.text for para in doc.paragraphs]
            return '\n'.join(paragraphs)
        except ImportError:
            print(f"Warning: python-docx not installed. Cannot read {file_path.name}")
            print("Install with: pip install python-docx")
            return None
        except Exception as e:
            print(f"Error reading Word document {file_path.name}: {e}")
            return None

    # PDF files (future support)
    elif suffix == '.pdf':
        print(f"PDF files not yet supported: {file_path.name}")
        return None

    # Unsupported format
    else:
        print(f"Unsupported file format: {file_path.name}")
        return None
