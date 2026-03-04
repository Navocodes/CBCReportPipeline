# CBC Report Processing Pipeline: Implementation Workflow

This document outlines the end-to-end workflow for the CBC (Complete Blood Count) Report Processing Pipeline. It details the system architecture, setup instructions, and the data flow from data extraction to visualization.

## 1. Project Overview

The **CBC Report Processing Pipeline** is a modular Python-based system designed to digitize, normalize, and visualize medical blood test data from PDF reports. It converts unstructured PDF data into structured formats (JSON, FHIR) and generates longitudinal health trend analysis.

## 2. Directory Structure

The project follows a clean, modular architecture:

'''
TimeSeries/
├── src/
│   ├── __init__.py
│   ├── extraction.py      # Module 1: OCR & Text Extraction
│   ├── parsing.py         # Module 2: Regex-based Data Parsing
│   ├── conversion.py      # Module 3: FHIR Standard Conversion
│   └── visualization.py   # Module 4: Time-Series Plotting
├── main.py                # Pipeline Orchestrator (CLI Entry Point)
├── requirements.txt       # Python Dependencies
└── README.md              # Project Documentation
'''

## 3. Prerequisites

Before running the pipeline, ensure the following system-level dependencies are installed on your machine:

### Python Environment

* Python 3.8 or higher

### System Dependencies

**Tesseract OCR**: The engine used to recognize text in images.

    *   *macOS*: `brew install tesseract`
    *   *Ubuntu*: `sudo apt-get install tesseract-ocr`
    *   *Windows*: Download and install the Tesseract binary.
**Poppler**: Required by `pdf2image` to convert PDF pages to images.
    *   *macOS*: `brew install poppler`
    *   *Ubuntu*: `sudo apt-get install poppler-utils`
    *   *Windows*: Download binary and add to PATH.

## 4. Installation & Setup

1. **Clone the Repository**

    bash
    git clone <repository-url>
    cd TimeSeries

2. **Create a Virtual Environment**
    It is recommended to use a virtual environment to manage dependencies.
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Python Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## 5. Usage

The pipeline is executed via the `main.py` script. It accepts an input directory (containing PDFs) and an output directory (where results will be saved).

### Command Syntax
```bash
python main.py <INPUT_DIR> <OUTPUT_DIR>
```

### Example
To process all PDFs in the current directory (`.`) and save the output to a folder named `processed_data`:

```bash
python main.py . processed_data
```

## 6. Detailed Pipeline Workflow

The `main.py` orchestrator runs the following sequential steps for each PDF file found in the input directory:

### Step 1: Text Extraction (`src/extraction.py`)
*   **Input**: Raw PDF file path.
*   **Process**: 
    1.  Converts PDF pages into high-resolution images using `pdf2image`.
    2.  Applies Tesseract OCR to each image to extract raw string text.
*   **Output**: Raw unstructured string.

### Step 2: Data Parsing (`src/parsing.py`)
*   **Input**: Raw text string.
*   **Process**:
    1.  Splits text into lines.
    2.  Uses Regular Expressions (Regex) to identify:
        *   Patient Demographics (Name, Age, Sex, ID).
        *   Report Metadata (Date).
        *   CBC Parameters (Haemoglobin, WBC, RBC, Platelets, etc.).
    3.  Normalizes units and values.
*   **Output**: Intermediate Python Dictionary (structured conceptual data).

### Step 3: Persistence & Conversion (`src/conversion.py`)
*   **Process A (Raw JSON)**: 
    *   The intermediate dictionary is dumped immediately to a standard JSON file (e.g., `PatientReport.json`) for easy debugging and usage.
*   **Process B (FHIR Standard)**:
    *   Maps internal keys to **LOINC codes** (Logical Observation Identifiers Names and Codes).
    *   Constructs a valid **FHIR R4 Bundle** containing `Patient`, `DiagnosticReport`, and `Observation` resources.
    * Saves as `fhir_bundle_<patient_id>_<date>.json`.

###

Step 4: Data Aggregation & Validation (in `main.py`)
* The orchestrator collects all successfully parsed reports into a list.
* Reports with missing dates or critical errors are flagged and skipped.

###

Step 5: Visualization (`src/visualization.py`)
***Input**: List of all parsed patient reports.
***Process**:
    1. Converts list of dictionaries into a **Pandas DataFrame**.
    2. Sets the index to the Report Date.
    3. Sorts chronologically.
    4. Generates a Matplotlib grid of subplots, one for each blood parameter (e.g., Hemoglobin trend over time).
***Output**: `cbc_trends.png` saved in the output directory.

## 7. Output Artifacts

After a successful run, your `<OUTPUT_DIR>` will contain:

1. **JSON Reports**: `COMPLETE HAEMOGRAM XX-XX-XXXX.json`
    * Easy-to-read, flat structure for general use.
2. **FHIR Bundles**: `fhir_bundle_patient-xyz_20230313.json`
    * Interoperable standard format ready for EHR integration.
3. **Visualization**: `cbc_trends.png`
    * A visual dashboard showing the patient's health trends over the reporting period.
