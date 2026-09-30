"""
Q8 - Compressed Log Index using Pickle and Zip
"""
import os
import re
import pickle
import zipfile
import sys

TOKEN_PATTERN = re.compile(r"[A-Za-z0-9_]+")

def tokenize(line):
    """Return lowercase normalized tokens from a line."""
    return set(
        token.lower()
        for token in TOKEN_PATTERN.findall(line)
    )

def build_index(folder_path, zip_name):
    """Build inverted index and create ZIP archive."""

    if not os.path.isdir(folder_path):
        raise FileNotFoundError(
            f"Folder not found: {folder_path}"
        )

    index = {}

    total_files = 0
    total_lines = 0

    files = []

    for root, dirs, filenames in os.walk(folder_path):
        for filename in filenames:

            full_path = os.path.join(root, filename)

            if os.path.isfile(full_path):
                files.append(full_path)

    files.sort()

    for file_path in files:

        total_files += 1

        # Store filename relative to the input folder
        relative_path = os.path.relpath(
            file_path,
            folder_path
        )

        try:
            with open(
                file_path,
                "r",
                encoding="utf-8",
                errors="replace"
            ) as file:

                for line_number, line in enumerate(
                    file,
                    start=1
                ):
                    total_lines += 1

                    tokens = tokenize(line)

                    for token in tokens:

                        if token not in index:
                            index[token] = []

                        index[token].append(
                            (relative_path, line_number)
                        )

        except OSError:
            # Skip files that cannot be read
            continue

    pickle_name = "log_index.pkl"

    with open(
        pickle_name,
        "wb"
    ) as file:

        pickle.dump(
            index,
            file,
            protocol=pickle.HIGHEST_PROTOCOL
        )

    with zipfile.ZipFile(
        zip_name,
        "w",
        compression=zipfile.ZIP_DEFLATED
    ) as archive:

        # Add original log files
        for file_path in files:

            if os.path.abspath(file_path) == os.path.abspath(zip_name):
                continue

            relative_path = os.path.relpath(
                file_path,
                folder_path
            )

            archive.write(
                file_path,
                arcname=relative_path
            )

        # Add pickle index
        archive.write(
            pickle_name,
            arcname=pickle_name
        )

    print("FILES", total_files)
    print("LINES", total_lines)
    print("TOKENS", len(index))


def search_index(pickle_path, queries):
    """Load pickle index and search tokens."""

    if not os.path.isfile(pickle_path):
        raise FileNotFoundError(
            f"Pickle file not found: {pickle_path}"
        )

    with open(
        pickle_path,
        "rb"
    ) as file:

        index = pickle.load(file)

    for query in queries:

        token = query.lower()

        matches = index.get(token, [])

        print(token + ":")

        for filename, line_number in matches:
            print(
                f"{filename}:{line_number}"
            )


def main():

    first_line = input().strip()

    if not first_line:
        return

    parts = first_line.split()

    mode = parts[0].upper()

    if mode == "BUILD":

        if len(parts) != 3:
            print("INVALID")
            return

        folder_path = parts[1]
        zip_name = parts[2]

        try:
            build_index(
                folder_path,
                zip_name
            )

        except Exception as e:
            print(
                "ERROR:",
                type(e).__name__,
                str(e)
            )

    elif mode == "SEARCH":

        if len(parts) != 3:
            print("INVALID")
            return

        pickle_path = parts[1]

        try:
            q = int(parts[2])
        except ValueError:
            print("INVALID")
            return

        if q < 0:
            print("INVALID")
            return

        queries = []

        while len(queries) < q:

            try:
                line = input().strip()
            except EOFError:
                break

            if line:
                queries.extend(line.split())

        queries = queries[:q]

        try:
            search_index(
                pickle_path,
                queries
            )

        except Exception as e:
            print(
                "ERROR:",
                type(e).__name__,
                str(e)
            )

    else:
        print("INVALID")


if __name__ == "__main__":
    main()
