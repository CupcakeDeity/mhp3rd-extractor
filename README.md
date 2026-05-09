# MHP3rd File Extractor & Repacker

A Python tool for extracting and repacking PAC archive files from Monster Hunter Portable 3rd.

## Features

- **Extract PAC files** into individual components (models, textures, animations, etc.)
- **Repack PAC files** from extracted components
- **File type detection** (PMO, PTX, ANM, etc.)
- **Detailed extraction logs** for reference
- **Termux-compatible** (runs on Android)

## Installation

### Prerequisites
- Python 3.6+
- Git (for cloning)

### Setup in Termux

```bash
# Install Python and git if needed
pkg install python git

# Clone the repository
git clone https://github.com/yourusername/mhp3rd-extractor.git
cd mhp3rd-extractor

# Make scripts executable
chmod +x extract_pac.py repack_pac.py
```

### Setup on PC (Linux/macOS/Windows)

```bash
git clone https://github.com/yourusername/mhp3rd-extractor.git
cd mhp3rd-extractor
python3 extract_pac.py --help
```

## Usage

### Extract a PAC File

```bash
# Basic extraction (creates head_extracted/ directory)
python3 extract_pac.py head.pac

# Custom output directory
python3 extract_pac.py head.pac -o my_extracted_files/

# Verbose output
python3 extract_pac.py head.pac -v
```

**Output structure:**
```
head_extracted/
├── head_00.pmo      (3D Model)
├── head_01.bin      (Supporting data)
├── head_02.bin      (Collision/Physics)
├── head_03.bin      (Vertices/Materials)
└── EXTRACTION_LOG.txt
```

### Repack a PAC File

#### From individual files:
```bash
python3 repack_pac.py output.pac -f head_00.pmo head_01.bin head_02.bin head_03.bin
```

#### From a directory:
```bash
python3 repack_pac.py output.pac -d head_extracted/

# With filename pattern matching
python3 repack_pac.py output.pac -d head_extracted/ -p "head_*.bin"
```

#### Advanced options:
```bash
# Sort files by name before packing (helps maintain order)
python3 repack_pac.py output.pac -d head_extracted/ -s

# Verbose output
python3 repack_pac.py output.pac -d head_extracted/ -v
```

## Workflow Example

**Edit armor colors for Ultramarines aesthetic:**

```bash
# 1. Extract original PAC
python3 extract_pac.py head.pac -o head_extracted

# 2. Modify files with your tools
#    - Edit head_00.pmo (PPSSPP texture replacement, PAC binary editing, etc.)
#    - Modify head_03.bin (vertex colors, texture data)

# 3. Repack the modified files
python3 repack_pac.py head_modified.pac -d head_extracted/ -s

# 4. Replace in game or test with PPSSPP
```

## File Types

| Extension | Type | Description |
|-----------|------|-------------|
| .pmo | PMO (3D Model) | Polygon model mesh and geometry |
| .ptx | PTX (Texture) | Texture data |
| .anm | ANM (Animation) | Animation data |
| .skl | SKL (Skeleton) | Bone/skeleton structure |
| .eff | EFF (Effect) | Particle/visual effects |
| .mtl | MTL (Material) | Material properties |
| .bin | Binary | Raw data (collision, vertices, etc.) |

## Troubleshooting

### "PAC file too small"
- Make sure you're pointing to the correct PAC file
- File might be corrupted

### Files missing after extraction
- Check EXTRACTION_LOG.txt for details
- The PAC might use a different format (less common)

### Repacked PAC doesn't work in-game
- Ensure files are in the same order as extracted
- Use `-s` (sort) flag to maintain consistent ordering
- Check file sizes match originals

## Notes for MHP3rd Modding

- **Texture recoloring**: Modify the `.pmo` or texture data in `.bin` files
- **Model editing**: Use external PMO editors, then repack
- **Armor aesthetics**: Color data is typically in vertex colors (head_03.bin)
- **PPSSPP testing**: Extract → Modify → Repack → Test with texture replacement

## Limitations

- PAC header doesn't store original filenames (they're generated from position)
- Some MHP3rd file formats may vary by region/patch
- Binary modifications require knowledge of the format

## Contributing

Found an undocumented PAC variant? File type not detected? Create an issue or submit a PR!

## License

MIT License - feel free to use and modify

## Resources

- Monster Hunter Portable 3rd ROM
- PPSSPP emulator for testing
- MHP3rd modding communities

---

**Questions?** Check the EXTRACTION_LOG.txt and PACK_LOG.txt files for detailed information about your PAC files.
