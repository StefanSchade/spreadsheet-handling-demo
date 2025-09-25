from spreadsheet_handling.api import load_dataset  # beispielhaft
from plugins.transforms import run_repo_validations

def main():
    ds = load_dataset("./data")  # oder über Excel-Layer, wenn erwünscht
    run_repo_validations(ds)     # wirft ValueError bei Regelverstoß
    print("Verification OK.")

if __name__ == "__main__":
    main()
