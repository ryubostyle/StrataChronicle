import os
import re
from datetime import datetime
from Generator import BaseGenerator


class ScreenGenerator(BaseGenerator):
    """Screen/ 配下の投影データを最終鑑賞フォーマットへ整形し、Theater/ へ送出する"""

    def __init__(self, root_dir: str, src_name: str = "Screen", dest_name: str = "Theater"):
        super().__init__(os.path.join(root_dir, src_name), os.path.join(root_dir, dest_name))

    def process_content(self, filename: str, raw_content: str) -> tuple[str, str]:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

        # デフォルト設定（architecture.yml の generators.Screen で上書き可能）
        screen_type = self.config.get("screen_type", "IMAX Silver Screen")

        updated_content = re.sub(
            r'sanctuary_stage:\s*".*?"',
            'sanctuary_stage: "Screen -> Theater"',
            raw_content,
        )
        updated_content = re.sub(
            r'status:\s*".*?"',
            'status: "Master-Print"',
            updated_content,
        )

        updated_content = updated_content.replace(
            "- [ ] ビジュアル・カット割り当て",
            f"- [x] ビジュアル・カット割り当て（{now_str} Screen定着済）",
        )

        screen_block = f"""
---

## 4. スクリーン定着・マスタープリント記録
- **定着日時**: {now_str}
- **スクリーン仕様**: {screen_type}
- **状態**: すべての光と文脈がスクリーン上で結像しました。`Theater/` での永久上映待機中。
"""
        return filename, updated_content + screen_block
