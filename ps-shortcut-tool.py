import string
import glob
import os
import pathlib
import re
import random
from time import sleep
import argparse

COMMAND_TYPES = {
  "Vanishing Point": {"kind": "dynamic", "id": ""},
  "Liquify": {"kind": "dynamic", "id": ""},
  "Lens Correction": {"kind": "dynamic", "id": ""},
  "Camera Raw Filter": {"kind": "dynamic", "id": ""},
  "Wide Angle Correction": {"kind": "dynamic", "id": ""},
  "New...": {"kind": "static", "id": "10"},
  "Open...": {"kind": "static", "id": "20"},
  "Open As...": {"kind": "static", "id": "21"},
  "Save": {"kind": "static", "id": "30"},
  "Close": {"kind": "static", "id": "31"},
  "Save As...": {"kind": "static", "id": "32"},
  "Save a Copy...": {"kind": "static", "id": "33"},
  "Revert": {"kind": "static", "id": "34"},
  "Exit": {"kind": "static", "id": "36"},
  "Close All": {"kind": "static", "id": "37"},
  "Close Others": {"kind": "static", "id": "46"},
  "Undo Rasterize Layer": {"kind": "static", "id": "101"},
  "Cut": {"kind": "static", "id": "103"},
  "Copy": {"kind": "static", "id": "104"},
  "Paste": {"kind": "static", "id": "105"},
  "Redo Eraser": {"kind": "static", "id": "132"},
  "Toggle Last State": {"kind": "static", "id": "133"},
  "Print One Copy": {"kind": "static", "id": "177"},
  "Rulers": {"kind": "static", "id": "1002"},
  "Zoom In": {"kind": "static", "id": "1004"},
  "Zoom Out": {"kind": "static", "id": "1005"},
  "Deselect": {"kind": "static", "id": "1016"},
  "All": {"kind": "static", "id": "1017"},
  "Inverse": {"kind": "static", "id": "1018"},
  "Last Filter": {"kind": "static", "id": "1019"},
  "Brush Settings": {"kind": "static", "id": "1025"},
  "Image Size...": {"kind": "static", "id": "1030"},
  "Canvas Size...": {"kind": "static", "id": "1031"},
  "Feather...": {"kind": "static", "id": "1036"},
  "Paste Into": {"kind": "static", "id": "1040"},
  "Fill...": {"kind": "static", "id": "1042"},
  "Color": {"kind": "static", "id": "1046"},
  "Info": {"kind": "static", "id": "1055"},
  "Layers": {"kind": "static", "id": "1098"},
  "Layer...": {"kind": "static", "id": "1099"},
  "Proof Colors": {"kind": "static", "id": "1105"},
  "Gamut Warning": {"kind": "static", "id": "1106"},
  "Copy Merged": {"kind": "static", "id": "1107"},
  "Hide Layers": {"kind": "static", "id": "1114"},
  "Select and Mask...": {"kind": "static", "id": "1115"},
  "File Info...": {"kind": "static", "id": "1137"},
  "Merge Visible": {"kind": "static", "id": "1139"},
  "Fade Eraser...": {"kind": "static", "id": "1154"},
  "Merge Down": {"kind": "static", "id": "1166"},
  "Actions": {"kind": "static", "id": "1170"},
  "100%": {"kind": "static", "id": "1190"},
  "Fit on Screen": {"kind": "static", "id": "1192"},
  "Paste in Place": {"kind": "static", "id": "1297"},
  "Browse in Bridge...": {"kind": "static", "id": "1520"},
  "Close and Go to Bridge...": {"kind": "static", "id": "1530"},
  "Save for Web (Legacy)...": {"kind": "static", "id": "1695"},
  "Invert": {"kind": "static", "id": "1701"},
  "Levels...": {"kind": "static", "id": "1801"},
  "Curves...": {"kind": "static", "id": "1802"},
  "Color Balance...": {"kind": "static", "id": "1804"},
  "Hue/Saturation...": {"kind": "static", "id": "1805"},
  "Auto Tone": {"kind": "static", "id": "1808"},
  "Desaturate": {"kind": "static", "id": "1809"},
  "Auto Contrast": {"kind": "static", "id": "1810"},
  "Auto Color": {"kind": "static", "id": "1817"},
  "Black & White...": {"kind": "static", "id": "1824"},
  "Reselect": {"kind": "static", "id": "1943"},
  "Print...": {"kind": "static", "id": "2101"},
  "Free Transform": {"kind": "static", "id": "2207"},
  "Again": {"kind": "static", "id": "2217"},
  "Content-Aware Scale": {"kind": "static", "id": "2220"},
  "General...": {"kind": "static", "id": "2311"},
  "Color Settings...": {"kind": "static", "id": "2344"},
  "Bring to Front": {"kind": "static", "id": "2711"},
  "Bring Forward": {"kind": "static", "id": "2712"},
  "Send Backward": {"kind": "static", "id": "2713"},
  "Send to Back": {"kind": "static", "id": "2714"},
  "Lock Guides": {"kind": "static", "id": "2940"},
  "Lock Layers...": {"kind": "static", "id": "2957"},
  "Group Layers": {"kind": "static", "id": "2958"},
  "Ungroup Layers": {"kind": "static", "id": "2959"},
  "All Layers": {"kind": "static", "id": "2962"},
  "Layer Via Copy": {"kind": "static", "id": "2970"},
  "Layer Via Cut": {"kind": "static", "id": "2971"},
  "Create Clipping Mask": {"kind": "static", "id": "2972"},
  "Find Layers": {"kind": "static", "id": "2982"},
  "Export As...": {"kind": "static", "id": "3443"},
  "Quick Export as PNG": {"kind": "static", "id": "3446"},
  "Export As...": {"kind": "static", "id": "3447"},
  "Extras": {"kind": "static", "id": "3500"},
  "Target Path": {"kind": "static", "id": "3502"},
  "Guides": {"kind": "static", "id": "3503"},
  "Grid": {"kind": "static", "id": "3504"},
  "Snap": {"kind": "static", "id": "3520"},
  "Search": {"kind": "static", "id": "5957"},
  "Keyboard Shortcuts...": {"kind": "static", "id": "5980"},
  "Menus...": {"kind": "static", "id": "5982"}
}

