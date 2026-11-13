---
title: "__init__"
date: "2026-11-13"
stage: "Film -> Projector"
author: "StrataChronicle-AI"
status: "Raw-Transformed"
---

# シナリオ台本: __init__

## 1. 原初プロット・素材 (Raw Notes)
import os
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
            print(f"⚠️ 読み込みエラー: {e}")
    return CURRENT_ROOT

SANCTUARY_ROOT = CURRENT_ROOT
NEXT_ROOT = resolve_next_root()

## 2. 演出メモ
- [ ] カット割りの構築
- [ ] 背景（Screen）の選定
