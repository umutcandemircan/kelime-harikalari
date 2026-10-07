const fs = require('fs');
const vm = require('vm');

const store = {};
global.localStorage = {
    getItem: (k) => store[k] || null,
    setItem: (k, v) => { store[k] = v; },
    clear: () => { for (let k in store) delete store[k]; }
};
global.window = {};

vm.runInThisContext(fs.readFileSync('src/save/SaveManager.js', 'utf8'));

console.log('=== TESTING SAVEMANAGER CORRUPTION & BOUNDS ===');

SaveManager.init();
console.assert(SaveManager.data.coins === 250, 'Default coins should be 250');
console.assert(SaveManager.data.schemaVersion === 4, 'Default schemaVersion should be 4');
console.assert(SaveManager.data.hasSelectedStartCity === false, 'Default hasSelectedStartCity should be false');

localStorage.setItem('sozcukSeferi_v2_save', JSON.stringify({
    coins: 999999999999,
    currentCityIdx: -500,
    unlockedCityIdx: 999999,
    currentSubLevel: 999999,
    completedProvinces: ['invalid', -10, 85, 35, 35, 34],
    stars: { '0_0': 5, '0_1': -2, '0_2': 3, 'bad_val': 'string' },
    bonusChest: 100,
    daily: { streak: -10 }
}));

SaveManager.load();

console.assert(SaveManager.data.coins === 99999, 'Coins should be clamped to 99999');
console.assert(SaveManager.data.unlockedCityIdx === 80, 'Unlocked city clamped to 80');
console.assert(SaveManager.data.currentCityIdx === 0, 'Current city clamped to 0..80');
console.assert(SaveManager.data.currentSubLevel === 24, 'Current sublevel clamped to 24');
console.assert(JSON.stringify(SaveManager.data.completedProvinces) === JSON.stringify([35, 34]), 'Completed provinces sanitized');
console.assert(SaveManager.data.stars['0_2'] === 3, 'Valid star preserved');
console.assert(SaveManager.data.stars['0_0'] === undefined, 'Star > 3 rejected');
console.assert(SaveManager.data.stars['0_1'] === undefined, 'Star < 1 rejected');
console.assert(SaveManager.data.bonusChest === 5, 'Bonus chest clamped to 5');
console.assert(SaveManager.data.daily.streak === 0, 'Negative streak normalized to 0');

localStorage.clear();
SaveManager.init();

const today = '2026-10-05';
let dState = SaveManager.getDailyState(today);
console.assert(dState.canPlay === true, 'Can play first daily');
console.assert(dState.streak === 0, 'Initial streak is 0');

SaveManager.recordDailyCompletion(today, 50);
console.assert(SaveManager.data.daily.streak === 1, 'Streak should be 1 after day 1');
console.assert(SaveManager.data.coins === 300, 'Coins should be 250 + 50 = 300');

dState = SaveManager.getDailyState(today);
console.assert(dState.canPlay === false, 'Cannot replay on same day');
console.assert(dState.completedToday === true, 'Marked completed today');

const tomorrow = '2026-10-06';
dState = SaveManager.getDailyState(tomorrow);
console.assert(dState.canPlay === true, 'Can play tomorrow');
console.assert(dState.streak === 1, 'Consecutive streak preserved');

SaveManager.recordDailyCompletion(tomorrow, 50);
console.assert(SaveManager.data.daily.streak === 2, 'Streak advanced to 2');

const futureDay = '2026-10-09';
dState = SaveManager.getDailyState(futureDay);
console.assert(dState.canPlay === true, 'Can play after missed day');
console.assert(dState.streak === 0, 'Streak reset to 0 after missed day');

console.log('ALL SAVEMANAGER TESTS PASSED 100%!');
