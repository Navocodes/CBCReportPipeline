# CBC Report Processing Pipeline

A modular Python-based system for digitizing, normalizing, and visualizing medical blood test data from PDF reports. This pipeline converts unstructured Complete Blood Count (CBC) reports into structured formats (JSON, FHIR) and generates longitudinal health trend analysis.

## Features

- **PDF Text Extraction**: OCR-based text extraction from scanned PDF reports using Tesseract
- **Intelligent Parsing**: Regex-based extraction of patient demographics and CBC parameters
- **FHIR Conversion**: Standards-compliant FHIR Bundle generation for healthcare interoperability
- **Time-Series Visualization**: Automated plotting of CBC trends over time

## Prerequisites

### System Dependencies

Before installing Python dependencies, ensure the following are installed:

**Tesseract OCR** (for text recognition):
- macOS: `brew install tesseract`
- Ubuntu: `sudo apt-get install tesseract-ocr`
- Windows: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

**Poppler** (for PDF to image conversion):
- macOS: `brew install poppler`
- Ubuntu: `sudo apt-get install poppler-utils`
- Windows: Download binary and add to PATH

### Python Requirements

- Python 3.8 or higher

## Installation

1. **Clone the repository**
   ```bash
   git clone <(https://github.com/Arka-Codes/CBCReportPipeline)>
   cd CBCRep
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the pipeline using the command-line interface:

```bash
python main.py <INPUT_DIR> <OUTPUT_DIR>
```

### Arguments

- `INPUT_DIR`: Directory containing PDF CBC reports
- `OUTPUT_DIR`: Directory where processed data and visualizations will be saved

### Example

```bash
python main.py ./reports ./processed_data
```

This will:
1. Process all PDF files in the `./reports` directory
2. Extract and parse CBC data from each report
3. Generate JSON files for each report in `./processed_data`
4. Create FHIR-compliant bundles
5. Generate time-series plots of CBC trends

## Pipeline Workflow

The system processes each PDF through the following stages:

1. **Extraction** (`src/extraction.py`)
   - Converts PDF pages to high-resolution images
   - Applies Tesseract OCR to extract raw text

2. **Parsing** (`src/parsing.py`)
   - Extracts patient demographics (name, age, sex, ID)
   - Identifies report metadata (date, lab details)
   - Parses CBC parameters (hemoglobin, WBC, RBC, platelets, etc.)
   - Captures reference ranges and units

3. **Conversion** (`src/conversion.py`)
   - Transforms parsed data into FHIR-compliant JSON bundles
   - Generates standardized healthcare data format

4. **Visualization** (`src/visualization.py`)
   - Creates time-series plots showing CBC parameter trends
   - Compares values against reference ranges

## Project Structure

```
CBCRep/
├── src/
│   ├── __init__.py
│   ├── extraction.py      # PDF text extraction via OCR
│   ├── parsing.py         # CBC data parsing with regex
│   ├── conversion.py      # FHIR standard conversion
│   └── visualization.py   # Time-series plotting
├── main.py                # Pipeline orchestrator (CLI)
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Output

For each processed PDF, the pipeline generates:

- **JSON file**: Structured representation of the CBC report
- **FHIR Bundle**: Healthcare standards-compliant data format
- **Visualization plots**: Time-series graphs showing CBC trends (generated after processing all reports)

## Dependencies

Key Python packages:
- `spacy` - Natural language processing
- `pytesseract` - OCR text extraction
- `pdf2image` - PDF to image conversion
- `pdfminer.six` - PDF text extraction fallback
- `pandas` - Data manipulation
- `matplotlib` - Visualization
- `python-dateutil` - Date parsing

See [requirements.txt](requirements.txt) for the complete list.

## Error Handling

The pipeline includes robust error handling:
- Skips PDFs that cannot be processed
- Logs warnings for files with no extractable text
- Continues processing remaining files if one fails

## Future Enhancements

- Support for additional lab report formats
- Machine learning-based parsing for improved accuracy
- Web-based dashboard for visualization
- Real-time anomaly detection in CBC values

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]

## Contact

[Add contact information here]
