# build_sanctuaries.py
import os
import yaml

def materialize_architecture():
    yml_path = "architecture.yml"
    if not os.path.exists(yml_path):
        print("⚠️ architecture.yml が見つかりません。")
        return

    with open(yml_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    print("🏛️ [StrataChronicle Auto-Builder] フィルム・映画館トポロジに基づく聖域の自動構築を開始します...")

    for sanctuary in config.get("sanctuaries", []):
        name = sanctuary["name"]
        role = sanctuary["role"]
        
        # 聖域フォルダの生成
        if not os.path.exists(name):
            os.makedirs(name)
            print(f"  + 📁 聖域フォルダ生成: {name}/ ({role})")

        # .gitkeep の確保
        gitkeep_path = os.path.join(name, ".gitkeep")
        if not os.path.exists(gitkeep_path):
            with open(gitkeep_path, 'w', encoding='utf-8') as gk:
                pass

        # 各聖域の動的初期化ファイル (__init__.py) の定着
        init_path = os.path.join(name, "__init__.py")
        init_content = f'''import os
import yaml

CURRENT_ROOT = os.path.dirname(os.path.abspath(__file__))
REPOSITORY_ROOT = os.path.dirname(CURRENT_ROOT)
SANCTUARY_NAME = os.path.basename(CURRENT_ROOT)

def resolve_next_root():
    yml_path = os.path.join(REPOSITORY_ROOT, "architecture.yml")
    if os.path.exists(yml_path):
        try:
            with open(yml_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            for s in config.get("sanctuaries", []):
                if s["name"] == SANCTUARY_NAME:
                    next_name = s.get("next")
                    if next_name:
                        return os.path.join(REPOSITORY_ROOT, next_name)
        except Exception as e:
            print(f"⚠️ 読み込みエラー: {{e}}")
    return CURRENT_ROOT

SANCTUARY_ROOT = CURRENT_ROOT
NEXT_ROOT = resolve_next_root()
'''

        with open(init_path, 'w', encoding='utf-8') as init_file:
            init_file.write(init_content)
        print(f"  + 📜 聖域トポロジ定着: {name}/__init__.py")

    print("✨ [StrataChronicle Auto-Builder] すべての聖域の構築が完遂しました。")

if __name__ == "__main__":
    materialize_architecture()
