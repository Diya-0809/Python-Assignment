"""
Q8 - Compressed Log Index using Pickle and Zip
Python 3.10+
"""
import os
import pickle
import re
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

TOKEN_RE = re.compile(r"[A-Za-z0-9_]+")

def build_index(folder, zip_name):
    folder = Path(folder)
    if not folder.is_dir():
        raise ValueError("Folder does not exist.")

    index = defaultdict(list)
    total_files = 0
    total_lines = 0
    source_files = []

    for path in sorted(folder.iterdir()):
        if not path.is_file():
            continue

        total_files += 1
        source_files.append(path)
        with path.open("r", encoding="utf-8", errors="replace") as f:
            for line_no, line in enumerate(f, 1):
                total_lines += 1
                for token in set(TOKEN_RE.findall(line.lower())):
                    index[token].append((path.name, line_no))

    pickle_path = folder / "_log_index.pkl"
    with pickle_path.open("wb") as f:
        pickle.dump(dict(index), f, protocol=pickle.HIGHEST_PROTOCOL)

    with zipfile.ZipFile(zip_name, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for path in source_files:
            z.write(path, arcname=path.name)
        z.write(pickle_path, arcname="log_index.pkl")

    pickle_path.unlink()
    print("FILES", total_files)
    print("LINES", total_lines)
    print("TOKENS", len(index))

def search_index(pickle_path, queries):
    with open(pickle_path, "rb") as f:
        index = pickle.load(f)

    for token in queries:
        matches = index.get(token.lower(), [])
        for filename, line_no in matches:
            print(f"{token}: {filename}:{line_no}")

def main():
    mode = input().strip().upper()

    if mode == "BUILD":
        parts = input().split()
        if len(parts) != 2:
            raise ValueError("BUILD requires: folder_path zip_name")
        build_index(parts[0], parts[1])

    elif mode == "SEARCH":
        parts = input().split()
        if len(parts) < 2:
            raise ValueError("SEARCH requires: pickle_path q [tokens...]")
        pickle_path = parts[0]
        q = int(parts[1])
        queries = parts[2:]
        if len(queries) != q:
            raise ValueError("Query count does not match q.")
        search_index(pickle_path, queries)

    else:
        raise ValueError("Mode must be BUILD or SEARCH.")

if __name__ == "__main__":
    main()
