"""Dataset Util
A script that finds and deletes Non-Economic duplicates in the dataset
"""
import csv
import os


def delete_multiple_lines(original_file, line_numbers):
    """In a file, delete the lines at line number in given list"""
    is_skipped = False
    if not line_numbers:
        return
    counter = 0
    dummy_file = original_file + '.bak'
    with open(original_file, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        for line in read_obj:
            if counter not in line_numbers:
                write_obj.write(line)
            else:
                is_skipped = True
            counter += 1
    if is_skipped:
        os.remove(original_file)
        os.rename(dummy_file, original_file)
    else:
        os.remove(dummy_file)


if __name__ == '__main__':
    seen = set()
    lineNumbers = []
    with open('forex_factory_catalog.csv', mode='r') as file:
        reader = csv.reader(file, delimiter=',')
        for i, row in enumerate(reader):
            # Remove rows where all fields except date are empty
            if row[0] and all(not field.strip() for field in row[1:]):
                lineNumbers.append(i)
                continue
            row_tuple = tuple(row)
            if row_tuple in seen:
                lineNumbers.append(i)
            else:
                seen.add(row_tuple)
    delete_multiple_lines(original_file='forex_factory_catalog.csv', line_numbers=lineNumbers)
