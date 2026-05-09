#!/usr/bin/env python3
"""
Batch PAC Extractor
Extract multiple PAC files at once
"""

import os
import sys
import argparse
from pathlib import Path
from extract_pac import PACExtractor


def main():
    """Batch extraction"""
    parser = argparse.ArgumentParser(
        description='Batch extract multiple PAC files',
        epilog='Example: %(prog)s *.pac -o extracted/'
    )
    
    parser.add_argument('pac_files', nargs='+', help='PAC files to extract (supports wildcards)')
    parser.add_argument('-o', '--output', help='Output base directory')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Expand wildcards
    files_to_process = []
    for pattern in args.pac_files:
        files_to_process.extend(Path('.').glob(pattern))
    
    if not files_to_process:
        print("[!] No PAC files found matching patterns")
        sys.exit(1)
    
    print(f"[*] Found {len(files_to_process)} PAC file(s)")
    
    for pac_file in files_to_process:
        try:
            print(f"\n[*] Processing: {pac_file.name}")
            
            extractor = PACExtractor(pac_file, verbose=args.verbose)
            
            if args.output:
                output_dir = Path(args.output) / pac_file.stem
            else:
                output_dir = None
            
            extractor.extract_all(output_dir)
            
        except Exception as e:
            print(f"[!] Error processing {pac_file.name}: {e}", file=sys.stderr)
            continue
    
    print(f"\n[+] Batch extraction complete!")


if __name__ == '__main__':
    main()
