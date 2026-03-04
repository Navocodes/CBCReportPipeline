import re
from dateutil import parser

def parse_cbc_report(text: str) -> dict:
    """
    Parses extracted text from a CBC report and returns a structured dictionary.
    """
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    # Patient details extraction
    patient_details = {}

    for line in lines:
        if "Patient Name" in line and not patient_details.get("patient_name"):
            name_match = re.search(r'Patient Name\s*:\s*(.+?)\s+Receiving Date', line)
            if name_match:
                patient_details["patient_name"] = name_match.group(1).strip()

        if "Sample Id. No." in line and not patient_details.get("patient_id"):
            pid_match = re.search(r'Sample Id. No.\s*:\s*([\w/,-]+)', line)
            if pid_match:
                patient_details["patient_id"] = pid_match.group(1).strip()

        if "Age :" in line and "Sex :" in line:
            age_match = re.search(r'Age\s*:\s*(\d+)', line)
            sex_match = re.search(r'Sex\s*:\s*(\w+)', line)
            if age_match:
                patient_details["age"] = int(age_match.group(1))
            if sex_match:
                patient_details["sex"] = sex_match.group(1)

    # Report date extraction
    for line in lines:
        if "Report Date" in line:
            date_match = re.search(r'Report Date.*?:?\s*([0-9]{2}[-/][0-9]{2}[-/][0-9]{2,4})', line)
            if date_match:
                try:
                    parsed_date = parser.parse(date_match.group(1), dayfirst=True)
                    patient_details["report_date"] = parsed_date.strftime('%Y-%m-%d')
                except Exception:
                    pass
            break

    # CBC test mapping to JSON keys
    mapping = {
        "Haemoglobin": "haemoglobin_g_dl",
        "Erythrocyte Count": "rbc_count_mill_per_cumm",
        "Total Leucocyte Count": "leucocyte_count_per_cumm",
        "Neutrophils": "neutrophils_percent",
        "Lymphocytes": "lymphocytes_percent",
        "Eosinophils": "eosinophils_percent",
        "Monocytes": "monocytes_percent",
        "Basophils": "basophils_percent",
        "Platelets Count": "platelet_count_per_cumm",
        "Hematocrit (PCV)": "pcv_percent",
        "MCV": "mcv_fL",
        "MCH": "mch_pg",
        "MCHC": "mchc_g_dl",
        "RDW-CV": "rdw_percent"
    }

    # Extract CBC data
    cbc_data = {}
    for test_name, json_key in mapping.items():
        for line in lines:
            if test_name in line:
                # Basic robust extraction: find the first number after the test name
                # Splitting by test_name ensures we look after the label
                parts = line.split(test_name, 1)
                if len(parts) > 1:
                    match = re.search(r'\b\d+(?:\.\d+)?\b', parts[1])
                    if match:
                        cbc_data[json_key] = float(match.group())
                        break

    # Construct JSON output
    report = {
        "patient_id": patient_details.get("patient_id"),
        "patient_name": patient_details.get("patient_name"),
        "age": patient_details.get("age"),
        "sex": patient_details.get("sex"),
        "report_date": patient_details.get("report_date"),
        "cbc_report": cbc_data
    }
    return report
