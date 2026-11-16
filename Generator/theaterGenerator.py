import os
import glob
import re
from datetime import datetime
from Generator import BaseGenerator


class TheaterGenerator(BaseGenerator):
    """Theater/ に到達した作品を永久アーカイブとして定着させ、上映ログを記録する"""

    def __init__(self, root_dir: str, src_name: str = "Theater"):
        theater_dir = os.path.join(root_dir, src_name)
        # 終端のため、出力先も自身のディレクトリ（インプレース定着）
        super().__init__(theater_dir, theater_dir)

    def execute(self):
        """終端専用オーバーライド：元ファイルを削除せず、未定着作品のみに刻印して保存する"""
        if not os.path.exists(self.src_dir):
            return

        files = glob.glob(os.path.join(self.src_dir, "*.md"))
        for file_path in files:
            base_name = os.path.basename(file_path)
            if base_name == ".gitkeep":
                continue

            with open(file_path, "r", encoding="utf-8") as f:
                raw_content = f.read()

            # すでに最終上映（Archived）済みの作品はスキップ
            if 'status: "Archived-Feature"' in raw_content:
                continue

            dest_filename, final_content = self.process_content(base_name, raw_content)
            if final_content is not None:
                with open(file_path, "w", encoding="utf-8") as out_f:
                    out_f.write(final_content)
                print(f"    🏛️ [TheaterGenerator] 永久上映アーカイブ定着完了: {dest_filename}")

    def process_content(self, filename: str, raw_content: str) -> tuple[str, str]:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

        archived_content = re.sub(
            r'sanctuary_stage:\s*".*?"',
            'sanctuary_stage: "Theater (Permanent Archive)"',
            raw_content,
        )
        archived_content = re.sub(
            r'status:\s*".*?"',
            'status: "Archived-Feature"',
            archived_content,
        )

        # プレビュー抜粋をログ出力
        preview_lines = [
            line.strip()
            for line in archived_content.splitlines()
            if line.strip() and not line.startswith("---")
        ]
        print(f"       🎬 タイトル抜粋: {preview_lines[0] if preview_lines else filename}")

        footer = f"\n> 🎞️ **Theater Archive Seal**: {now_str} に正式上映作品として永久保存されました。\n"
        return filename, archived_content + footer
