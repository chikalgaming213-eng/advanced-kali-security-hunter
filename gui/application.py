from pathlib import Path
def run_gui(root:Path):
    try:
        from PySide6.QtWidgets import QApplication
        from .main_window import MainWindow
    except ImportError as e: print(f"GUI dependency unavailable: {e}"); return 2
    app=QApplication([]); win=MainWindow(root); win.show(); return app.exec()
