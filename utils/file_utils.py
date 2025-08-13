import os

def list_files(folder_path: str, extensions: list[str]) -> list[str]:
    """
    List files in folder matching extensions.
    """
    files = []
    for fname in os.listdir(folder_path):
        if any(fname.lower().endswith(ext) for ext in extensions):
            files.append(os.path.join(folder_path, fname))
    return files
