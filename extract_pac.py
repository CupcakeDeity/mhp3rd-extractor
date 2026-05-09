#!/usr/bin/env python3
"""
MHP3rd PAC File Extractor
Extracts Capcom PAC archive files used in Monster Hunter Portable 3rd
"""

import struct
import os
import sys
import argparse
from pathlib import Path


class PACExtractor:
    """Extracts PAC (Capcom archive) files"""
    
    # File type signatures
    SIGNATURES = {
        b'pmo': 'PMO (3D Model)',
        b'ptx': 'PTX (Texture)',
        b'anm': 'ANM (Animation)',
        b'skl': 'SKL (Skeleton)',
        b'eff': 'EFF (Effect)',
        b'mtl': 'MTL (Material)',
    }
    
    def __init__(self, pac_path, verbose=False):
        """Initialize extractor"""
        self.pac_path = Path(pac_path)
        self.verbose = verbose
        
        if not self.pac_path.exists():
            raise FileNotFoundError(f"PAC file not found: {self.pac_path}")
        
        with open(self.pac_path, 'rb') as f:
            self.data = f.read()
        
        self.entries = []
        self.parse_header()
    
    def parse_header(self):
        """Parse PAC header and offset table"""
        if len(self.data) < 4:
            raise ValueError("PAC file too small (< 4 bytes)")
        
        # First 4 bytes = number of entries
        num_entries = struct.unpack('<I', self.data[0:4])[0]
        
        if self.verbose:
            print(f"[*] PAC Header: {num_entries} entries")
        
        # Read offset table
        offsets = []
        for i in range(num_entries):
            offset = struct.unpack('<I', self.data[(i+1)*4:(i+2)*4])[0]
            offsets.append((i, offset))
        
        # Sort by offset to determine file boundaries
        offsets_sorted = sorted(offsets, key=lambda x: x[1])
        
        # Calculate file sizes
        for i, (file_num, start) in enumerate(offsets_sorted):
            if i < len(offsets_sorted) - 1:
                end = offsets_sorted[i+1][1]
            else:
                end = len(self.data)
            
            file_data = self.data[start:end]
            file_type = self.identify_type(file_data)
            
            self.entries.append({
                'index': file_num,
                'offset': start,
                'size': end - start,
                'data': file_data,
                'type': file_type
            })
            
            if self.verbose:
                print(f"  [{file_num}] offset=0x{start:04x} size={end-start:6d}b type={file_type}")
    
    def identify_type(self, data):
        """Identify file type from magic bytes"""
        if len(data) < 4:
            return 'Unknown'
        
        # Check common signatures
        for sig, name in self.SIGNATURES.items():
            if data[:len(sig)] == sig:
                return name
        
        # Check for binary data
        if data[:4] == b'\x00\x00\x00\x80':
            return 'Collision/Physics'
        
        # Default
        return f'Binary (0x{data[:4].hex()})'
    
    def extract_all(self, output_dir=None):
        """Extract all files from PAC"""
        if output_dir is None:
            output_dir = self.pac_path.stem + '_extracted'
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True, parents=True)
        
        print(f"[*] Extracting {len(self.entries)} files to: {output_path}")
        
        for entry in self.entries:
            filename = self.generate_filename(entry)
            filepath = output_path / filename
            
            with open(filepath, 'wb') as f:
                f.write(entry['data'])
            
            print(f"  ✓ {filename:30s} ({entry['size']:6d}b) - {entry['type']}")
        
        # Write extraction log
        self.write_log(output_path)
        
        print(f"\n[+] Extraction complete!")
        return output_path
    
    def generate_filename(self, entry):
        """Generate appropriate filename for extracted file"""
        base_name = self.pac_path.stem
        file_num = entry['index']
        
        # Get extension from type
        file_type = entry['type']
        if 'Model' in file_type:
            ext = '.pmo'
        elif 'Texture' in file_type:
            ext = '.ptx'
        elif 'Animation' in file_type:
            ext = '.anm'
        elif 'Skeleton' in file_type:
            ext = '.skl'
        elif 'Effect' in file_type:
            ext = '.eff'
        elif 'Material' in file_type:
            ext = '.mtl'
        else:
            ext = '.bin'
        
        return f"{base_name}_{file_num:02d}{ext}"
    
    def write_log(self, output_dir):
        """Write extraction log with file information"""
        log_path = output_dir / 'EXTRACTION_LOG.txt'
        
        with open(log_path, 'w') as f:
            f.write(f"MHP3rd PAC Extraction Log\n")
            f.write(f"Source: {self.pac_path.name}\n")
            f.write(f"Entries: {len(self.entries)}\n")
            f.write(f"\n{'Index':5} {'Offset':8} {'Size':8} {'Type'}\n")
            f.write(f"{'-'*50}\n")
            
            for entry in self.entries:
                f.write(f"{entry['index']:5d} 0x{entry['offset']:06x} {entry['size']:8d} {entry['type']}\n")
        
        print(f"  ℹ Log written to: EXTRACTION_LOG.txt")


def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description='Extract Monster Hunter Portable 3rd PAC archive files',
        epilog='Example: %(prog)s head.pac -o extracted/'
    )
    
    parser.add_argument('pac_file', help='PAC file to extract')
    parser.add_argument('-o', '--output', help='Output directory (default: pac_name_extracted)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    try:
        extractor = PACExtractor(args.pac_file, verbose=args.verbose)
        extractor.extract_all(args.output)
    
    except FileNotFoundError as e:
        print(f"[!] Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[!] Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
