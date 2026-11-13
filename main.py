# main.py
import os
import glob
import shutil
from datetime import datetime

class CinematicCirculationPipeline:
    def __init__(self):
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        self.film_dir = os.path.join(self.root_dir, "Film")
        self.projector_dir = os.path.join(self.root_dir, "Projector")
        self.screen_dir = os.path.join(self.root_dir, "Screen")
        self.theater_dir = os.path.join(self.root_dir, "Theater")

    def run_metabolism(self):
        print("🎬 [StrataChronicle] シネマティック代謝サイクルを開始します...")
        
        # 1. Film -> Projector (生テキストのシナリオ化・YAML付与)
        self._process_film_to_projector()
        
        # 2. Projector -> Screen (パススルー移送)
        self._sweep_sanctuary(self.projector_dir, self.screen_dir, "🎥 [Projector -> Screen]")
        
        # 3. Screen -> Theater (最終的な映写館へ結晶化)
        self._sweep_sanctuary(self.screen_dir, self.theater_dir, "📺 [Screen -> Theater]")
        
        # 4. Theater での結晶化ログ定着
        self._crystallize_theater()
        
        print("✨ [StrataChronicle] 今回の代謝サイクルが完了しました。")

    def _process_film_to_projector(self):
        """Film 配下の生テキストを FrontMetaData 付きのシナリオ Markdown に変換する"""
        if not os.path.exists(self.film_dir):
            return
        if not os.path.exists(self.projector_dir):
            os.makedirs(self.projector_dir)

        files = glob.glob(os.path.join(self.film_dir, "*"))
        for file_path in files:
            if os.path.isfile(file_path):
                base_name = os.path.basename(file_path)
                if base_name == ".gitkeep":
                    continue

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        raw_content = f.read().strip()
                except Exception as e:
                    print(f"⚠️ 読み込みエラー ({base_name}): {e}")
                    continue

                title_stem = os.path.splitext(base_name)[0]
                today_str = datetime.now().strftime("%Y-%m-%d")

                # YAML Front Matter 付きのシナリオ Markdown を構築
                markdown_content = f"""---
title: "{title_stem}"
date: "{today_str}"
stage: "Film -> Projector"
author: "StrataChronicle-AI"
status: "Raw-Transformed"
---

# シナリオ台本: {title_stem}

## 1. 原初プロット・素材 (Raw Notes)
{raw_content}

## 2. 演出メモ
- [ ] カット割りの構築
- [ ] 背景（Screen）の選定
"""

                dest_file_name = f"{title_stem}.md"
                dest_path = os.path.join(self.projector_dir, dest_file_name)

                with open(dest_path, 'w', encoding='utf-8') as dest_file:
                    dest_file.write(markdown_content)

                os.remove(file_path)
                print(f"    🎞️ [Film -> Projector] 台本生成・変換: [{base_name}] -> {dest_file_name}")

    def _sweep_sanctuary(self, src_dir: str, dest_dir: str, label: str):
        if not os.path.exists(src_dir):
            return
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        files = glob.glob(os.path.join(src_dir, "*"))
        for file_path in files:
            if os.path.isfile(file_path):
                base_name = os.path.basename(file_path)
                if base_name == ".gitkeep":
                    continue
                
                dest_path = os.path.join(dest_dir, base_name)
                if os.path.exists(dest_path):
                    os.remove(dest_path)
                
                shutil.move(file_path, dest_path)
                print(f"    {label} 移送: [{base_name}] -> {os.path.basename(dest_dir)}")

    def _crystallize_theater(self):
        if not os.path.exists(self.theater_dir):
            return

        files = glob.glob(os.path.join(self.theater_dir, "*"))
        for file_path in files:
            if os.path.isfile(file_path):
                base_name = os.path.basename(file_path)
                if base_name == ".gitkeep":
                    continue

                print(f"\n    💎✨ [Theater Screen Output] 映写完了 ──────────────────")
                print(f"    📜 上映作品: [{base_name}]")
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        print(f"    --------------------------------------------------")
                        print(content[:400] + ("..." if len(content) > 400 else ""))
                        print(f"    --------------------------------------------------\n")
                except Exception as e:
                    print(f"    (Binary asset: {e})")

                print(f"    🏛️ [Strata Stored] 映画館の地層に作品が永遠に刻まれました: [{base_name}]")

if __name__ == "__main__":
    pipeline = CinematicCirculationPipeline()
    pipeline.run_metabolism()
