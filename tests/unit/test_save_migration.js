const assert = require('assert');
const fs = require('fs');

// Mock localStorage
const localStorageStore = {};
global.localStorage = {
    getItem: (key) => localStorageStore[key] || null,
    setItem: (key, val) => { localStorageStore[key] = String(val); },
    removeItem: (key) => { delete localStorageStore[key]; },
    clear: () => { Object.keys(localStorageStore).forEach(k => delete localStorageStore[k]); }
};

const path = require('path');
const SaveManager = require(path.resolve('src/save/SaveManager.js'));

console.log("=== RUNNING SAVE MANAGER MIGRATION UNIT TESTS ===");

// Test 1: Defaults initialized properly
SaveManager.init();
assert.strictEqual(SaveManager.data.schemaVersion, 4);
assert.strictEqual(SaveManager.data.coins, 250);
assert.strictEqual(SaveManager.data.currentCountry, 'tr');
console.log("✓ Test 1 Passed: Default state matches schema v4.");

// Test 2: Legacy v1/v2 save migration
localStorage.clear();
const legacySave = {
    version: 3,
    coins: 720,
    hasSelectedStartCity: true,
    currentCityIdx: 34,
    currentSubLevel: 12,
    completedProvinces: [6, 34, 35],
    stars: { "34_0": 3, "34_1": 2 }
};
localStorage.setItem('sozcukSeferi_v1_save', JSON.stringify(legacySave));

SaveManager.init();
assert.strictEqual(SaveManager.data.schemaVersion, 4);
assert.strictEqual(SaveManager.data.coins, 720);
assert.strictEqual(SaveManager.data.currentCityIdx, 34);
assert.strictEqual(SaveManager.data.currentSubLevel, 12);
assert.deepStrictEqual(SaveManager.data.completedProvinces, [6, 34, 35]);
assert.strictEqual(SaveManager.data.stars["34_0"], 3);
console.log("✓ Test 2 Passed: Legacy save migrated cleanly without loss of coins or progress.");

// Test 3: Corrupt save recovery
localStorage.clear();
localStorage.setItem('sozcukSeferi_v2_save', '{ corrupt json string !!!');
SaveManager.init();
assert.strictEqual(SaveManager.data.schemaVersion, 4);
assert.strictEqual(SaveManager.data.coins, 250);
console.log("✓ Test 3 Passed: Corrupt save recovered gracefully to valid defaults.");

console.log("ALL SAVE MANAGER UNIT TESTS PASSED!");