TOOL_MAPPINGS = {
  "Move Tool": {"type": "1", "key": "1819113074"},
  "Artboard Tool": {"type": "1", "key": "1098019924"},
  "Rectangular Marquee Tool": {"type": "1", "key": "1919380852"},
  "Elliptical Marquee Tool": {"type": "1", "key": "1701604724"},
  "Single Row Marquee Tool": {"type": "1", "key": "1936878964"},
  "Single Column Marquee Tool": {"type": "1", "key": "1935895924"},
  "Selection Brush Tool": {"type": "1", "key": "1936482930"},
  "Lasso Tool": {"type": "1", "key": "1818325871"},
  "Polygonal Lasso Tool": {"type": "1", "key": "1885826926"},
  "Magnetic Lasso Tool": {"type": "1", "key": "1835819379"},
  "Object Selection Tool": {"type": "1", "key": "1835494497"},
  "Quick Selection Tool": {"type": "1", "key": "1902867308"},
  "Magic Wand Tool": {"type": "1", "key": "2002873956"},
  "Crop Tool": {"type": "1", "key": "1668444016"},
  "Perspective Crop Tool": {"type": "1", "key": "1885565552"},
  "Slice Tool": {"type": "1", "key": "1399612244"},
  "Slice Select Tool": {"type": "1", "key": "1399608148"},
  "Frame Tool": {"type": "1", "key": "1181773652"},
  "Eyedropper Tool": {"type": "1", "key": "1702454628"},
  "Color Sampler Tool": {"type": "1", "key": "1668246643"},
  "Ruler Tool": {"type": "1", "key": "1835360596"},
  "Note Tool": {"type": "1", "key": "1417180225"},
  "Count Tool": {"type": "1", "key": "1668248942"},
  "Spot Healing Brush Tool": {"type": "1", "key": "1936746562"},
  "Remove Tool": {"type": "1", "key": "1667327604"},
  "Healing Brush Tool": {"type": "1", "key": "1937010029"},
  "Patch Tool": {"type": "1", "key": "1886675816"},
  "Content-Aware Move Tool": {"type": "1", "key": "1919118704"},
  "Red Eye Tool": {"type": "1", "key": "1919182201"},
  "Brush Tool": {"type": "1", "key": "1886286946"},
  "Pencil Tool": {"type": "1", "key": "1885695587"},
  "Color Replacement Tool": {"type": "1", "key": "1668440692"},
  "Mixer Brush Tool": {"type": "1", "key": "2003137634"},
  "Clone Stamp Tool": {"type": "1", "key": "1937006957"},
  "Pattern Stamp Tool": {"type": "1", "key": "1937010032"},
  "History Brush Tool": {"type": "1", "key": "1752396866"},
  "Art History Brush Tool": {"type": "1", "key": "1634230900"},
  "Eraser Tool": {"type": "1", "key": "1701994867"},
  "Background Eraser Tool": {"type": "1", "key": "1936028257"},
  "Magic Eraser Tool": {"type": "1", "key": "1835364961"},
  "Gradient Tool": {"type": "1", "key": "1651401812"},
  "Paint Bucket Tool": {"type": "1", "key": "1651860331"},
  "Blur Tool": {"type": "1", "key": "1651275122"},
  "Sharpen Tool": {"type": "1", "key": "1936220530"},
  "Smudge Tool": {"type": "1", "key": "1936553316"},
  "Adjustment Brush Tool": {"type": "1", "key": "1633970786"},
  "Dodge Tool": {"type": "1", "key": "1685021799"},
  "Burn Tool": {"type": "1", "key": "1651864174"},
  "Sponge Tool": {"type": "1", "key": "1685283188"},
  "Pen Tool": {"type": "1", "key": "1885695572"},
  "Freeform Pen Tool": {"type": "1", "key": "1836082542"},
  "Curvature Pen Tool": {"type": "1", "key": "1668310382"},
  "Add Anchor Point Tool": {"type": "1", "key": "1634430580"},
  "Delete Anchor Point Tool": {"type": "1", "key": "1684762228"},
  "Convert Point Tool": {"type": "1", "key": "1667985012"},
  "Horizontal Type Tool": {"type": "1", "key": "1954038392"},
  "Vertical Type Tool": {"type": "1", "key": "1954038358"},
  "Vertical Type Mask Tool": {"type": "1", "key": "1987344723"},
  "Horizontal Type Mask Tool": {"type": "1", "key": "1954115667"},
  "Path Selection Tool": {"type": "1", "key": "1885565780"},
  "Direct Selection Tool": {"type": "1", "key": "1886677089"},
  "Rectangle Tool": {"type": "1", "key": "1382376308"},
  "Ellipse Tool": {"type": "1", "key": "1164734579"},
  "Triangle Tool": {"type": "1", "key": "1416778600"},
  "Polygon Tool": {"type": "1", "key": "1349479545"},
  "Line Tool": {"type": "1", "key": "1818848852"},
  "Custom Shape Tool": {"type": "1", "key": "1131762536"},
  "Hand Tool": {"type": "1", "key": "1751215716"},
  "Rotate View Tool": {"type": "1", "key": "1919906932"},
  "Zoom Tool": {"type": "1", "key": "2054123373"},
  "Targeted Adjustment Tool": {"type": "1", "key": "1952932196"},
  "Default Foreground/Background Colors": {"type": "2", "key": ""},
  "Switch Foreground/Background Colors": {"type": "3", "key": ""},
  "Toggle Standard/Quick Mask Modes": {"type": "4", "key": ""},
  "Toggle Screen Modes": {"type": "5", "key": ""},
  "Toggle Preserve Transparency": {"type": "6", "key": ""},
  "Decrease Brush Size": {"type": "7", "key": ""},
  "Increase Brush Size": {"type": "8", "key": ""},
  "Decrease Brush Hardness": {"type": "9", "key": ""},
  "Increase Brush Hardness": {"type": "10", "key": ""},
  "Previous Brush": {"type": "11", "key": ""},
  "Next Brush": {"type": "12", "key": ""},
  "First Brush": {"type": "13", "key": ""},
  "Last Brush": {"type": "14", "key": ""},
  "Foreground Color Picker": {"type": "15", "key": ""},
  "Background Color Picker": {"type": "16", "key": ""},
  "Load Mixer Brush": {"type": "17", "key": ""},
  "Clean Mixer Brush": {"type": "18", "key": ""},
  "Toggle Mixer Brush Auto-Load": {"type": "19", "key": ""},
  "Toggle Mixer Brush Auto-Clean": {"type": "20", "key": ""},
  "Toggle Mixer Brush Sample All Layers": {"type": "21", "key": ""},
  "Sharpen Erodible Tips": {"type": "22", "key": ""},
  "Direct Selection Mode Toggle": {"type": "23", "key": ""},
  "Toggle Brush Airbrush Mode": {"type": "24", "key": ""},
  "Toggle Brush Pressure Controls Size": {"type": "25", "key": ""},
  "Toggle Brush Pressure Controls Opacity": {"type": "26", "key": ""},
  "Toggle Symmetry Off/Last": {"type": "27", "key": ""},
  "Toggle Symmetry Visibility": {"type": "28", "key": ""},
  "Toggle Preview Mode": {"type": "29", "key": ""},
  "Brush Toggle Erase": {"type": "30", "key": ""},
  "Show Previous Layer Boundary": {"type": "31", "key": ""},
  "Show Next Layer Boundary": {"type": "32", "key": ""}
}

