import os
import re
from datetime import datetime
from Generator import BaseGenerator


class ScreenGenerator(BaseGenerator):
    """Screen/ 配下の投影データを最終鑑賞フォーマットへ整形し、Theater/ へ送出する"""

    def __init__(self, root_dir: str, src_name: str = "Screen", dest_name: str = "Theater"):
        src_dir = os.path.join(root_dir, src_name)
        dest_dir = os.path.join(root_dir, dest_name)
        super().__init__(src_dir, dest_dir)

    def process_content(self, filename: str, raw_content: str) -> tuple[str, str]:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

        # ステータスとステージのメタデータを更新
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

        # スクリーン演出ヘッダーの付与
        screen_block = f"""
---

## 4. スクリーン定着・マスタープリント記録
- **定着日時**: {now_str}
- **状態**: すべての光と文脈がスクリーン上で結像しました。`Theater/` での永久上映待機中。
"""
        return filename, updated_content + screen_block
