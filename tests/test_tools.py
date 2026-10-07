import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def module_at(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


pdf = module_at('pdf_check', ROOT / 'skills/chinese-mobile-pdf-qa/scripts/check_pdf.py')
validator = module_at('repository_validation', ROOT / 'scripts/validate_repository.py')


class Page(dict):
    def __init__(self, text, fonts=None):
        super().__init__({'/Resources': {'/Font': fonts or {}}})
        self.text = text

    def extract_text(self):
        return self.text


class Reader:
    def __init__(self, pages):
        self.pages = pages


class Checks(unittest.TestCase):
    def test_repository(self):
        self.assertEqual(validator.validate(), [])

    def test_image_only(self):
        report = pdf.inspect_reader(Reader([Page('')]))
        self.assertEqual(report['pages'][0]['text_characters'], 0)
        self.assertEqual(len(report['warnings']), 1)

    def test_embedded_cjk(self):
        font = {'/Subtype': '/Type0', '/BaseFont': '/Example', '/ToUnicode': {}, '/DescendantFonts': [{'/FontDescriptor': {'/FontFile2': b'fixture'}}]}
        report = pdf.inspect_reader(Reader([Page('中文测试', {'/F0': font})]))
        self.assertTrue(report['pages'][0]['has_cjk_text'])
        self.assertEqual(report['warnings'], [])
        self.assertEqual(report['visual_review'], 'required')

    def test_unembedded_font(self):
        report = pdf.inspect_reader(Reader([Page('Text', {'/F0': {'/BaseFont': '/Helvetica'}})]))
        self.assertEqual(len(report['warnings']), 2)

    def test_empty_document(self):
        self.assertIn('Document has no pages', pdf.inspect_reader(Reader([]))['warnings'])


if __name__ == '__main__':
    unittest.main()
