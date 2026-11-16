# main.py
import os
import glob
import shutil
import yaml

from Generator.filmGenerator import FilmGenerator
from Generator.projectorGenerator import ProjectorGenerator
from Generator.screenGenerator import ScreenGenerator
from Generator.theaterGenerator import TheaterGenerator


class DynamicCirculationPipeline:
    """architecture.yml のトポロジに基づき、各聖域のGeneratorを動的駆動する司令塔"""

    GENERATOR_MAP = {
        "Film": FilmGenerator,
        "Projector": ProjectorGenerator,
        "Screen": ScreenGenerator,
    }

    def __init__(self):
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        self.arch_path = os.path.join(self.root_dir, "architecture.yml")
        self.sanctuaries = self._load_architecture()

    def _load_architecture(self):
        if os.path.exists(self.arch_path):
            try:
                with open(self.arch_path, "r", encoding="utf-8") as f:
                    config = yaml.safe_load(f)
                    return config.get("sanctuaries", [])
            except Exception as e:
                print(f"⚠️ architecture.yml の読み込みエラー: {e}")
        return [
            {"name": "Film", "next": "Projector"},
            {"name": "Projector", "next": "Screen"},
            {"name": "Screen", "next": "Theater"},
            {"name": "Theater", "next": None},
        ]

    def run_metabolism(self):
        print("🎬 [StrataChronicle] 動的代謝サイクルを開始します...")

        # 上流から下流への遷移リストを構築
        transitions = [
            (self.sanctuaries[i]["name"], self.sanctuaries[i + 1]["name"])
            for i in range(len(self.sanctuaries) - 1)
        ]

        # 1. 各聖域間の代謝・加工リレー
        for src_name, dest_name in transitions:
            gen_cls = self.GENERATOR_MAP.get(src_name)
            if gen_cls:
                gen_cls(self.root_dir, src_name=src_name, dest_name=dest_name).execute()
            else:
                # GENERATOR_MAP に未登録の拡張聖域が追加された場合の汎用スイープ
                src_dir = os.path.join(self.root_dir, src_name)
                dest_dir = os.path.join(self.root_dir, dest_name)
                self._sweep(src_dir, dest_dir, f"[{src_name} -> {dest_name}]")

        # 2. 終端聖域での定着・アーカイブ処理
        if self.sanctuaries:
            term_name = self.sanctuaries[-1]["name"]
            if term_name == "Theater":
                TheaterGenerator(self.root_dir, src_name=term_name).execute()
            else:
                self._crystallize(term_name)

        print("✨ [StrataChronicle] 代謝サイクルが完遂しました。")

    def _sweep(self, src: str, dest: str, label: str):
        """専用Generatorを持たない拡張聖域用のフォールバック移送"""
        if not os.path.exists(src):
            return
        os.makedirs(dest, exist_ok=True)
        for path in glob.glob(os.path.join(src, "*")):
            if os.path.isfile(path):
                base = os.path.basename(path)
                if base == ".gitkeep":
                    continue
                dest_path = os.path.join(dest, base)
                if os.path.exists(dest_path):
                    os.remove(dest_path)
                shutil.move(path, dest_path)
                print(f"    ⚡ {label} 移送: {base}")

    def _crystallize(self, term: str):
        """Theater 以外のカスタム終端聖域が指定された場合のログ出力"""
        term_dir = os.path.join(self.root_dir, term)
        if not os.path.exists(term_dir):
            return
        for path in glob.glob(os.path.join(term_dir, "*")):
            if os.path.isfile(path):
                base = os.path.basename(path)
                if base == ".gitkeep":
                    continue
                print(f"    💎✨ [{term}] 映写完了: {base}")


if __name__ == "__main__":
    pipeline = DynamicCirculationPipeline()
    pipeline.run_metabolism()
