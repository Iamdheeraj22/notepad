from dataclasses import dataclass

@dataclass
class DocumentStatistics:
    """
    A data transfer object (DTO) that holds the current state and statistics
    of the document. This decouples the UI from the calculation logic.
    """
    word_count: int = 0
    char_count: int = 0
    line_count: int = 0
    current_line: int = 1
    current_column: int = 1
    insert_mode: bool = True
    encoding: str = "UTF-8"
    line_ending: str = "CRLF"
    zoom_percentage: int = 100
    is_modified: bool = False

