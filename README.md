# Photoshop Keyboard Shortcuts Converter

A command-line tool to convert Adobe Photoshop keyboard shortcuts from HTML format to KYS (Keyboard Shortcuts) format.

## Description

This tool processes HTML-exported keyboard shortcuts from Adobe Photoshop and converts them into the KYS format that can be imported back into Photoshop. It handles:

- Command shortcuts
- Tool shortcuts
- Taskspace-specific shortcuts
- Tool properties and options

## Usage

### Command Line Mode

The tool can be run with command-line arguments:

```bash
ps-shortcut-tool.py -i "input.htm" -o "output name" -d "C:\path\to\directory"
```

Parameters:
- `-i` or `--input`: Input HTML file name (required)
- `-o` or `--output`: Output keymapping name without extension (required)
- `-d` or `--directory`: Base directory for input/output files (optional)

Example:
```bash
ps-shortcut-tool.py -i "shortcuts.htm" -o "My Custom Shortcuts" -d "C:\Users\username\Documents"
```

### Interactive Mode

Run the tool without parameters to use interactive mode:

```bash
ps-shortcut-tool.py
```

The tool will prompt you for:
1. Base directory (press Enter to use current directory)
2. Input HTML file name
3. Output keymapping name

## Output

The tool generates a `.kys` file that can be imported into Photoshop:
- Preserves all shortcut mappings
- Includes tool IDs and types
- Handles taskspace-specific settings

## Notes

- Input HTML file should be exported from Photoshop's keyboard shortcuts panel
- Output file will be created in the specified directory with `.kys` extension
- Spaces in the output name are handled automatically

## Error Handling

- Validates input file existence
- Checks directory permissions
- Reports conversion errors with details
- Allows retry on file input errors

## Requirements

- Windows operating system
- Python 3.6
- No additional dependencies required

## Standalone Version

A standalone executable will be made when I can get pyInstaller to work properly :)
