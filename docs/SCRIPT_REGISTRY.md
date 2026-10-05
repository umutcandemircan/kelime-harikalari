# Sözcük Seferî — Script Registry & Lifecycle Classification

| Script Path | Category | Status | Purpose & Description |
| :--- | :--- | :--- | :--- |
| `tools/build.py` | BUILD | **ACTIVE** | Main production build pipeline. Validates template, audits crossword datasets, bundles CSS & JS, checks syntax via Node, and compiles `index.html`. |
| `tools/build_verified_dataset.py` | BUILD | **ACTIVE** | Compiles and validates 186 levels across 81 provinces from showcase data, levels_100, and TDK dictionary. |
| `tools/find_strict_crosswords.py` | BUILD / CORE | **ACTIVE** | Algorithmic solver for strict non-adjacent crosswords (90-deg intersections, Manhattan distance >= 2). |
| `tools/generate_pwa_icons.py` | BUILD | **ACTIVE** | Generates compliant PWA icon assets (`icon-192.png`, `icon-512.png`) using pure Python without external dependencies. |
| `tools/clean_province_names.py` | DATA | **ACTIVE** | Normalizes Turkish province names in SVG map datasets. |
| `tools/generate_turkey_map_data.py` | DATA | **ACTIVE** | Extracts SVG path centroids and plate metadata for Turkey map. |
| `tools/generate_tdk_dict.py` | DATA | **ACTIVE** | Extracts approved word pools from raw Turkish dictionary data. |
| `tools/extract.py` | REFACTOR | **LEGACY** | Extracted monolithic HTML into early modular prototype. |
| `tools/split_js.py` | REFACTOR | **LEGACY** | Early modular JS splitting utility. |
| `tools/cleanup.py` | MAINTENANCE | **LEGACY** | Initial repository root cleanup script. |
| `tools/clean_template.py` | MAINTENANCE | **LEGACY** | Cleaned initial template layer. |
| `tools/apply_resolved_photos.py` | ASSET | **LEGACY** | Batch updated Unsplash photos for early landmark models. |
| `tools/resolve_all_landmark_photos.py` | ASSET | **LEGACY** | Resolved landmark photo URLs for early iterations. |
| `tools/resolve_remaining.py` | ASSET | **LEGACY** | Fallback resolver for missing landmark photo links. |
| `tools/build_city_architecture.py` | BUILD | **LEGACY** | Predecessor to unified dataset builder. |
| `tools/build_clean_v2.py` | BUILD | **LEGACY** | V2 release build script. |
| `tools/build_commercial_index.py` | BUILD | **LEGACY** | Prototype commercial build script. |
| `tools/build_commercial_index_template.py`| BUILD | **LEGACY** | Template builder prototype. |
| `tools/build_commercial_masterpiece.py` | BUILD | **LEGACY** | Masterpiece prototype build script. |
| `tools/build_full_game.py` | BUILD | **LEGACY** | Early single-file generator. |
| `tools/build_idioms.py` | BUILD | **LEGACY** | Extracted and normalized idioms dataset. |
| `tools/build_unified_data.py` | BUILD | **LEGACY** | Predecessor to `build_verified_dataset.py`. |
| `tools/build_v2_release.py` | BUILD | **LEGACY** | V2 release compiler. |
| `tools/compile_masterpiece_index.py` | BUILD | **LEGACY** | V3 masterpiece compiler. |
| `tools/compile_sozcuk_seferi_v1.py` | BUILD | **LEGACY** | V1 release compiler. |
| `tools/compile_v2.py` | BUILD | **LEGACY** | V2 compiler prototype. |
| `tools/compile_v2_safe.py` | BUILD | **LEGACY** | V2 safe compiler prototype. |
| `tools/compile_v3_masterpiece.py` | BUILD | **LEGACY** | V3 compiler prototype. |
| `tools/generate_100_levels.py` | DATA | **LEGACY** | Early procedural level generator. |
| `tools/generate_final_game.py` | BUILD | **LEGACY** | Early monolithic generator. |
| `tools/generate_verified_100_levels.py` | DATA | **LEGACY** | Generated `levels_100.json`. |
| `tools/make_index_html.py` | BUILD | **LEGACY** | Early HTML generator. |
| `tools/restructure.py` | REFACTOR | **LEGACY** | Initial directory restructuring script. |
| `tools/write_index.py` | BUILD | **LEGACY** | Raw index writer. |
| `tools/update_header.py` | REFACTOR | **LEGACY** | Early header patch script. |
| `tools/fix_all_elements.py` | FIX | **LEGACY** | DOM repair script for prototype. |
| `tools/fix_mobile_layout_perfect.py` | FIX | **LEGACY** | Mobile layout patch for early version. |
| `tools/fix_null_listeners.py` | FIX | **LEGACY** | Null listener patch for prototype. |
| `tools/find_overflow.py` | QA | **LEGACY** | Early viewport overflow scanner. |
| `tools/inspect_cities.py` | QA | **LEGACY** | City inspection script. |
| `tools/audit_game.py` | QA | **LEGACY** | Early monolithic runtime audit. |
| `tools/shots.py` | QA | **LEGACY** | Early screenshot utility. |
| `tools/take_final_screenshots.py` | QA | **LEGACY** | Early Chrome screenshot script. |
| `tools/take_v3_screenshots.py` | QA | **LEGACY** | V3 Chrome screenshot script. |
| `tools/capture_all_screens.py` | QA | **LEGACY** | Multi-screen capture script. |
| `tools/extract_prompt.py` | UTILITY | **UNUSED** | Extracted prompt logs for debugging. |
| `tests/validate_all_production_levels.py`| QA | **ACTIVE** | Rigorous verification of all 186 production levels (crossword geometry, solvability, TDK dictionary). |
| `tests/validate_strict_crossword.py` | QA | **ACTIVE** | Core geometry validator enforcing 90-degree crossings and distance >= 2 parallel rule. |
| `tests/browser_qa_cdp.js` | QA | **ACTIVE** | Automated headless Chrome DevTools Protocol suite: navigates, plays, clicks hints, solves, measures FPS & latency across 11 viewports. |
| `tests/test_save_manager.js` | QA | **ACTIVE** | Node.js unit test suite for `SaveManager.js` covering schema normalization, range clamping, corruption recovery, and daily streaks. |
| `tests/audit_dataset.py` | QA | **TEST** | Verifies level counts and distributions across 81 provinces. |
| `tests/check_cities_data.py` | QA | **TEST** | Checks showcase city levels. |
| `tests/check_levels_100_solvability.py` | QA | **TEST** | Verifies word solvability against wheel letters. |
| `tests/check_wheel_keys.py` | QA | **TEST** | Validates schema consistency between `wheel` and `letters` properties. |
| `tests/simulate_economy.py` | SIMULATION | **TEST** | Mathematical simulation of coin earn/spend balance across casual, normal, and skilled player personas. |
| `tests/test_all_landmarks.py` | QA | **TEST** | Audits landmark photo availability. |
| `tests/test_compile_data.py` | QA | **TEST** | Data compilation test. |
| `tests/test_images.py` | QA | **TEST** | Image URL HTTP status verification. |
| `tests/test_landmark_urls.py` | QA | **TEST** | Landmark URL link validation. |
| `tests/test_load.py` | QA | **TEST** | Load timing benchmark. |
| `tests/test_solvability.py` | QA | **TEST** | Solvability benchmark. |
| `tests/test_turkish_locale.py` | QA | **TEST** | Turkish locale and character case conversion verification. |
| `tests/validate_showcase_levels.py` | QA | **TEST** | Validates showcase level geometry. |
| `tests/verify_clean_runtime.py` | QA | **TEST** | Verifies runtime bundle size and clean syntax. |
| `tests/verify_data.py` | QA | **TEST** | JSON schema data validator. |
| `tests/verify_index.py` | QA | **TEST** | HTML structure checker. |
