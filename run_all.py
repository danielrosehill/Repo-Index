import importlib.util
import sys

def import_from_file(file_path):
    spec = importlib.util.spec_from_file_location("module", file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["module"] = module
    spec.loader.exec_module(module)
    return module

def run_all():
    print("Starting GitHub Timeline generation...")
    
    print("\n1. Generating README.md...")
    readme_builder = import_from_file("readme-builder.py")
    readme_builder.generate_timeline()
    
    print("\n2. Generating repo-index.json...")
    json_creator = import_from_file("json-creator.py")
    timeline_data = json_creator.generate_timeline_json()
    if timeline_data:
        json_creator.save_timeline_json(timeline_data)
    
    print("\n3. Generating repo-index.csv...")
    csv_creator = import_from_file("csv-creator.py")
    timeline_data = csv_creator.generate_timeline_csv()
    if timeline_data:
        csv_creator.save_timeline_csv(timeline_data)
    
    print("\nAll operations completed!")

if __name__ == "__main__":
    run_all()