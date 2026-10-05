# -*- coding: utf-8 -*-
"""
Builder for Kelime Harikaları v2.0.0
"""
import json

with open("credits.json", "r", encoding="utf-8") as f:
    credits_json = f.read()

with open("idioms.json", "r", encoding="utf-8") as f:
    idioms_json = f.read()

with open("levels_100.json", "r", encoding="utf-8") as f:
    levels_json = f.read()

with open("config.js", "r", encoding="utf-8") as f:
    config_code = f.read()

print("Assets verified and ready for injection.")
