import re

def fix_configuration_numbers(xdatcar_files):
    new_lines = []
    config_number = 0

    for index, file_name in enumerate(xdatcar_files):
        with open(file_name, 'r') as f:
            lines = f.readlines()

        # Skip the first 7 lines after the first file
        start_index = 0 if index == 0 else 7

        for line_index, line in enumerate(lines[start_index:]):
            if re.match(r'^\s*Direct\s*configuration=\s*\d+', line):
                config_number += 1
                new_line = f'Direct configuration= {config_number}\n'
                new_lines.append(new_line)
            else:
                new_lines.append(line)

    with open('concatenated_xdatcar', 'w') as f:
        f.writelines(new_lines)

if __name__ == '__main__':
    xdatcar_files = ['XDATCAR_1', 'XDATCAR_2','XDATCAR']  # Add your XDATCAR file names here
    fix_configuration_numbers(xdatcar_files)