TASKSPACE_MAPPINGS = {
  # Tools with type and key
  "Quick Selection Tool": {"type": "1", "key": "1902867308"},
  "Refine Edge Brush Tool": {"type": "1", "key": "1397518949"},
  "Brush Tool": {"type": "1", "key": "1886286946"},
  "Object Selection Tool": {"type": "1", "key": "1835494497"},
  "Lasso Tool": {"type": "1", "key": "1818325871"},
  "Polygonal Lasso Tool": {"type": "1", "key": "1885826926"},
  "Hand Tool": {"type": "1", "key": "1751215716"},
  "Zoom Tool": {"type": "1", "key": "2054123373"},
  "Sampling Brush Tool": {"type": "1", "key": "1886217314"},
  "Alignment Tool": {"type": "1", "key": "1886216556"},
  "Selection Brush Tool": {"type": "1", "key": "1852273506"},
  "Selection Removal Brush Tool": {"type": "1", "key": "1852273522"},
  # Properties (only need type)
  "Cycle Tool Mode": {"type": "1", "key": ""},
  "Show Edge": {"type": "1", "key": ""},
  "Show Original": {"type": "1", "key": ""},
  "High Quality Preview": {"type": "1", "key": ""},
  "Cycle View Mode": {"type": "1", "key": ""},
  "Disable Views": {"type": "1", "key": ""},
  "Marching Ants": {"type": "1", "key": ""},
  "Overlay": {"type": "1", "key": ""},
  "On Black": {"type": "1", "key": ""},
  "On White": {"type": "1", "key": ""},
  "Black & White": {"type": "1", "key": ""},
  "On Layers": {"type": "1", "key": ""},
  "Onion Skin": {"type": "1", "key": ""},
  "Smart Radius": {"type": "1", "key": ""},
  "Decontaminate Colors": {"type": "1", "key": ""},
  "Show Sampling Area": {"type": "1", "key": ""},
  "Sample All Layers": {"type": "1", "key": ""},
  "Scale": {"type": "1", "key": ""},
  "Mirror": {"type": "1", "key": ""}
}

