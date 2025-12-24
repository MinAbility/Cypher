def scan_note_files(self):
        notes_dir = pathlib.Path(__file__).parent / "Notes"
        if notes_dir.exists():
            self.note_files = [f.stem for f in notes_dir.glob('*.txt')]
            logger.info(f"Found {len(self.note_files)} note files: {self.note_files}")
        else:
            self.note_files = []
            logger.warning("Notes directory not found")
    