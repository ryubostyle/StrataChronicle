import os
import re
from datetime import datetime
from Generator import BaseGenerator


class ProjectorGenerator(BaseGenerator):
    """Projector/ 配下の台本をシーン分割・構造化し、Screen/ へ投影準備する"""

    def __init__(self, root_dir: str, src_name: str = "Projector", dest_name: str = "Screen"):
        super().__init__(os.path.join(root_dir, src_name), os.path.join(root_dir, dest_name))

    def process_content(self, filename: str, raw_content: str) -> tuple[str, str]:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

        # デフォルト設定（architecture.yml の generators.Projector で上書き可能）
        aspect_ratio = self.config.get("aspect_ratio", "16:9 Cinema")

        updated_content = re.sub(
            r'sanctuary_stage:\s*".*?"',
            'sanctuary_stage: "Projector -> Screen"',
            raw_content,
        )
        updated_content = re.sub(
            r'status:\s*".*?"',
            'status: "Projected-Cut"',
            updated_content,
        )

        updated_content = updated_content.replace(
            "- [ ] シーン分割の確定",
            f"- [x] シーン分割の確定（{now_str} Projector処理済）",
        )

        projection_block = f"""
---

## 3. 映写・カット構成（Projector 生成レイヤー）
- **投影日時**: {now_str}
- **投影フォーマット**: {aspect_ratio}
- **光学変換ステータス**: シーン構成の最適化完了（Screen への照射準備完了）
"""
        return filename, updated_content + projection_block
