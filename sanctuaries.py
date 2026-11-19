import os
import yaml

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ARCH_PATH = os.path.join(ROOT_DIR, "architecture.yml")

DEFAULT_SANCTUARIES = [
    {"name": "Film", "next": "Projector"},
    {"name": "Projector", "next": "Screen"},
    {"name": "Screen", "next": "Theater"},
    {"name": "Theater", "next": None},
]


def load_sanctuaries(arch_path: str = ARCH_PATH) -> list[dict]:
  """architecture.yml から聖域トポロジを読み込む（未存在時はデフォルトを返す）"""
  if os.path.exists(arch_path):
    try:
      with open(arch_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
      sanctuaries = data.get("sanctuaries")
      if isinstance(sanctuaries, list) and sanctuaries:
        return sanctuaries
    except Exception as e:
      print(f"⚠️ architecture.yml の読み込みに失敗しました: {e}")
  return DEFAULT_SANCTUARIES


def materialize_sanctuaries(sanctuaries: list[dict], root_dir: str = ROOT_DIR):
  """各聖域ディレクトリと .gitkeep を自動構築（マテリアライズ）する"""
  for node in sanctuaries:
    name = node.get("name")
    if not name:
      continue
    sanctuary_dir = os.path.join(root_dir, name)
    os.makedirs(sanctuary_dir, exist_ok=True)

    gitkeep_path = os.path.join(sanctuary_dir, ".gitkeep")
    if not os.path.exists(gitkeep_path):
      with open(gitkeep_path, "w", encoding="utf-8") as f:
        f.write("")

    print(f"🏛️ 聖域マテリアライズ完了: {name}/")


def main():
  print("🧭 [StrataChronicle] 第1段階：聖域トポロジの構築を開始します...")
  sanctuaries = load_sanctuaries()
  materialize_sanctuaries(sanctuaries)
  print("✨ [StrataChronicle] すべての聖域が零点の秩序で整いました。")


if __name__ == "__main__":
  main()
