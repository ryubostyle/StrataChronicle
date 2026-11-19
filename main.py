import glob
import os
import shutil
import yaml
from datetime import datetime


class DynamicCirculationPipeline:

  def __init__(self):
    self.root_dir = os.path.dirname(os.path.abspath(__file__))
    self.arch_path = os.path.join(self.root_dir, "architecture.yml")
    self.sanctuaries = self._load_architecture()

  def _load_architecture(self):
    """architecture.yml から聖域のトポロジを動的に読み込む"""
    if os.path.exists(self.arch_path):
      try:
        with open(self.arch_path, "r", encoding="utf-8") as f:
          config = yaml.safe_load(f)
        return config.get("sanctuaries", [])
      except Exception as e:
        print(f"⚠️ architecture.yml の読み込みに失敗しました: {e}")
    return [
        {"name": "Film", "next": "Projector"},
        {"name": "Projector", "next": "Screen"},
        {"name": "Screen", "next": "Theater"},
        {"name": "Theater", "next": None},
    ]

  def _get_unique_dest_path(self, dest_dir: str, file_name: str) -> str:
    """宛先に同名ファイルがある場合、上書きせずに連番（_01, _02...）を付与したパスを返す"""
    dest_path = os.path.join(dest_dir, file_name)
    if not os.path.exists(dest_path):
      return dest_path

    stem, ext = os.path.splitext(file_name)
    counter = 1
    while True:
      numbered_name = f"{stem}_{counter:02d}{ext}"
      candidate_path = os.path.join(dest_dir, numbered_name)
      if not os.path.exists(candidate_path):
        return candidate_path
      counter += 1

  def run_metabolism(self):
    print("🎬 [StrataChronicle] 動的シネマティック代謝サイクルを開始します...")
    for i in range(len(self.sanctuaries) - 1):
      current_node = self.sanctuaries[i]
      next_node = self.sanctuaries[i + 1]
      src_name = current_node["name"]
      dest_name = next_node["name"]
      src_dir = os.path.join(self.root_dir, src_name)
      dest_dir = os.path.join(self.root_dir, dest_name)

      if src_name == "Film":
        self._process_film_to_next(src_dir, dest_dir)
      else:
        self._sweep_sanctuary(src_dir, dest_dir, f"[{src_name} -> {dest_name}]")

    self._crystallize_terminal()
    print("✨ [StrataChronicle] 動的代謝サイクルが完遂しました。")

  def _process_film_to_next(self, src_dir: str, dest_dir: str):
    """Film 配下の生テキストを FrontMetaData 付き Markdown に変換して次へ送る"""
    if not os.path.exists(src_dir):
      return
    os.makedirs(dest_dir, exist_ok=True)

    for file_path in sorted(glob.glob(os.path.join(src_dir, "*"))):
      if not os.path.isfile(file_path):
        continue
      base_name = os.path.basename(file_path)
      if base_name == ".gitkeep":
        continue

      try:
        with open(file_path, "r", encoding="utf-8") as f:
          raw_content = f.read().strip()
      except Exception as e:
        print(f"⚠️ 読み込みエラー ({base_name}): {e}")
        continue

      title_stem = os.path.splitext(base_name)[0]
      today_str = datetime.now().strftime("%Y-%m-%d")
      dest_file_name = f"{title_stem}.md"
      dest_path = self._get_unique_dest_path(dest_dir, dest_file_name)
      final_stem = os.path.splitext(os.path.basename(dest_path))[0]

      markdown_content = f"""---
title: "{final_stem}"
date: "{today_str}"
stage: "Dynamic-Circulation"
author: "StrataChronicle-AI"
status: "Crystallized"
---

# シナリオ台本: {final_stem}

## 1. 原初プロット・素材
{raw_content}

## 2. 循環トポロジ情報
- Source: Film
- Processed by: Dynamic Pipeline
"""
      with open(dest_path, "w", encoding="utf-8") as dest_file:
        dest_file.write(markdown_content)
      os.remove(file_path)
      print(
          f"    🎞️ [Film Metabolize] [{base_name}] ->"
          f" {os.path.basename(dest_path)} (次聖域へ)"
      )

  def _sweep_sanctuary(self, src_dir: str, dest_dir: str, label: str):
    """任意の聖域間を動的にスイープ（移送）する（重複時は連番付与）"""
    if not os.path.exists(src_dir):
      return
    os.makedirs(dest_dir, exist_ok=True)

    for file_path in sorted(glob.glob(os.path.join(src_dir, "*"))):
      if not os.path.isfile(file_path):
        continue
      base_name = os.path.basename(file_path)
      if base_name == ".gitkeep":
        continue

      dest_path = self._get_unique_dest_path(dest_dir, base_name)
      shutil.move(file_path, dest_path)
      print(f"    ⚡ {label} 移送: [{os.path.basename(dest_path)}]")

  def _crystallize_terminal(self):
    """終端聖域（Theater）に到達した結晶の観測ログを出力"""
    terminal_node = self.sanctuaries[-1]["name"]
    terminal_dir = os.path.join(self.root_dir, terminal_node)
    if not os.path.exists(terminal_dir):
      return

    for file_path in sorted(glob.glob(os.path.join(terminal_dir, "*"))):
      if not os.path.isfile(file_path):
        continue
      base_name = os.path.basename(file_path)
      if base_name == ".gitkeep":
        continue

      print(f"\n💎✨ [{terminal_node} Terminal Output] 映写・定着完了 ──────")
      print(f"    📜 結晶化作品: [{base_name}]")
      try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
          content = f.read()
        print("    --------------------------------------------------")
        print(content[:300] + ("..." if len(content) > 300 else ""))
        print("    --------------------------------------------------\n")
      except Exception as e:
        print(f"    (Asset read error: {e})")
      print("    🏛️ [Strata Stored] 永遠の地層への定着が完了しました。")


if __name__ == "__main__":
  pipeline = DynamicCirculationPipeline()
  pipeline.run_metabolism()
