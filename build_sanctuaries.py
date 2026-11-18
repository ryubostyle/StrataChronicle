# build_sanctuaries.py
import os
import yaml

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ARCH_PATH = os.path.join(ROOT_DIR, "architecture.yml")
GENERATOR_DIR = os.path.join(ROOT_DIR, "Generator")
MAIN_PY_PATH = os.path.join(ROOT_DIR, "main.py")

DEFAULT_ARCHITECTURE = {
    "system": "StrataChronicle",
    "version": "2.0.0",
    "sanctuaries": [
        {"name": "Film", "next": "Projector", "role": "Raw draft intake & script binding"},
        {"name": "Projector", "next": "Screen", "role": "Scene structuring & optical projection"},
        {"name": "Screen", "next": "Theater", "role": "Visual formatting & master print"},
        {"name": "Theater", "next": None, "role": "Permanent archive & final screening"},
    ],
}

# --- テンプレート群 ---

BASE_INIT_TEMPLATE = '''import os
import glob
import yaml
from abc import ABC, abstractmethod


class BaseGenerator(ABC):
    """全聖域の代謝サイクルと、architecture.yml からの設定オーバーライドを司る基底クラス"""

    def __init__(self, root_dir: str, src_name: str, dest_name: str = None):
        self.root_dir = os.path.abspath(root_dir)
        self.sanctuary_name = src_name
        self.src_dir = os.path.join(self.root_dir, src_name)
        self.dest_dir = os.path.join(self.root_dir, dest_name) if dest_name else self.src_dir
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

                    if os.path.abspath(file_path) != os.path.abspath(dest_path):
                        os.remove(file_path)
                    print(f"    ✨ [{self.__class__.__name__}] {base_name} -> {dest_filename}")

            except Exception as e:
                print(f"    ⚠️ [{self.__class__.__name__}] エラー ({base_name}): {e}")

    @abstractmethod
    def process_content(self, filename: str, raw_content: str) -> tuple[str, str]:
        pass
'''

MAIN_PY_TEMPLATE = '''# main.py (Auto-synced by build_sanctuaries.py)
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
                dest_path = os.path.join(dest, base)
                if os.path.exists(dest_path):
                    os.remove(dest_path)
                shutil.move(path, dest_path)
                print(f"    ⚡ {label} 移送: {base}")

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
'''


def ensure_architecture() -> list[dict]:
    if not os.path.exists(ARCH_PATH):
        with open(ARCH_PATH, "w", encoding="utf-8") as f:
            yaml.safe_dump(DEFAULT_ARCHITECTURE, f, allow_unicode=True, sort_keys=False)
        print("📜 architecture.yml を新規生成しました。")
        return DEFAULT_ARCHITECTURE["sanctuaries"]

    with open(ARCH_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}
    return config.get("sanctuaries", DEFAULT_ARCHITECTURE["sanctuaries"])


def build_sanctuary_dirs(sanctuaries: list[dict]):
    for node in sanctuaries:
        name = node["name"]
        s_dir = os.path.join(ROOT_DIR, name)
        os.makedirs(s_dir, exist_ok=True)
        gitkeep_path = os.path.join(s_dir, ".gitkeep")
        if not os.path.exists(gitkeep_path):
            with open(gitkeep_path, "w", encoding="utf-8") as f:
                f.write("")
        print(f"🏛️ 聖域構築完了: {name}/")


def ensure_generator_package():
    os.makedirs(GENERATOR_DIR, exist_ok=True)
    init_path = os.path.join(GENERATOR_DIR, "__init__.py")
    if not os.path.exists(init_path):
        with open(init_path, "w", encoding="utf-8") as f:
            f.write(BASE_INIT_TEMPLATE)
        print("🧬 Generator/__init__.py (BaseGenerator) を生成しました。")
    else:
        print("🧬 Generator/__init__.py は既に存在するため保護しました。")


def sync_main_py():
    with open(MAIN_PY_PATH, "w", encoding="utf-8") as f:
        f.write(MAIN_PY_TEMPLATE)
    print("⚙️ main.py を最新の動的ジェネレータ構成へ同期しました。")


def main():
    print("🏗️ [StrataChronicle] 聖域・パイプライン構築を開始します...")
    sanctuaries = ensure_architecture()
    build_sanctuary_dirs(sanctuaries)
    ensure_generator_package()
    sync_main_py()
    print("✅ [StrataChronicle] すべての聖域および起動システムの構築が完了しました。")


if __name__ == "__main__":
    main()
