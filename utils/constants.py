class Constants():

    def __init__(self):
        pass

    appName="Notepad"
    version = "1.0"

    #Hold menu items
    holdMenuItem=[
        "Properties", "Auto Save", "Auto Recovery", 
        "Close All", "Reopen Closed File"
    ]

    file_types = [
        ("Text Files", "*.txt"),
    ]

    FILE_TYPES = {
        "Text File (*.txt)": ".txt",
        "Python File (*.py)": ".py",
        "Markdown (*.md)": ".md",
        "JSON (*.json)": ".json",
        "HTML (*.html)": ".html",
        "All Files (*.*)": ""
    }