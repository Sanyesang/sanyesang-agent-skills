"""Read-only PDF structure checks. Visual acceptance must be performed separately."""
import argparse
import json
import sys
from pathlib import Path


def dereference(value):
    return value.get_object() if hasattr(value, 'get_object') else value


def font_info(font):
    font = dereference(font)
    faces = [font]
    faces.extend(dereference(x) for x in font.get('/DescendantFonts', []))
    embedded = any(
        any(key in dereference(face.get('/FontDescriptor', {})) for key in ('/FontFile', '/FontFile2', '/FontFile3'))
        for face in faces
    )
    return {'base_font': str(font.get('/BaseFont', 'unknown')), 'subtype': str(font.get('/Subtype', 'unknown')),
            'embedded': embedded, 'to_unicode': '/ToUnicode' in font}


def inspect_reader(reader):
    report = {'page_count': len(reader.pages), 'pages': [], 'warnings': [], 'visual_review': 'required'}
    for number, page in enumerate(reader.pages, 1):
        text = page.extract_text() or ''
        resources = dereference(page.get('/Resources', {}))
        fonts = dereference(resources.get('/Font', {}))
        details = [font_info(font) for font in fonts.values()]
        entry = {'page': number, 'text_characters': len(text.strip()), 'has_cjk_text': any('\u3400' <= c <= '\u9fff' for c in text), 'fonts': details}
        report['pages'].append(entry)
        if not text.strip():
            report['warnings'].append(f'Page {number}: no extracted text; inspect image-only content or encoding')
        for font in details:
            if not font['embedded']:
                report['warnings'].append(f"Page {number}: {font['base_font']} has no detected embedded font program")
            if not font['to_unicode']:
                report['warnings'].append(f"Page {number}: {font['base_font']} has no ToUnicode; check actual copy/search behavior")
    if not reader.pages:
        report['warnings'].append('Document has no pages')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path)
    args = parser.parse_args()
    try:
        from pypdf import PdfReader
        report = inspect_reader(PdfReader(str(args.pdf)))
    except ImportError:
        print(json.dumps({'error': 'Install pypdf in your selected Python environment before running this helper'}))
        return 2
    except Exception as error:
        print(json.dumps({'error': str(error)}, ensure_ascii=True))
        return 2
    print(json.dumps(report, ensure_ascii=True, indent=2))
    return 1 if report['warnings'] else 0


if __name__ == '__main__':
    sys.exit(main())
