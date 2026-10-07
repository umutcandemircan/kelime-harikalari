import json
import os
import sys

from validate_words import validate_words
from validate_landmarks import validate_landmarks
from validate_puzzles import validate_puzzles

def validate_release():
    print("==================================================")
    print("   SÖZCÜK SEFERÎ V2 MASTER RELEASE QUALITY GATE   ")
    print("==================================================")

    # 1. Words check
    validate_words()
    print("-" * 50)

    # 2. Landmarks check
    validate_landmarks()
    print("-" * 50)

    # 3. Puzzles check
    validate_puzzles()
    print("-" * 50)

    # 4. Check index.html build size and existence
    if not os.path.exists('index.html'):
        print("FAILED: index.html not found!")
        sys.exit(1)
        
    size_mb = os.path.getsize('index.html') / (1024 * 1024)
    print(f"BUILD ASSET: index.html verified ({size_mb:.2f} MB)")

    print("==================================================")
    print("  ALL QUALITY GATES PASSED! READY FOR RELEASE!    ")
    print("==================================================")

if __name__ == '__main__':
    validate_release()