def read_html_file(file_path):
  tr_blocks = []
  current_block = []
  
  with open(file_path, 'r', encoding='utf-8') as f:
    for line in f:
      line = line.strip()
      if '<tr>' in line:
        # Start a new block
        current_block = [line]
      elif '</tr>' in line:
        # End current block and add to list
        current_block.append(line)
        tr_blocks.append('\n'.join(current_block))
        current_block = []
      elif current_block:
        # Add line to current block
        current_block.append(line)
  
  return tr_blocks

def extract_td_content(line):
  # Pattern to match content between <td...> and </td>
  pattern = r'<td.*?>(.*?)</td>'
  match = re.search(pattern, line)
  if match:
    return match.group(1)
  return None

def extract_shortcut_info(tr_block):
  # Split the tr_block into lines
  lines = tr_block.strip().split('\n')
  
  # Find the command name and shortcut from the relevant td elements
  command_name = None
  shortcut = None
  
  for line in lines:
    line = line.strip()
    if 'colspan="3"' in line:
      # This is the command name line
      command_name = extract_td_content(line)
    elif 'class="shortcutcols"' in line and 'colspan' not in line:
      # This is the shortcut line
      shortcut = extract_td_content(line)
  
  # Only return if both command and shortcut exist
  if command_name and shortcut:
    return command_name, shortcut
  return None

def conversion_loop_part1(infile, outfile):
  tr_blocks = []
  current_block = []
  
  # Reset file pointer to start
  infile.seek(0)
  
  for line in infile:
    line = line.strip()
    if '<tr>' in line:
      current_block = [line]
    elif '</tr>' in line:
      current_block.append(line)
      block = '\n'.join(current_block)
      result = extract_shortcut_info(block)

      if result:
        command_name, shortcut = result
        command_info = COMMAND_TYPES.get(command_name, {"kind": "static", "id": ""})
        # Only include id attribute if it has a value
        id_attr = f' id="{command_info["id"]}"' if command_info["id"] else ''
        outfile.write(f'\t<command kind="{command_info["kind"]}"{id_attr} name="{command_name}">\n')
        outfile.write(f'\t\t<shortcut>{shortcut}</shortcut>\n')
        outfile.write('\t</command>\n')

      current_block = []
    elif current_block:
        current_block.append(line)

