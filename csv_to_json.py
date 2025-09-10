#!/usr/bin/env python3
"""
CSV to JSON Converter for ForexFactory Calendar Data

Converts forex_factory_catalog.csv to JSON array format.
Each row becomes a JSON object with keys: date, country, impact, title, actual, forecast, previous
"""

import csv
import json
import sys
import argparse
from pathlib import Path


def csv_to_json(csv_file_path, json_file_path=None, pretty=True):
    """
    Convert CSV file to JSON array format.
    
    Args:
        csv_file_path (str): Path to the input CSV file
        json_file_path (str, optional): Path to output JSON file. If None, uses input name with .json extension
        pretty (bool): Whether to format JSON with indentation
    
    Returns:
        str: Path to the created JSON file
    """
    csv_path = Path(csv_file_path)
    
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_file_path}")
    
    # Determine output file path
    if json_file_path is None:
        json_path = csv_path.with_suffix('.json')
    else:
        json_path = Path(json_file_path)
    
    # Column names mapping
    column_names = ['date', 'country', 'impact', 'title', 'actual', 'forecast', 'previous']
    
    events = []
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            
            for row_num, row in enumerate(reader, 1):
                # Skip empty rows
                if not row or all(cell.strip() == '' for cell in row):
                    continue
                
                # Ensure we have exactly 7 columns (pad with empty strings if needed)
                while len(row) < 7:
                    row.append('')
                
                # Create event dictionary
                event = {}
                for i, column_name in enumerate(column_names):
                    if i < len(row):
                        event[column_name] = row[i].strip()
                    else:
                        event[column_name] = ''
                
                events.append(event)
    
    except Exception as e:
        raise Exception(f"Error reading CSV file at row {row_num}: {str(e)}")
    
    # Write JSON file
    try:
        with open(json_path, 'w', encoding='utf-8') as jsonfile:
            if pretty:
                json.dump(events, jsonfile, indent=2, ensure_ascii=False)
            else:
                json.dump(events, jsonfile, ensure_ascii=False)
    
    except Exception as e:
        raise Exception(f"Error writing JSON file: {str(e)}")
    
    return str(json_path)


def main():
    parser = argparse.ArgumentParser(
        description='Convert ForexFactory CSV calendar data to JSON array format'
    )
    parser.add_argument(
        'csv_file', 
        nargs='?',
        default='forex_factory_catalog.csv',
        help='Input CSV file path (default: forex_factory_catalog.csv)'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output JSON file path (default: input filename with .json extension)'
    )
    parser.add_argument(
        '--compact',
        action='store_true',
        help='Output compact JSON without pretty formatting'
    )
    
    args = parser.parse_args()
    
    try:
        output_path = csv_to_json(
            args.csv_file, 
            args.output, 
            pretty=not args.compact
        )
        
        # Get file stats
        input_path = Path(args.csv_file)
        output_path_obj = Path(output_path)
        
        input_size = input_path.stat().st_size
        output_size = output_path_obj.stat().st_size
        
        print(f"✓ Converted {args.csv_file} → {output_path}")
        print(f"  Input:  {input_size:,} bytes")
        print(f"  Output: {output_size:,} bytes")
        
        # Count records
        with open(output_path, 'r') as f:
            data = json.load(f)
            print(f"  Records: {len(data):,}")
            
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
