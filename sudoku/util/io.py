from __future__ import annotations


class SudokuIO:
    @staticmethod
    def read_from_file(path: str) -> str:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def write_to_file(path: str, content: str) -> None:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
