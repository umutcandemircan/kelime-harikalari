import json
import os
import sys

def validate_words():
    print("=== QA AUDIT: WORD VALIDATION & CONTENT POLICY ===")
    
    dict_path = 'data/dictionary/tdk_snapshot_v2.json'
    policy_path = 'data/dictionary/content_policy_blocked.json'
    levels_path = 'data/levels/tr_levels.json'

    if not os.path.exists(dict_path) or not os.path.exists(policy_path) or not os.path.exists(levels_path):
        print("ERROR: Required data files missing.")
        sys.exit(1)

    with open(dict_path, 'r', encoding='utf-8') as f:
        tdk_data = json.load(f)
        tdk_words = set(tdk_data.get('words', []))

    with open(policy_path, 'r', encoding='utf-8') as f:
        policy_data = json.load(f)
        blocked_words = set(policy_data.get('blocked', []))

    with open(levels_path, 'r', encoding='utf-8') as f:
        levels = json.load(f)

    errors = []
    total_words_checked = 0

    for lvl in levels:
        lvl_id = lvl.get('id', 'unknown')
        for w_obj in lvl.get('words', []):
            total_words_checked += 1
            word = w_obj.get('word', '')
            
            # 1. Content Policy Check
            if word in blocked_words:
                errors.append(f"WORD_POLICY_VIOLATION: Level {lvl_id} contains inappropriate word: '{word}'")

            # 2. TDK Dictionary Check
            if word not in tdk_words:
                errors.append(f"WORD_NOT_IN_TDK: Level {lvl_id} word '{word}' not found in TDK snapshot")

    if errors:
        print(f"FAILED: Found {len(errors)} word errors:")
        for e in errors[:10]:
            print(f"  - {e}")
        sys.exit(1)

    print(f"SUCCESS: All {total_words_checked} puzzle words validated against TDK snapshot & Content Policy! Zero policy violations.")

if __name__ == '__main__':
    validate_words()
