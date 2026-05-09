#!/usr/bin/env python3
"""
MHP3rd PAC File Repacker
Repacks extracted files back into PAC archives
"""

import struct
import os
import sys
import argparse
from pathlib import Path


class PACRepacker:
    """Repacks files into PAC (Capcom archive) format"""
    
    def __init__(self, output_path, verbose=False):
        """Initialize repacker"""
        self.output_path = Path(output_path)
        self.verbose = verbose
        self.files = []
    
    def add_file(self, file_path):
        """Add a file to the PAC archive"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'rb') as f:
            data = f.read()
        
        self.files.append({
            'name': file_path.name,
            'path': file_path,
            'data': data,
            'size': len(data)
        })
        
        if self.verbose:
            print(f"[+] Added: {file_path.name} ({len(data)} bytes)")
    
    def add_directory(self, directory, pattern='*'):
        """Add all matching files from a directory"""
        dir_path = Path(directory)
        
        if not dir_path.is_dir():
            raise NotADirectoryError(f"Not a directory: {directory}")
        
        files = sorted(dir_path.glob(pattern))
        
        if self.verbose:
            print(f"[*] Scanning directory: {dir_path}")
        
        for file_path in files:
            # Skip log files and non-regular files
            if file_path.is_file() and not file_path.suffix == '.txt':
                self.add_file(file_path)
        
        if self.verbose:
            print(f"[*] Found {len(self.files)} files")
    
    def pack(self, sort_by_name=False, preserve_order=None):
        """Pack all files into PAC format"""
        if not self.files:
            raise ValueError("No files to pack")
        
        # Sort files by name if requested
        if sort_by_name:
            self.files.sort(key=lambda x: x['name'])
        
        # Or preserve specific order if provided (list of filenames)
        if preserve_order:
            ordered = []
            for name in preserve_order:
                for f in self.files:
                    if f['name'] == name:
                        ordered.append(f)
                        break
            self.files = ordered
        
        # Build PAC file
        pac_data = bytearray()
        
        # Header: number of entries
        num_entries = len(self.files)
        pac_data.extend(struct.pack('<I', num_entries))
        
        # Offset table
        offsets = []
        current_offset = (num_entries + 1) * 4  # Header + offset table size
        
        for file_entry in self.files:
            offsets.append(current_offset)
            pac_data.extend(struct.pack('<I', current_offset))
            current_offset += file_entry['size']
        
        # File data
        for file_entry in self.files:
            pac_data.extend(file_entry['data'])
        
        # Write PAC file
        with open(self.output_path, 'wb') as f:
            f.write(pac_data)
        
        print(f"[+] Packed {num_entries} files")
        print(f"[+] Output: {self.output_path} ({len(pac_data)} bytes)")
        
        # Write pack log
        self.write_log()
        
        return self.output_path
    
    def write_log(self):
        """Write packing log"""
        log_path = self.output_path.parent / 'PACK_LOG.txt'
        
        with open(log_path, 'w') as f:
            f.write(f"MHP3rd PAC Packing Log\n")
            f.write(f"Output: {self.output_path.name}\n")
            f.write(f"Entries: {len(self.files)}\n")
            f.write(f"\n{'Index':5} {'Filename':30} {'Size':8}\n")
            f.write(f"{'-'*50}\n")
            
            for i, file_entry in enumerate(self.files):
                f.write(f"{i:5d} {file_entry['name']:30} {file_entry['size']:8d}\n")
        
        print(f"[*] Log written to: PACK_LOG.txt")


def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description='Repack files into Monster Hunter Portable 3rd PAC archives',
        epilog='Examples:\n  %(prog)s output.pac -f file1.pmo file2.bin\n  %(prog)s output.pac -d extracted_dir/'
    )
    
    parser.add_argument('output', help='Output PAC file path')
    parser.add_argument('-f', '--files', nargs='+', help='Files to pack')
    parser.add_argument('-d', '--directory', help='Directory containing files to pack')
    parser.add_argument('-p', '--pattern', default='*', help='File pattern to match (with -d, default: *)')
    parser.add_argument('-s', '--sort', action='store_true', help='Sort files by name')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if not args.files and not args.directory:
        parser.print_help()
        sys.exit(1)
    
    try:
        repacker = PACRepacker(args.output, verbose=args.verbose)
        
        if args.directory:
            repacker.add_directory(args.directory, args.pattern)
        
        if args.files:
            for file_path in args.files:
                repacker.add_file(file_path)
        
        repacker.pack(sort_by_name=args.sort)
    
    except Exception as e:
        print(f"[!] Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
