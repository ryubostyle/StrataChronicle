import glob
import os
from abc import ABC, abstractmethod
import yaml


def get_unique_dest_path(dest_dir: str, file_name: str) -> str:
  """宛先に同名ファイルがある場合、上書きせずに _nn 連番（_01, _02...）を付与したパスを返す"""
  dest_path = os.path.join(dest_dir, file_name)
  if not os.path.exists(dest_path):
    return dest_path

  stem, ext = os.path.splitext(file_name)
  counter = 1
  while True:
    candidate_name = f"{stem}_{counter:02d}{ext}"
    candidate_path = os.path.join(dest_dir, candidate_name)
    if not os.path.exists(candidate_path):
      return candidate_path
    counter += 1


class BaseGenerator(ABC):
  """全聖域の代謝サイクルと、architecture.yml からの設定オーバーライドを司る基底クラス"""

  def __init__(self, root_dir: str, src_name: str, dest_name: str = None):
    self.root_dir = os.path.abspath(root_dir)
    self.sanctuary_name = src_name
    self.src_dir = os.path.join(self.root_dir, src_name)
    self.dest_dir = (
        os.path.join(self.root_dir, dest_name) if dest_name else self.src_dir
    )
    self.config = self._load_override_config()

  def _load_override_config(self) -> dict:
    """architecture.yml の generators.<聖域名> があれば取得し、無ければ空辞書を返す"""
    arch_path = os.path.join(self.root_dir, "architecture.yml")
    if os.path.exists(arch_path):
      try:
        with open(arch_path, "r", encoding="utf-8") as f:
          data = yaml.safe_load(f) or {}
        return data.get("generators", {}).get(self.sanctuary_name, {})
      except Exception:
        pass
    return {}

  def execute(self):
    """共通の代謝フロー：走査 -> 変換 -> 次聖域へ出力（重複時は _nn 連番） -> 元ファイル削除"""
    if not os.path.exists(self.src_dir):
      return
    os.makedirs(self.dest_dir, exist_ok=True)
    files = glob.glob(os.path.join(self.src_dir, "*"))
    for file_path in files:
      if not os.path.isfile(file_path):
        continue
      base_name = os.path.basename(file_path)
      if base_name == ".gitkeep":
        continue
      try:
        with open(file_path, "r", encoding="utf-8") as f:
          raw_content = f.read()
        dest_filename, formatted_content = self.process_content(
            base_name, raw_content
        )
        if formatted_content is not None:
          dest_path = get_unique_dest_path(self.dest_dir, dest_filename)
          final_filename = os.path.basename(dest_path)
          with open(dest_path, "w", encoding="utf-8") as out_f:
            out_f.write(formatted_content)
          if os.path.abspath(file_path) != os.path.abspath(dest_path):
            os.remove(file_path)
          print(
              f"    ✨ [{self.__class__.__name__}] {base_name} ->"
              f" {final_filename}"
          )
      except Exception as e:
        print(f"    ⚠️ [{self.__class__.__name__}] エラー ({base_name}): {e}")

  @abstractmethod
  def process_content(self, filename: str, raw_content: str) -> tuple[str, str]:
    pass
