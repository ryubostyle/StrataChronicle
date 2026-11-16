import os
import re
from datetime import datetime
from Generator import BaseGenerator


class FilmGenerator(BaseGenerator):
    """Film/ 配下の殴り書きメモを構造化された台本（Markdown）へと製本する"""

    def __init__(self, root_dir: str, src_name: str = "Film", dest_name: str = "Projector"):
        super().__init__(os.path.join(root_dir, src_name), os.path.join(root_dir, dest_name))

    def process_content(self, filename: str, raw_content: str) -> tuple[str, str]:
        stem = os.path.splitext(filename)[0]
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

        # デフォルト設定（architecture.yml に generators.Film があれば上書きされる）
        mode = self.config.get("mode", "rule_based")  # "rule_based" | "dialogue"
        chapter_prefix = self.config.get("chapter_prefix", "第{n}節")

        # 1. クレンジング（行末空白除去・連続空行の圧縮）
        lines = [line.rstrip() for line in raw_content.strip().splitlines()]
        cleaned_text = re.sub(r"\n{3,}", "\n\n", "\n".join(lines))
        paragraphs = [p.strip() for p in cleaned_text.split("\n\n") if p.strip()]
        if not paragraphs:
            return f"{stem}.md", None

        # 2. タイトル抽出
        first_line = paragraphs[0].splitlines()[0]
        book_title = re.sub(r"^[#・\-\* \s]+", "", first_line)[:50] or stem

        # 3. モードに応じた本文の製本整形
        if mode == "dialogue":
            body = self._format_dialogue(paragraphs)
        else:
            body = self._format_chapters(paragraphs, chapter_prefix)

        char_count = len(re.sub(r"\s+", "", cleaned_text))

        # 4. FrontMatter + 本文の結合
        bound_script = f"""---
title: "{book_title}"
source_file: "{filename}"
bound_at: "{now_str}"
binding_mode: "{mode}"
char_count: {char_count}
sanctuary_stage: "Film -> Projector"
status: "Bound-Script"
---

# 📜 {book_title}

> **製本記録**: `{filename}` より自動編纂（{char_count} 文字 / モード: `{mode}`）

---

{body}

---

## 演出・シーン展開ノート（Projector 引き継ぎ領域）
- [ ] シーン分割の確定
- [ ] ビジュアル・カット割り当て
"""
        return f"{stem}.md", bound_script

    def _format_chapters(self, paragraphs: list[str], prefix_tpl: str) -> str:
        """デフォルト：段落ごとの章立て＆箇条書き・TODO正規化"""
        chapters = []
        for idx, para in enumerate(paragraphs, start=1):
            p = re.sub(r"^[・＊●]\s*", "- ", para, flags=re.MULTILINE)
            p = re.sub(r"^(?:TODO|todo|タスク)[:：]\s*(.+)$", r"- [ ] \1", p, flags=re.MULTILINE)
            chapters.append(f"### {prefix_tpl.format(n=idx)}\n\n{p}")
        return "\n\n".join(chapters)

    def _format_dialogue(self, paragraphs: list[str]) -> str:
        """オプション：セリフ・ト書きを台本レイアウトへ変換"""
        speaker_re = re.compile(r"^([^：:「『\n]{1,15})[：:](.+)$")
        scenes = []
        for idx, para in enumerate(paragraphs, start=1):
            converted = []
            for line in para.splitlines():
                s = line.strip()
                m = speaker_re.match(s)
                if m:
                    converted.append(f"**{m.group(1).strip()}**\n> 「{m.group(2).strip().strip('「」『』')}」")
                elif s.startswith(("（", "(")) and s.endswith(("）", ")")):
                    converted.append(f"*（ト書き：{s[1:-1]}）*")
                else:
                    converted.append(s)
            scenes.append(f"### 🎬 SCENE {idx}\n\n" + "\n\n".join(converted))
        return "\n\n".join(scenes)
