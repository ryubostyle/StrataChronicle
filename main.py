# main.py (Auto-synced by build_sanctuaries.py)
import os
import glob
import shutil
import yaml
from Generator import get_unique_dest_path
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
        transitions = [
            (self.sanctuaries[i]["name"], self.sanctuaries[i + 1]["name"])
            for i in range(len(self.sanctuaries) - 1)
        ]
        for src_name, dest_name in transitions:
            gen_cls = self.GENERATOR_MAP.get(src_name)
            if gen_cls:
                gen_cls(self.root_dir, src_name=src_name, dest_name=dest_name).execute()
            else:
                src_dir = os.path.join(self.root_dir, src_name)
                dest_dir = os.path.join(self.root_dir, dest_name)
                self._sweep(src_dir, dest_dir, f"[{src_name} -> {dest_name}]")
        if self.sanctuaries:
            term_name = self.sanctuaries[-1]["name"]
            if term_name == "Theater":
                TheaterGenerator(self.root_dir, src_name=term_name).execute()
            else:
                self._crystallize(term_name)
        print("✨ [StrataChronicle] 代謝サイクルが完遂しました。")

    def _sweep(self, src: str, dest: str, label: str):
        if not os.path.exists(src):
            return
        os.makedirs(dest, exist_ok=True)
        for path in glob.glob(os.path.join(src, "*")):
            if os.path.isfile(path):
                base = os.path.basename(path)
                if base == ".gitkeep":
                    continue
                dest_path = get_unique_dest_path(dest, base)
                shutil.move(path, dest_path)
                print(f"    ⚡ {label} 移送: {os.path.basename(dest_path)}")

    def _crystallize(self, term: str):
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
