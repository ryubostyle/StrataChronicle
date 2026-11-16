import os
import glob
import shutil
from abc import ABC, abstractmethod

class BaseGenerator(ABC):
    """全聖域の代謝サイクルを司る基底ジェネレータ"""

    def __init__(self, src_dir: str, dest_dir: str):
        self.src_dir = src_dir
        self.dest_dir = dest_dir

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

                # サブクラス固有の変換・製本ロジックを実行
                dest_filename, formatted_content = self.process_content(base_name, raw_content)

                if formatted_content is not None:
                    dest_path = os.path.join(self.dest_dir, dest_filename)
                    with open(dest_path, "w", encoding="utf-8") as out_f:
                        out_f.write(formatted_content)

                    # 代謝完了した元ファイルを除去
                    os.remove(file_path)
                    print(f"    ✨ [{self.__class__.__name__}] {base_name} -> {dest_filename}")

            except Exception as e:
                print(f"    ⚠️ [{self.__class__.__name__}] エラー ({base_name}): {e}")

    @abstractmethod
    def process_content(self, filename: str, raw_content: str) -> tuple[str, str]:
        """
        各聖域固有の加工ロジック（サブクラスで必ず実装する）
        戻り値: (出力ファイル名, 加工後のテキスト内容)
        """
        pass
