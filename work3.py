import os

def find_keywords(list_file, key_file, result_file, checkpoint_file='checkpoint.txt'):
    # Load the checkpoint if it exists
    start_page = 1
    matched_keywords = {}
    total_matched = 0
    total_unmatched = 0

    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as checkpoint_f:
            lines = checkpoint_f.readlines()
            if lines:
                start_page = int(lines[0].strip())
                total_matched = int(lines[1].strip())
                total_unmatched = int(lines[2].strip())
                matched_keywords = eval(lines[3].strip())

    # Read list and key content once to avoid repeated I/O operations
    with open(list_file, 'r') as list_f:
        list_content = list_f.readlines()

    with open(key_file, 'r') as key_f:
        key_set = set(key_f.read().splitlines())

    total_lines = len(list_content)

    for page_number in range(start_page, total_lines + 1):
        line = list_content[page_number - 1].strip()
        if line in key_set:
            total_matched += 1
            if line not in matched_keywords:
                matched_keywords[line] = [page_number]
            else:
                matched_keywords[line].append(page_number)
        else:
            total_unmatched += 1

        # Print status
        if page_number % 100 == 0:  # Print status every 100 lines
            print(f"Total lines: {total_lines}, Unmatched strings: {total_unmatched}, Matched strings: {total_matched}")

        # Save checkpoint every 100 lines to reduce I/O overhead
        if page_number % 100 == 0:
            with open(checkpoint_file, 'w') as checkpoint_f:
                checkpoint_f.write(f"{page_number + 1}\n")
                checkpoint_f.write(f"{total_matched}\n")
                checkpoint_f.write(f"{total_unmatched}\n")
                checkpoint_f.write(f"{matched_keywords}\n")

    with open(result_file, 'w') as result_f:
        for keyword, pages in matched_keywords.items():
            result_f.write(f"{keyword}: {', '.join(map(str, pages))}\n")

    # Remove checkpoint file after completion
    if os.path.exists(checkpoint_file):
        os.remove(checkpoint_file)

# Usage
list_file = 'List.txt'
key_file = 'block.txt'
result_file = 'KEYFOUND.txt'
checkpoint_file = 'checkpoint.txt'

find_keywords(list_file, key_file, result_file, checkpoint_file)

