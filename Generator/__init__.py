import os
import glob
import yaml
from abc import ABC, abstractmethod


class BaseGenerator(ABC):
    """全聖域の代謝サイクルと、architecture.yml からの設定オーバーライドを司る基底クラス"""

    def __init__(self, src_dir: str, dest_dir: str):
        self.src_dir = src_dir
        self.dest_dir = dest_dir
        self.root_dir = os.path.dirname(os.path.abspath(src_dir))
        self.sanctuary_name = os.path.basename(src_dir)
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
        """共通の代謝フロー：走査 -> 変換 -> 次聖域へ出力 -> 元ファイル削除"""
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

                dest_filename, formatted_content = self.process_content(base_name, raw_content)

                if formatted_content is not None:
                    dest_path = os.path.join(self.dest_dir, dest_filename)
                    with open(dest_path, "w", encoding="utf-8") as out_f:
                        out_f.write(formatted_content)

                    os.remove(file_path)
                    print(f"    ✨ [{self.__class__.__name__}] {base_name} -> {dest_filename}")

            except Exception as e:
                print(f"    ⚠️ [{self.__class__.__name__}] エラー ({base_name}): {e}")

    @abstractmethod
    def process_content(self, filename: str, raw_content: str) -> tuple[str, str]:
        pass
