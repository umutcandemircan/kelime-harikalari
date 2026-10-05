# -*- coding: utf-8 -*-
"""
Economy Simulation for Kelime Harikaları (Phase 4)
Calculates gold inflow and outflow over 50 levels across different player profiles.
Design goal: Ad-free players should be able to afford a hint approximately every 2 levels.
"""

def simulate_economy():
    INITIAL_COINS = 200
    LEVEL_WIN = 30
    BONUS_WORD_AVG_PER_LEVEL = 0.8
    BONUS_CHEST_THRESHOLD = 5
    BONUS_CHEST_REWARD = 35
    DAILY_FREE_HINT = 1 # 1 free hint equivalent to 50 coins daily
    
    HINT_COST = 50
    TARGET_COST = 90
    LIGHTNING_COST = 140

    print("=== EKONOMİ SİMÜLASYONU (50 Bölüm) ===")
    
    # Profile A: Reklamsız Normal Oyuncu (Her 2 bölümde 1 ampul ipucu kullanan)
    coins_a = INITIAL_COINS
    hints_used_a = 0
    bonus_accum_a = 0
    history_a = []
    
    for lvl in range(1, 51):
        # Kazanılan
        earned = LEVEL_WIN
        bonus_accum_a += BONUS_WORD_AVG_PER_LEVEL
        if bonus_accum_a >= BONUS_CHEST_THRESHOLD:
            earned += BONUS_CHEST_REWARD
            bonus_accum_a -= BONUS_CHEST_THRESHOLD
            
        coins_a += earned
        
        # Harcanan: Her 2 bölümde 1 ipucu
        if lvl % 2 == 0:
            if coins_a >= HINT_COST:
                coins_a -= HINT_COST
                hints_used_a += 1
                
        history_a.append(coins_a)
        
    print(f"Profil A (Reklamsız, Her 2 Bölümde 1 İpucu):")
    print(f"  Başlangıç: {INITIAL_COINS} Altın")
    print(f"  50 Bölüm Sonu Bakiye: {coins_a} Altın")
    print(f"  Kullanılan İpucu: {hints_used_a}")
    print(f"  Minimum Bakiye: {min(history_a)} Altın (Negatife hiç düşmedi)")
    print(f"  Ortalama bölüm başı net kazanç: {(coins_a - INITIAL_COINS) / 50:.1f} Altın/bölüm")
    print()

    # Profile B: Reklamsız Zorlanan Oyuncu (Her bölümde 1 ipucu kullanan)
    coins_b = INITIAL_COINS
    hints_used_b = 0
    bonus_accum_b = 0
    history_b = []
    
    for lvl in range(1, 51):
        earned = LEVEL_WIN
        bonus_accum_b += BONUS_WORD_AVG_PER_LEVEL
        if bonus_accum_b >= BONUS_CHEST_THRESHOLD:
            earned += BONUS_CHEST_REWARD
            bonus_accum_b -= BONUS_CHEST_THRESHOLD
            
        coins_b += earned
        
        # Her bölümde 1 ipucu isterse
        if coins_b >= HINT_COST:
            coins_b -= HINT_COST
            hints_used_b += 1
            
        history_b.append(coins_b)
        
    print(f"Profil B (Reklamsız, Her Bölümde 1 İpucu İhtiyacı):")
    print(f"  Başlangıç: {INITIAL_COINS} Altın")
    print(f"  50 Bölüm Sonu Bakiye: {coins_b} Altın")
    print(f"  Kullanılan İpucu: {hints_used_b}")
    print(f"  Minimum Bakiye: {min(history_b)} Altın")
    print()

    # Profile C: Reklam İzleyen Oyuncu (Bölüm sonu 2X)
    coins_c = INITIAL_COINS
    hints_used_c = 0
    bonus_accum_c = 0
    
    for lvl in range(1, 51):
        earned = LEVEL_WIN + 30 # 2X ödül: +30 ek
        bonus_accum_c += BONUS_WORD_AVG_PER_LEVEL
        if bonus_accum_c >= BONUS_CHEST_THRESHOLD:
            earned += BONUS_CHEST_REWARD
            bonus_accum_c -= BONUS_CHEST_THRESHOLD
        coins_c += earned
        
        if lvl % 2 == 0 and coins_c >= HINT_COST:
            coins_c -= HINT_COST
            hints_used_c += 1
            
    print(f"Profil C (2X Reklam İzleyen, Her 2 Bölümde 1 İpucu):")
    print(f"  50 Bölüm Sonu Bakiye: {coins_c} Altın")
    print(f"  Kullanılan İpucu: {hints_used_c}")
    print()

if __name__ == '__main__':
    simulate_economy()