def conversion_loop_part2(infile, outfile):
  in_tools_section = False
  current_block = []
  
  # Reset file pointer to start
  infile.seek(0)
  
  for line in infile:
    line = line.strip()
    
    if '<h2>Tools</h2>' in line:
      in_tools_section = True
      continue
    elif '<h2>' in line and in_tools_section:  # New section started
      break  # Exit when new section starts
    
    if not in_tools_section:
      continue
        
    if '<tr>' in line:
      current_block = [line]
      
    elif '</tr>' in line:
      current_block.append(line)
      block = '\n'.join(current_block)
      lines = block.split('\n')
      tool_name = None
      shortcut = None
      
      for line in lines:
        if 'colspan="2"' in line:
          tool_name = extract_td_content(line)
        elif 'class="shortcutcols"' in line and 'width=' not in line:
          shortcut = extract_td_content(line)
          if shortcut == '&nbsp;':
            shortcut = None
      
      if tool_name and shortcut:
        tool_info = TOOL_MAPPINGS.get(tool_name, {"type": "1", "key": ""})
        # Only include key attribute if it has a value
        key_attr = f' key="{tool_info["key"]}"' if tool_info["key"] else ''
        outfile.write(f'\t<tool name="{tool_name}" type="{tool_info["type"]}"{key_attr}>{shortcut}</tool>\n')

      current_block = []
    elif current_block:
      current_block.append(line)

def conversion_loop_part3(infile, outfile):
  in_taskspace_section = False
  current_taskspace = None
  in_properties_section = False
  current_block = []
  
  # Reset file pointer to start
  infile.seek(0)
  
  for line in infile:
    line = line.strip()
    
    if '<h2>Taskspace</h2>' in line:
      in_taskspace_section = True
      continue
    elif '<h2>' in line and in_taskspace_section:  # New section started
      break  # Exit when new section starts
    
    if not in_taskspace_section:
      continue
    
    if '<tr>' in line:
      current_block = [line]
    elif '</tr>' in line:
      current_block.append(line)
      block = '\n'.join(current_block)
      lines = block.split('\n')
      
      for line in lines:
        if 'bgcolor="#cccccc"' in line:
          if current_taskspace:
            outfile.write('\t</taskspace>\n')
          taskspace_name = extract_td_content(line)
          current_taskspace = taskspace_name
          outfile.write(f'\t<taskspace name="{taskspace_name}">\n')
          in_properties_section = False
          break
        
        elif 'Properties and Tool Options' in line:
          in_properties_section = True
          continue
        
        elif current_taskspace and ('class="shortcutcols"' in line):
          name = None
          shortcut = None
          
          for l in lines:
            if 'colspan="2"' in l:
              name = extract_td_content(l)
            elif 'class="shortcutcols"' in l and 'width=' not in line:
              shortcut = extract_td_content(l)
              if shortcut == '&nbsp;':
                  shortcut = None
          
          if name and shortcut:
            mapping = TASKSPACE_MAPPINGS.get(name, {"type": "1", "key": ""})
            if in_properties_section:
              # Properties only use type attribute
              outfile.write(f'\t\t<taskspace-property name="{name}" type="{mapping["type"]}">{shortcut}</taskspace-property>\n')
            else:
              # Only include key attribute for tools if it has a value
              key_attr = f' key="{mapping["key"]}"' if mapping["key"] else ''
              outfile.write(f'\t\t<taskspace-tool name="{name}" type="{mapping["type"]}"{key_attr}>{shortcut}</taskspace-tool>\n')

      current_block = []
    elif current_block:
      current_block.append(line)
  
  if current_taskspace:
    outfile.write('\t</taskspace>\n')

