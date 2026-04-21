#!/usr/bin/env python3
import json
import subprocess
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python batch_upload_to_bq.py <config.json>")
        sys.exit(1)

    config_file = sys.argv[1]

    # Read config
    with open(config_file, 'r') as f:
        config = json.load(f)

    project = config['project']
    dataset = config['dataset']
    uploads = config['uploads']

    # Track results
    successful = []
    failed = []

    # Process each upload
    for i, upload in enumerate(uploads, 1):
        csv_file = upload['csv_file']
        table_name = upload['table_name']
        table_id = f"{project}.{dataset}.{table_name}"

        print(f"\n[{i}/{len(uploads)}] Uploading {csv_file} to {table_id}...")

        try:
            result = subprocess.run(
                ['python', 'scripts/upload_to_bq.py', csv_file, table_id],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print(f"✓ Success")
                successful.append(csv_file)
            else:
                print(f"✗ Failed: {result.stderr}")
                failed.append(csv_file)
        except Exception as e:
            print(f"✗ Error: {e}")
            failed.append(csv_file)

    # Print summary
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    print(f"Total: {len(uploads)}")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(failed)}")

    if failed:
        print(f"\nFailed uploads:")
        for f in failed:
            print(f"  - {f}")

if __name__ == "__main__":
    main()
