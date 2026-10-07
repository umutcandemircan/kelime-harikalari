import json
import os
import sys

def validate_landmarks():
    print("=== QA AUDIT: LANDMARKS & ATTRIBUTION METADATA ===")
    
    cities_path = 'data/cities/tr_cities.json'
    landmarks_path = 'data/landmarks/tr_landmarks.json'

    with open(cities_path, 'r', encoding='utf-8') as f:
        cities = json.load(f)

    with open(landmarks_path, 'r', encoding='utf-8') as f:
        landmarks = json.load(f)

    errors = []

    # 1. 81 cities must have exactly 5 landmarks each
    landmarks_by_city = {}
    for lm in landmarks:
        cid = lm.get('cityId')
        landmarks_by_city.setdefault(cid, []).append(lm)

    if len(cities) != 81:
        errors.append(f"CITY_COUNT_ERROR: Expected 81 cities, found {len(cities)}")

    for c in cities:
        cid = c['id']
        city_lms = landmarks_by_city.get(cid, [])
        if len(city_lms) != 5:
            errors.append(f"LANDMARK_COUNT_ERROR: City {c['name']} ({cid}) has {len(city_lms)} landmarks (expected 5)")
        
        for lm in city_lms:
            if not lm.get('name'):
                errors.append(f"LANDMARK_NAME_EMPTY: {cid} landmark has no name")
            if not lm.get('image') or not lm['image'].startswith('https://'):
                errors.append(f"LANDMARK_IMAGE_INVALID: {lm.get('id')} has invalid image URL: {lm.get('image')}")
            if not lm.get('credit') or not lm['credit'].get('verified'):
                errors.append(f"LANDMARK_CREDIT_UNVERIFIED: {lm.get('id')} has unverified credit metadata")

    if errors:
        print(f"FAILED: Found {len(errors)} landmark errors:")
        for e in errors[:10]:
            print(f"  - {e}")
        sys.exit(1)

    print(f"SUCCESS: 81/81 cities verified with exactly 5 authentic landmarks each ({len(landmarks)} total)! All images verified.")

if __name__ == '__main__':
    validate_landmarks()