def master_conversion_loop(file_path, output_file_path, output_file_name, output_file_name_no_spaces):
  with open(file_path, 'r', encoding='utf-8') as infile, \
      open(output_file_path, 'w', encoding='utf-8') as outfile:
    
    # Write header once at start
    outfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    outfile.write(f'<photoshop-keyboard-shortcuts version="4" filename="$$$/FileName/Presets/KeyboardCustomization/{output_file_name_no_spaces}={output_file_name}" modified="0" multi-undo="1">\n')
    
    try:
      # Initial pause
      sleep(0.5)
      print("Starting conversion...")
      
      # Part 1
      conversion_loop_part1(infile, outfile)
      for _ in range(random.randint(1, 3)):
        print("...")
        sleep(0.75)
      print("... Section 1 complete")
      
      # Part 2
      conversion_loop_part2(infile, outfile)
      for _ in range(random.randint(1, 3)):
        print("...")
        sleep(0.75)
      print("... Section 2 complete")
      
      # Part 3
      conversion_loop_part3(infile, outfile)
      for _ in range(random.randint(1, 3)):
        print("...")
        sleep(0.75)
      print("... Section 3 complete")

      outfile.write('</photoshop-keyboard-shortcuts>')
      
      print("...Conversion completed successfully!\n")
      print(f"Output file saved as: {output_file_path}\n")
          
    except Exception as e:
      print(f"Error during conversion: {e}")
      raise

def parse_arguments():
  parser = argparse.ArgumentParser(description='Convert Photoshop shortcuts from HTML to KYS format')
  parser.add_argument('-i', '--input', help='Input HTML file path')
  parser.add_argument('-o', '--output', help='Output keymapping name')
  parser.add_argument('-d', '--directory', help='Base directory for input and output files')
  return parser.parse_args()

def get_file_paths_interactive(base_folder):
  file_string = "Enter the filename of the HTM/HTML file to source shortcuts from (provide suffix): "
  output_file_string = "What would you like to name this keymapping? "

  file_name_input = input(file_string)
  # Use Path operator / for joining paths
  file_name = base_folder / file_name_input
  file_name = file_name.resolve()

  output_file_name = input(output_file_string)
  return file_name, output_file_name

def main():
  args = parse_arguments()
  base_folder = pathlib.Path.cwd()

  if args.input and args.output:
    # Command line mode - check for directory argument first
    if args.directory:
      base_folder = pathlib.Path(args.directory)
      base_folder = base_folder.resolve()
      print(f"Using specified directory: {base_folder}")
    else:
      print(f"Using current directory: {base_folder}")
      
    # Process files using provided arguments
    file_name = base_folder / args.input
    file_name = file_name.resolve()
    output_file_name = args.output
    
  else:
    # Interactive mode - prompt for directory
    print(f"Current working directory:\n{base_folder}")
    wd_string = "Enter the base folder to start from (Enter for current directory): "
    base_folder_input = input(wd_string)
    
    if base_folder_input:
      base_folder = pathlib.Path(base_folder_input)
    
    cwd_correct = False
    while not cwd_correct:
      print(f"Base directory is set to: {base_folder}")
      continue_choice = input("Is this correct? (Y for Yes, N for No, Ctrl+C to exit)")
      if continue_choice.upper() == "Y":
        cwd_correct = True
      else:
        base_folder_input = input(wd_string)
        if base_folder_input:
          base_folder = pathlib.Path(base_folder_input)
    
    # Get file paths interactively
    file_name, output_file_name = get_file_paths_interactive(base_folder)

  # Create output path using Path operations
  output_file_full = base_folder / output_file_name
  output_file_full = output_file_full.with_suffix('.kys')
  output_file_full = output_file_full.resolve()
  output_file_name_no_spaces = output_file_name.replace(" ", "")

  print(f"Input file is set to: {file_name}")
  print(f"Output file is set to: {output_file_full}")

  # In command line mode, skip confirmation
  continue_flag = bool(args.input and args.output)
  
  while not continue_flag:
    if file_name == "":
      file_name = pathlib.Path.cwd()
    continue_choice = input("Is this correct? (Y for Yes, N for No, Ctrl+C to exit)")
    if continue_choice.upper() == "Y":
      continue_flag = True
    else:
      file_name, output_file_name = get_file_paths_interactive(base_folder)
      output_file_full = base_folder / output_file_name
      output_file_full = output_file_full.with_suffix('.kys')
      output_file_full = output_file_full.resolve()
      output_file_name_no_spaces = output_file_name.replace(" ", "")
      print(f"Input file is set to: {file_name}")
      print(f"Output file is set to: {output_file_full}")

  if continue_flag:
    master_conversion_loop(file_name, output_file_full, output_file_name, output_file_name_no_spaces)

if __name__ == '__main__':
  main()