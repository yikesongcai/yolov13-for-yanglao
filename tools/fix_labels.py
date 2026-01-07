import os
from pathlib import Path

def fix_labels():
    labels_dir = Path('../datasets/door/labels')
    count = 0
    for txt_file in labels_dir.rglob('*.txt'):
        if txt_file.name == 'classes.txt':
            continue
        try:
            content = txt_file.read_text()
            lines = content.splitlines()
            new_lines = []
            modified = False
            for line in lines:
                parts = line.split()
                if parts and parts[0] != '0':
                    parts[0] = '0'
                    new_lines.append(' '.join(parts))
                    modified = True
                else:
                    new_lines.append(line)
            if modified:
                txt_file.write_text('\n'.join(new_lines) + '\n')
                count += 1
                print(f"Fixed: {txt_file}")
        except Exception as e:
            print(f"Error processing {txt_file}: {e}")
    print(f"Successfully fixed {count} files.")

if __name__ == "__main__":
    fix_labels()
