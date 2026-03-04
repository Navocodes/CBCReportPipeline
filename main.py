import os
import argparse
import json
import glob
from src.extraction import extract_text_from_pdf
from src.parsing import parse_cbc_report
from src.conversion import convert_to_fhir_bundle
from src.visualization import plot_cbc_trends

def main():
    parser = argparse.ArgumentParser(description="CBC Report Processing Pipeline")
    parser.add_argument("input_dir", help="Directory containing PDF reports")
    parser.add_argument("output_dir", help="Directory to save processed data and plots")
    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    pdf_files = glob.glob(os.path.join(args.input_dir, "*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in {args.input_dir}")
        return

    all_reports = []

    for pdf_path in pdf_files:
        print(f"Processing {pdf_path}...")
        try:
            # 1. Extraction
            text = extract_text_from_pdf(pdf_path)
            if not text:
                print(f"Warning: No text extracted from {pdf_path}")
                continue

            # 2. Parsing
            report = parse_cbc_report(text)
            
            # Save raw JSON
            file_name = os.path.basename(pdf_path).replace(".pdf", ".json")
            json_path = os.path.join(args.output_dir, file_name)
            with open(json_path, "w") as f:
                json.dump(report, f, indent=2)
            
            # 3. Validation & Accumulation
            # Only add to list if we have meaningful data
            if report.get("cbc_report"):
                all_reports.append(report)
            
            # 4. FHIR Conversion
            convert_to_fhir_bundle(report, args.output_dir)

        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")

    # 5. Visualization
    if all_reports:
        print("Generating time-series visualization...")
        plot_cbc_trends(all_reports, args.output_dir)
        print("Done.")
    else:
        print("No valid reports parsed for visualization.")

if __name__ == "__main__":
    main()
