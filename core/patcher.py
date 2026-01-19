import os
import shutil
from datetime import datetime

class SafePatcher:
    @staticmethod
    def apply_patch(file_path, line_number, old_code, new_code):
        backup_path = f"{file_path}.{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
        shutil.copy2(file_path, backup_path)
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
            target_line = lines[line_number - 1].strip()
            if old_code.strip() in target_line or not old_code:
                indent = lines[line_number - 1][:len(lines[line_number - 1]) - len(lines[line_number - 1].lstrip())]
                lines[line_number - 1] = f"{indent}{new_code}\n"
                
                with open(file_path, 'w') as f:
                    f.writelines(lines)
                return True, backup_path
            return False, "патч не применим"
        except Exception as e:
            return False, str(e)