import os
import shutil
import argparse
from pathlib import Path


class FileOrganizer:
    def __init__(self, directory):
        self.directory = Path(directory)
        self.file_types = {
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
            'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.xls', '.xlsx', '.ppt', '.pptx'],
            'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
            'Video': ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm'],
            'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
            'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php', '.json', '.xml'],
            'Executables': ['.exe', '.msi', '.dmg', '.pkg', '.deb'],
        }

    def organize_files(self, dry_run=False):
        """Organize files into categorized folders"""
        if not self.directory.exists():
            print(f"❌ Directory {self.directory} does not exist!")
            return

        files_moved = 0

        for file_path in self.directory.iterdir():
            if file_path.is_file():
                category = self.get_file_category(file_path.suffix.lower())

                if category:
                    target_dir = self.directory / category
                    target_dir.mkdir(exist_ok=True)

                    target_path = target_dir / file_path.name

                    if dry_run:
                        print(f"📄 Would move: {file_path.name} -> {category}/")
                    else:
                        try:
                            
                            if target_path.exists():
                                base_name = file_path.stem
                                extension = file_path.suffix
                                counter = 1
                                while target_path.exists():
                                    new_name = f"{base_name}_{counter}{extension}"
                                    target_path = target_dir / new_name
                                    counter += 1

                            shutil.move(str(file_path), str(target_path))
                            print(f"✅ Moved: {file_path.name} -> {category}/")
                            files_moved += 1

                        except Exception as e:
                            print(f"❌ Error moving {file_path.name}: {e}")

        if dry_run:
            print(f"\n🔍 Dry run complete. {files_moved} files would be moved.")
        else:
            print(f"\n🎉 Organization complete! {files_moved} files moved.")

    def get_file_category(self, extension):
        """Determine category for file extension"""
        for category, extensions in self.file_types.items():
            if extension in extensions:
                return category
        return 'Other'

    def list_files_by_type(self):
        """List all files grouped by type"""
        file_groups = {category: [] for category in self.file_types}
        file_groups['Other'] = []

        for file_path in self.directory.iterdir():
            if file_path.is_file():
                category = self.get_file_category(file_path.suffix.lower())
                file_groups[category].append(file_path.name)

        print(f"\n📁 Files in {self.directory}:")
        print("=" * 50)

        total_files = 0
        for category, files in file_groups.items():
            if files:
                print(f"\n{category} ({len(files)} files):")
                for file in sorted(files)[:10]:  
                    print(f"  📄 {file}")
                if len(files) > 10:
                    print(f"  ... and {len(files) - 10} more")
                total_files += len(files)

        print(f"\n📊 Total files: {total_files}")

    def create_custom_category(self, category_name, extensions):
        """Add a custom file category"""
        self.file_types[category_name] = extensions
        print(
            f"✅ Created category '{category_name}' with extensions: {extensions}")


def main():
    parser = argparse.ArgumentParser(
        description='Organize files into categorized folders')
    parser.add_argument('directory', nargs='?', default='.',
                        help='Directory to organize (default: current directory)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be moved without actually moving')
    parser.add_argument('--list', action='store_true',
                        help='List files by type without organizing')

    args = parser.parse_args()

    organizer = FileOrganizer(args.directory)

    if args.list:
        organizer.list_files_by_type()
    else:
        print(f"🚀 Organizing files in: {organizer.directory}")
        print("File categories:", ", ".join(organizer.file_types.keys()))
        print()

        organizer.organize_files(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
