# Testing guide

Install Python dependencies before running tests:

```bash
python -m pip install -r requirements.txt
```

Run a focused test module from the repository root:

```bash
python -m pytest tests/test_slide_template_export.py
```

Run the complete suite:

```bash
python -m pytest
```

Slide export tests should avoid network access by monkeypatching media downloads and using in-memory PNG fixtures. Reopen generated decks with `pptx.Presentation` to validate package integrity and inspect layouts, shapes, tables, charts, and notes.

The live application requires model credentials and local retrieval artifacts; unit tests should not require those services. The React production bundle is built with:

```bash
cd app/frontend
npm install
npm run build
```

Visual PPTX QA may use LibreOffice headless to convert decks to PDF and `pdftoppm` for page images. Skip visual tests explicitly when LibreOffice is unavailable.
