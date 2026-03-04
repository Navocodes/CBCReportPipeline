import json
import uuid
from datetime import datetime
import os

def convert_to_fhir_bundle(report: dict, output_path: str) -> str:
    """
    Converts a CBC report dictionary to a FHIR Bundle JSON file.
    Returns the path to the created file.
    """
    loinc_map = {
        "haemoglobin_g_dl": ("718-7", "Hemoglobin", "g/dL"),
        "rbc_count_mill_per_cumm": ("789-8", "Erythrocytes", "10^6/uL"),
        "leucocyte_count_per_cumm": ("6690-2", "Leukocytes", "10^3/uL"),
        "platelet_count_per_cumm": ("777-3", "Platelets", "10^3/uL"),
        "pcv_percent": ("4544-3", "Hematocrit", "%"),
        "mcv_fL": ("787-2", "MCV", "fL"),
        "mch_pg": ("785-6", "MCH", "pg"),
        "mchc_g_dl": ("786-4", "MCHC", "g/dL")
    }

    report_date_str = report.get("report_date")
    if report_date_str:
        try:
            report_date = datetime.strptime(report_date_str, "%Y-%m-%d")
        except ValueError:
            # Try fallback format if different
            try:
                report_date = datetime.strptime(report_date_str, "%d-%m-%Y")
            except ValueError:
                report_date = datetime.now()
    else:
        report_date = datetime.now()

    age = report.get("age")
    birth_year = report_date.year - int(age) if age else report_date.year
    birth_date = f"{birth_year:04d}-{report_date.month:02d}-{report_date.day:02d}"

    # Generate or reuse patient ID
    # In a real system, this would look up an existing patient
    patient_id = report.get("patient_id")
    if not patient_id:
        patient_id = f"patient-{uuid.uuid4().hex[:8]}"
    else:
        # Sanitize for ID usage
        patient_id = "".join(c for c in patient_id if c.isalnum() or c in "-._")

    obs_entries = []
    cbc_report = report.get("cbc_report", {})
    
    for key, value in cbc_report.items():
        if key in loinc_map:
            loinc_code, display, unit = loinc_map[key]
            obs_id = f"obs-{uuid.uuid4().hex[:8]}"
            obs_entries.append({
                "resource": {
                    "resourceType": "Observation",
                    "id": obs_id,
                    "meta": {
                        "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Observation"]
                    },
                    "text": {
                        "status": "generated",
                        "div": f"<div xmlns=\"http://www.w3.org/1999/xhtml\">{display}: {value} {unit}</div>"
                    },
                    "status": "final",
                    "category": [{
                        "coding": [{
                            "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                            "code": "laboratory",
                            "display": "Laboratory"
                        }]
                    }],
                    "code": {
                        "coding": [{
                            "system": "http://loinc.org",
                            "code": loinc_code,
                            "display": display
                        }],
                        "text": display
                    },
                    "subject": {"reference": f"Patient/{patient_id}"},
                    "effectiveDateTime": report_date.strftime("%Y-%m-%d"),
                    "valueQuantity": {
                        "value": value,
                        "unit": unit,
                        "system": "http://unitsofmeasure.org"
                    }
                }
            })

    diagnostic_report = {
        "resource": {
            "resourceType": "DiagnosticReport",
            "id": f"report-{uuid.uuid4().hex[:8]}",
            "meta": {
                "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/DiagnosticReportLab"]
            },
            "text": {
                "status": "generated",
                "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">CBC Diagnostic Report</div>"
            },
            "status": "final",
            "code": {
                "coding": [{
                    "system": "http://loinc.org",
                    "code": "58410-2",
                    "display": "CBC panel - Blood"
                }],
                "text": "CBC panel - Blood"
            },
            "subject": {"reference": f"Patient/{patient_id}"},
            "effectiveDateTime": report_date.strftime("%Y-%m-%d"),
            "issued": report_date.strftime("%Y-%m-%dT15:00:00+05:30"),
            "result": [{"reference": f"Observation/{entry['resource']['id']}"} for entry in obs_entries]
        }
    }

    patient = {
        "resource": {
            "resourceType": "Patient",
            "identifier": [{
                "system": "https://ndhm.gov.in/health_id",
                "value": report.get("patient_id", patient_id)
            }],
            "id": patient_id,
            "meta": {
                "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Patient"]
            },
            "text": {
                "status": "generated",
                "div": f"<div xmlns=\"http://www.w3.org/1999/xhtml\">Patient: {report.get('patient_name', '')}, Gender: {report.get('sex', '')}, BirthDate: {birth_date}</div>"
            },
            "name": [{"text": report.get("patient_name", "")}],
            "gender": report.get("sex", "").lower() if report.get("sex") else "unknown",
            "birthDate": birth_date
        }
    }

    fhir_bundle = {
        "resourceType": "Bundle",
        "type": "collection",
        "entry": [patient, diagnostic_report] + obs_entries
    }

    file_name = f"fhir_bundle_{patient_id}_{report_date.strftime('%Y%m%d')}.json"
    full_path = os.path.join(output_path, file_name)
    with open(full_path, "w") as fhir_out:
        json.dump(fhir_bundle, fhir_out, indent=2)
    
    return full_path
