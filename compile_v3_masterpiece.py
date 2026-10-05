# -*- coding: utf-8 -*-
"""
V3 Masterpiece Compiler for Kelime Harikaları
Assembles the complete production-grade index.html with state machine,
interactive Turkey map, travel transition, postcard UX, and TDK dictionary.
"""
import json

with open('cities_data.json', 'r', encoding='utf-8') as f:
    cities_data = json.load(f)

with open('idioms.json', 'r', encoding='utf-8') as f:
    idioms_data = json.load(f)

with open('tdk_dict.json', 'r', encoding='utf-8') as f:
    tdk_dict = json.load(f)

with open('credits.json', 'r', encoding='utf-8') as f:
    credits_data = json.load(f)

# Flatten all city levels for linear gameplay and quick indexing
all_levels = []
for city in cities_data:
    for lvl in city['levels']:
        all_levels.append(lvl)

print(f"Total levels assembled: {len(all_levels)} across {len(cities_data)} cities.")

html_template = '''<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, viewport-fit=cover">
  <title>Kelime Harikaları - Türkiye Kültür Yolculuğu</title>
  <meta name="referrer" content="no-referrer">
  
  <meta name="description" content="Kelime Harikaları: Türk dili ve kültürel mirasından ilham alan modern, mobil öncelikli çapraz bulmaca ve harf çarkı oyunu.">
  <meta name="theme-color" content="#020617">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  
  <link rel="manifest" href="manifest.json">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800;900&family=Playfair+Display:ital,wght@1,700;1,900&display=swap" rel="stylesheet">

  <style>
    :root {
      --bg-dark: #020617;
      --card-bg: rgba(15, 23, 42, 0.88);
      --card-border: rgba(255, 255, 255, 0.16);
      --gold-primary: #fbbf24;
      --gold-glow: rgba(251, 191, 36, 0.5);
      --accent-blue: #38bdf8;
      --accent-purple: #c084fc;
      --font-main: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-serif: 'Playfair Display', Georgia, serif;
      --wheel-size: min(250px, 36vh);
      --node-size: min(48px, 6.8vh);
    }

    body.dyslexic-font {
      --font-main: 'OpenDyslexic', 'Comic Sans MS', sans-serif !important;
    }
    body.high-contrast {
      --card-bg: #000000 !important;
      --card-border: #ffffff !important;
    }

    @media (prefers-reduced-motion: reduce) {
      * {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
      }
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      user-select: none;
      -webkit-user-select: none;
      -webkit-tap-highlight-color: transparent;
    }

    html, body {
      width: 100%;
      height: 100%;
      height: 100dvh;
      overflow: hidden;
      font-family: var(--font-main);
      background: var(--bg-dark);
      color: #fff;
    }

    #bg-layer {
      position: fixed;
      inset: 0;
      width: 100vw;
      height: 100vh;
      height: 100dvh;
      background-size: cover;
      background-position: center center;
      background-repeat: no-repeat;
      filter: brightness(0.65) saturate(1.25);
      transition: background-image 0.7s cubic-bezier(0.4, 0, 0.2, 1);
      z-index: 0;
    }

    #bg-gradient {
      position: fixed;
      inset: 0;
      width: 100vw;
      height: 100vh;
      height: 100dvh;
      background: radial-gradient(circle at 50% 35%, rgba(15, 23, 42, 0.25) 0%, rgba(2, 6, 23, 0.88) 100%);
      z-index: 1;
      pointer-events: none;
    }

    #screen-flash {
      position: fixed;
      inset: 0;
      background: #fff;
      opacity: 0;
      pointer-events: none;
      z-index: 99;
      transition: opacity 0.08s ease-out;
    }

    #confetti-canvas {
      position: fixed;
      inset: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 80;
    }

    #targeting-banner {
      display: none;
      position: absolute;
      top: 54px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(14, 165, 233, 0.95);
      backdrop-filter: blur(10px);
      padding: 5px 14px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 800;
      color: #fff;
      box-shadow: 0 4px 16px rgba(14, 165, 233, 0.5);
      z-index: 30;
      animation: bounceBanner 0.5s infinite alternate;
    }
    body.targeting-mode #targeting-banner {
      display: block;
    }
    @keyframes bounceBanner {
      0% { transform: translate(-50%, 0); }
      100% { transform: translate(-50%, -3px); }
    }

    #app-container {
      position: relative;
      z-index: 2;
      width: 100%;
      max-width: 440px;
      height: 100%;
      height: 100dvh;
      margin: 0 auto;
      overflow: hidden;
    }

    /* Game Screen State Machine */
    .game-screen {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      opacity: 0;
      pointer-events: none;
      transform: scale(0.96);
      transition: opacity 0.28s ease, transform 0.28s cubic-bezier(0.34, 1.56, 0.64, 1);
      padding: max(8px, env(safe-area-inset-top)) 8px max(8px, env(safe-area-inset-bottom)) 8px;
      box-sizing: border-box;
    }
    .game-screen.active {
      opacity: 1;
      pointer-events: auto;
      transform: scale(1);
    }

    /* ---------------- UI Components & Pills ---------------- */
    .header-pill {
      display: flex;
      align-items: center;
      gap: 5px;
      background: var(--card-bg);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      padding: 4px 8px;
      border-radius: 999px;
      border: 1px solid var(--card-border);
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
      font-weight: 700;
      font-size: 11.5px;
    }
    .level-pill {
      flex: 0 0 auto;
      max-width: 110px;
    }
    .level-badge {
      display: flex;
      flex-direction: column;
      line-height: 1.1;
    }
    .level-badge .sub-title {
      font-size: 8.5px;
      color: #94a3b8;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .level-badge .main-title {
      font-size: 12px;
      color: #f8fafc;
      font-weight: 800;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 80px;
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 4px;
      flex-shrink: 0;
    }

    .btn-header {
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 3px;
      background: var(--card-bg);
      backdrop-filter: blur(12px);
      border: 1px solid var(--card-border);
      border-radius: 999px;
      padding: 4px 8px;
      color: #fff;
      font-size: 11px;
      font-weight: 800;
      height: 30px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.25);
      transition: transform 0.15s;
    }
    .btn-header:active {
      transform: scale(0.92);
    }
    .btn-header.daily-btn {
      background: linear-gradient(135deg, rgba(245, 158, 11, 0.35), rgba(217, 119, 6, 0.55));
      border-color: rgba(245, 158, 11, 0.7);
      color: #fef08a;
    }
    .btn-header.idiom-btn {
      background: linear-gradient(135deg, rgba(168, 85, 247, 0.35), rgba(126, 34, 206, 0.55));
      border-color: rgba(168, 85, 247, 0.7);
      color: #f3e8ff;
    }
    .coin-badge {
      color: #fef08a;
      text-shadow: 0 0 6px var(--gold-glow);
      font-weight: 800;
    }

    /* ---------------- SCREEN 1: MENU ---------------- */
    #menu-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 44px;
      width: 100%;
    }
    #menu-hero {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 10px 0;
      gap: 12px;
    }
    .menu-title-glow {
      font-size: 30px;
      font-weight: 900;
      letter-spacing: 1px;
      background: linear-gradient(135deg, #fff 20%, #fef08a 60%, #f59e0b 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      filter: drop-shadow(0 4px 16px rgba(245, 158, 11, 0.5));
      line-height: 1.1;
    }
    .menu-subtitle {
      font-size: 12.5px;
      font-weight: 800;
      color: #93c5fd;
      letter-spacing: 2px;
      text-transform: uppercase;
      margin-top: -4px;
    }

    .menu-status-card {
      width: 100%;
      max-width: 320px;
      background: linear-gradient(135deg, rgba(30, 41, 59, 0.85), rgba(15, 23, 42, 0.95));
      border: 1.5px solid rgba(255, 255, 255, 0.18);
      border-radius: 18px;
      padding: 12px 16px;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
      display: flex;
      align-items: center;
      gap: 12px;
      text-align: left;
    }
    .status-card-icon {
      font-size: 30px;
      filter: drop-shadow(0 0 10px rgba(245, 158, 11, 0.7));
    }
    .status-card-info {
      flex: 1;
    }
    .status-card-city {
      font-size: 15px;
      font-weight: 900;
      color: #f8fafc;
    }
    .status-card-landmark {
      font-size: 11.5px;
      color: #cbd5e1;
      font-weight: 600;
    }

    .menu-buttons-list {
      display: flex;
      flex-direction: column;
      gap: 9px;
      width: 100%;
      max-width: 320px;
    }
    .btn-menu-primary {
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      width: 100%;
      padding: 14px 20px;
      background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 60%, #d97706 100%);
      color: #0f172a;
      font-size: 17px;
      font-weight: 900;
      border: 2px solid #fef08a;
      border-radius: 999px;
      box-shadow: 0 8px 24px var(--gold-glow);
      transition: transform 0.15s, box-shadow 0.15s;
    }
    .btn-menu-primary:active {
      transform: scale(0.95);
    }
    .btn-menu-action {
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      width: 100%;
      padding: 11px 18px;
      background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9));
      color: #f8fafc;
      font-size: 13.5px;
      font-weight: 800;
      border: 1px solid rgba(255, 255, 255, 0.18);
      border-radius: 999px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
      transition: transform 0.15s;
    }
    .btn-menu-action:active {
      transform: scale(0.96);
    }

    #menu-footer {
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 36px;
      padding: 0 4px;
      font-size: 11px;
      color: #94a3b8;
    }
    .btn-text-link {
      background: none;
      border: none;
      color: #94a3b8;
      font-size: 11.5px;
      font-weight: 700;
      cursor: pointer;
      text-decoration: underline;
    }

    /* ---------------- SCREEN 2: MAP VIEW ---------------- */
    #map-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 44px;
      width: 100%;
    }
    #map-container {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      position: relative;
      width: 100%;
      padding: 4px;
      overflow: hidden;
    }
    #turkey-svg-map {
      width: 100%;
      max-height: 250px;
      filter: drop-shadow(0 8px 24px rgba(0, 0, 0, 0.5));
    }
    .city-node-circle {
      cursor: pointer;
      transition: transform 0.2s, filter 0.2s;
    }
    .city-node-circle:hover {
      transform: scale(1.2);
    }
    .city-node-pulse {
      animation: pulseNode 1.5s infinite;
    }
    @keyframes pulseNode {
      0% { r: 12; opacity: 0.9; }
      50% { r: 18; opacity: 0.3; }
      100% { r: 12; opacity: 0.9; }
    }

    /* City Drawer / Level Selector inside MAP */
    #city-drawer {
      width: 100%;
      background: linear-gradient(135deg, rgba(30, 41, 59, 0.92), rgba(15, 23, 42, 0.98));
      backdrop-filter: blur(14px);
      border: 1.5px solid rgba(255, 255, 255, 0.18);
      border-radius: 20px;
      padding: 12px 14px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
      margin-top: 6px;
    }
    .city-drawer-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 8px;
    }
    .city-drawer-title {
      font-size: 15px;
      font-weight: 900;
      color: #fef08a;
    }
    .city-drawer-plate {
      font-size: 11px;
      font-weight: 800;
      background: rgba(255, 255, 255, 0.1);
      padding: 2px 7px;
      border-radius: 6px;
      border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .city-drawer-levels {
      display: flex;
      flex-direction: column;
      gap: 5px;
      max-height: 180px;
      overflow-y: auto;
    }
    .drawer-level-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 10px;
      padding: 7px 10px;
      font-size: 12px;
      font-weight: 800;
    }
    .drawer-level-item.unlocked {
      border-color: rgba(251, 191, 36, 0.4);
    }
    .btn-drawer-play {
      cursor: pointer;
      background: linear-gradient(135deg, #fbbf24, #d97706);
      border: none;
      border-radius: 999px;
      padding: 4px 12px;
      color: #0f172a;
      font-weight: 900;
      font-size: 11px;
    }

    /* ---------------- SCREEN 3: GAMEPLAY ---------------- */
    #gameplay-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 44px;
      width: 100%;
    }
    #board-area {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 140px;
      position: relative;
      padding: 4px;
      overflow: hidden;
    }
    #crossword-grid {
      display: grid;
      gap: 5px;
      position: relative;
      margin: 0 auto;
      transition: transform 0.3s ease;
    }
    .crossword-cell {
      position: relative;
      width: 100%;
      height: 100%;
      perspective: 600px;
    }
    .crossword-cell.hidden {
      visibility: hidden;
      pointer-events: none;
    }
    .cell-inner {
      width: 100%;
      height: 100%;
      position: relative;
      transform-style: preserve-3d;
      transition: transform 0.45s cubic-bezier(0.34, 1.56, 0.64, 1);
      border-radius: 8px;
    }
    .crossword-cell.revealed .cell-inner {
      transform: rotateY(180deg);
    }
    .cell-front, .cell-back {
      position: absolute;
      inset: 0;
      backface-visibility: hidden;
      -webkit-backface-visibility: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 8px;
      font-weight: 900;
      box-shadow: 0 3px 8px rgba(0, 0, 0, 0.35);
    }
    .cell-front {
      background: rgba(255, 255, 255, 0.16);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      border: 1.5px solid rgba(255, 255, 255, 0.35);
      color: transparent;
      cursor: pointer;
      transition: border-color 0.2s, box-shadow 0.2s, transform 0.2s;
    }
    body.targeting-mode .cell-front {
      border: 2px solid #38bdf8 !important;
      box-shadow: 0 0 14px rgba(56, 189, 248, 0.8) !important;
      animation: pulseTarget 0.9s infinite alternate;
      cursor: crosshair;
    }
    @keyframes pulseTarget {
      0% { transform: scale(0.96); background: rgba(56, 189, 248, 0.25); }
      100% { transform: scale(1.04); background: rgba(56, 189, 248, 0.45); }
    }
    .cell-back {
      background: linear-gradient(135deg, #ffffff, #f1f5f9);
      border: 2px solid #fbbf24;
      color: #0f172a;
      transform: rotateY(180deg);
      font-size: 18px;
      box-shadow: 0 0 12px rgba(251, 191, 36, 0.45), inset 0 2px 4px rgba(255, 255, 255, 0.8);
      cursor: pointer;
    }
    .star-badge {
      position: absolute;
      top: -5px;
      right: -5px;
      font-size: 13px;
      z-index: 5;
      animation: floatStar 1.6s ease-in-out infinite alternate;
      filter: drop-shadow(0 0 6px rgba(245, 158, 11, 0.9));
    }
    @keyframes floatStar {
      0% { transform: translateY(0) scale(1); }
      100% { transform: translateY(-3px) scale(1.15); }
    }

    #bottom-section {
      display: flex;
      flex-direction: column;
      align-items: center;
      flex-shrink: 0;
    }
    #preview-container {
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 2px;
    }
    #word-preview {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-width: 65px;
      height: 30px;
      padding: 0 14px;
      border-radius: 999px;
      background: rgba(15, 23, 42, 0.88);
      backdrop-filter: blur(14px);
      border: 1.5px solid rgba(255, 255, 255, 0.2);
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4);
      font-size: 15px;
      font-weight: 900;
      letter-spacing: 2px;
      color: #f8fafc;
      opacity: 0;
      transform: scale(0.85);
      transition: opacity 0.18s, transform 0.18s, border-color 0.18s;
    }
    #word-preview.active {
      opacity: 1;
      transform: scale(1);
      border-color: #fbbf24;
      box-shadow: 0 0 18px var(--gold-glow);
    }

    #powerups-toolbar {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 100%;
      max-width: 310px;
      margin: 0 auto 4px auto;
      gap: 7px;
    }
    .btn-powerup, .bonus-chest-btn {
      flex: 0 0 45px;
      width: 45px;
      height: 45px;
      border-radius: 12px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      color: #fff;
      border: 1.5px solid rgba(255, 255, 255, 0.2);
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
      padding: 1px;
      box-sizing: border-box;
      transition: transform 0.15s, border-color 0.2s;
    }
    .btn-powerup:active, .bonus-chest-btn:active {
      transform: scale(0.92);
    }
    .btn-powerup {
      background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.96));
    }
    .bonus-chest-btn {
      background: linear-gradient(135deg, rgba(168, 85, 247, 0.4), rgba(126, 34, 206, 0.7));
      border-color: rgba(216, 180, 254, 0.5) !important;
    }
    .btn-powerup .icon, .bonus-chest-btn .icon {
      font-size: 16px;
      line-height: 1;
    }
    .btn-powerup .cost, .bonus-chest-btn .counter {
      font-size: 8.5px;
      font-weight: 800;
      color: #fef08a;
      margin-top: 1px;
      display: flex;
      align-items: center;
      gap: 1px;
    }
    .bonus-chest-btn .counter {
      color: #f3e8ff;
    }
    .btn-powerup.active-tool {
      border-color: #38bdf8 !important;
      box-shadow: 0 0 14px rgba(56, 189, 248, 0.8) !important;
      background: rgba(14, 165, 233, 0.35) !important;
    }

    #wheel-wrapper {
      position: relative;
      width: var(--wheel-size);
      height: var(--wheel-size);
      margin: 0 auto 4px auto;
      display: flex;
      align-items: center;
      justify-content: center;
      touch-action: none;
    }
    #wheel-canvas-container {
      position: absolute;
      inset: 0;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.85) 100%);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 2px solid rgba(255, 255, 255, 0.18);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5), inset 0 0 16px rgba(255, 255, 255, 0.06);
      pointer-events: none;
    }
    #wheel-svg {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 10;
    }
    #connection-line {
      fill: none;
      stroke: #fbbf24;
      stroke-width: 10;
      stroke-linecap: round;
      stroke-linejoin: round;
      filter: drop-shadow(0 0 8px rgba(251, 191, 36, 0.9));
    }
    .wheel-node {
      position: absolute;
      width: var(--node-size);
      height: var(--node-size);
      border-radius: 50%;
      background: linear-gradient(135deg, #ffffff, #e2e8f0);
      color: #0f172a;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 21px;
      font-weight: 900;
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3), inset 0 2px 4px rgba(255, 255, 255, 0.9);
      border: 2px solid rgba(255, 255, 255, 0.8);
      z-index: 20;
      transition: transform 0.18s cubic-bezier(0.34, 1.56, 0.64, 1), background 0.18s, box-shadow 0.18s;
      transform: translate(-50%, -50%);
    }
    .wheel-node.selected {
      background: linear-gradient(135deg, #fbbf24, #f59e0b);
      color: #ffffff;
      transform: translate(-50%, -50%) scale(1.15);
      box-shadow: 0 0 18px rgba(245, 158, 11, 0.9), inset 0 2px 4px rgba(255, 255, 255, 0.5);
      border-color: #fef08a;
    }

    /* ---------------- MODALS & POSTCARD UX ---------------- */
    .modal-overlay {
      position: fixed;
      inset: 0;
      background: rgba(2, 6, 23, 0.85);
      backdrop-filter: blur(8px);
      z-index: 100;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 14px;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.25s ease;
    }
    .modal-overlay.active {
      opacity: 1;
      pointer-events: auto;
    }
    .modal-card {
      width: 100%;
      max-width: 390px;
      max-height: 90vh;
      overflow-y: auto;
      background: linear-gradient(135deg, rgba(30, 41, 59, 0.96), rgba(15, 23, 42, 0.98));
      border: 1.5px solid rgba(255, 255, 255, 0.18);
      border-radius: 22px;
      padding: 20px;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6);
      text-align: center;
      transform: scale(0.92);
      transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .modal-overlay.active .modal-card {
      transform: scale(1);
    }

    /* Postcard UX (Tilt effect + Wax seal) */
    .postcard-container {
      background: #fdfbf7;
      color: #1e293b;
      border-radius: 16px;
      padding: 14px;
      box-shadow: 0 16px 36px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(0,0,0,0.08);
      transform: rotate(-2deg);
      transition: transform 0.3s ease;
      position: relative;
      margin-bottom: 14px;
      text-align: left;
    }
    .postcard-photo-wrap {
      position: relative;
      width: 100%;
      height: 190px;
      border-radius: 10px;
      overflow: hidden;
      margin-bottom: 10px;
      border: 3px solid #fff;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .postcard-photo {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
    .wax-seal {
      position: absolute;
      top: 8px;
      right: 8px;
      background: linear-gradient(135deg, #dc2626, #991b1b);
      color: #fef08a;
      font-size: 9.5px;
      font-weight: 900;
      padding: 5px 9px;
      border-radius: 999px;
      box-shadow: 0 4px 12px rgba(153, 27, 27, 0.6);
      border: 1.5px solid #fecaca;
      text-transform: uppercase;
      letter-spacing: 0.6px;
      display: flex;
      align-items: center;
      gap: 3px;
    }
    .postcard-title {
      font-family: var(--font-serif);
      font-size: 20px;
      font-weight: 900;
      color: #0f172a;
      line-height: 1.2;
      margin-bottom: 4px;
    }
    .postcard-city {
      font-size: 11px;
      font-weight: 800;
      color: #b45309;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      margin-bottom: 6px;
    }
    .postcard-text {
      font-size: 12.5px;
      line-height: 1.5;
      color: #334155;
    }
    .postcard-trivia {
      font-size: 12px;
      line-height: 1.45;
      color: #92400e;
      font-weight: 700;
      background: rgba(254, 243, 199, 0.6);
      padding: 6px 10px;
      border-radius: 8px;
      margin-top: 6px;
      border-left: 3px solid #f59e0b;
    }

    /* Buttons */
    .btn-gold {
      cursor: pointer;
      width: 100%;
      padding: 13px 20px;
      border-radius: 999px;
      border: none;
      background: linear-gradient(135deg, #fbbf24, #f59e0b);
      color: #0f172a;
      font-weight: 900;
      font-size: 14.5px;
      box-shadow: 0 4px 16px var(--gold-glow);
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: transform 0.15s;
    }
    .btn-gold:active {
      transform: scale(0.96);
    }
    .btn-secondary {
      cursor: pointer;
      width: 100%;
      padding: 11px 18px;
      border-radius: 999px;
      border: 1px solid rgba(255, 255, 255, 0.2);
      background: rgba(30, 41, 59, 0.65);
      color: #cbd5e1;
      font-weight: 800;
      font-size: 13px;
      margin-top: 8px;
      transition: transform 0.15s;
    }
    .btn-secondary:active {
      transform: scale(0.96);
    }

    /* Travel Modal Flight Animation */
    #travel-map-canvas {
      width: 100%;
      height: 220px;
      margin-bottom: 12px;
    }

    /* Toast Notification */
    #toast-notification {
      position: fixed;
      top: 60px;
      left: 50%;
      transform: translateX(-50%) translateY(-20px);
      background: rgba(15, 23, 42, 0.95);
      backdrop-filter: blur(12px);
      border: 1.5px solid #fbbf24;
      color: #fef08a;
      padding: 8px 18px;
      border-radius: 999px;
      font-size: 13px;
      font-weight: 800;
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5), 0 0 15px var(--gold-glow);
      z-index: 120;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.25s, transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    #toast-notification.active {
      opacity: 1;
      transform: translateX(-50%) translateY(0);
    }

    /* Spark Projectile */
    .spark-projectile {
      position: fixed;
      width: 14px;
      height: 14px;
      border-radius: 50%;
      background: radial-gradient(circle, #fff, #fbbf24);
      box-shadow: 0 0 16px #fbbf24, 0 0 24px #f59e0b;
      z-index: 60;
      pointer-events: none;
      transition: transform 0.42s cubic-bezier(0.25, 1, 0.5, 1), opacity 0.42s;
    }
  </style>
</head>
<body>

  <!-- Fullscreen Immersive Background -->
  <div id="bg-layer"></div>
  <div id="bg-gradient"></div>
  <div id="screen-flash"></div>
  <canvas id="confetti-canvas"></canvas>
  <div id="targeting-banner">🎯 Açmak istediğin kutucuğa dokun!</div>
  <div id="toast-notification">Bildirim</div>

  <div id="app-container">

    <!-- ==================== SCREEN 1: MENU ==================== -->
    <section id="screen-menu" class="game-screen active">
      <header id="menu-header">
        <div class="header-pill">
          <span>🇹🇷</span><span>Kelime Harikaları</span>
        </div>
        <div class="header-actions">
          <button class="btn-header" id="btn-menu-sound" aria-label="Ses">
            <span id="menu-sound-icon">🔊</span>
          </button>
          <button class="btn-header" id="btn-menu-settings" aria-label="Ayarlar">
            <span>⚙️</span>
          </button>
          <div class="header-pill coin-badge">
            <span>🪙</span><span class="coins-val">200</span>
          </div>
        </div>
      </header>

      <main id="menu-hero">
        <div>
          <h1 class="menu-title-glow">KELİME<br>HARİKALARI</h1>
          <div class="menu-subtitle">Türkiye Kültür Yolculuğu</div>
        </div>

        <div class="menu-status-card">
          <div class="status-card-icon">🏛️</div>
          <div class="status-card-info">
            <div class="status-card-city" id="menu-current-city">İzmir (35)</div>
            <div class="status-card-landmark" id="menu-current-landmark">Bölüm 1: Efes Kütüphanesi</div>
          </div>
        </div>

        <div class="menu-buttons-list">
          <button class="btn-menu-primary" id="btn-menu-play">
            <span>▶</span><span>OYUNA BAŞLA</span>
          </button>
          <button class="btn-menu-action" id="btn-menu-map">
            <span>🗺️</span><span>Yolculuk Haritası</span>
          </button>
          <button class="btn-menu-action" id="btn-menu-daily">
            <span>📅</span><span>Günlük Bulmaca</span>
          </button>
          <button class="btn-menu-action" id="btn-menu-idioms">
            <span>📜</span><span>Atasözü & Deyim Modu</span>
          </button>
        </div>
      </main>

      <footer id="menu-footer">
        <button class="btn-text-link" id="btn-menu-about">🏛️ Kültürel Kaynaklar & Lisanslar</button>
        <span>v2.5.0</span>
      </footer>
    </section>

    <!-- ==================== SCREEN 2: MAP VIEW ==================== -->
    <section id="screen-map" class="game-screen">
      <header id="map-header">
        <button class="btn-header" id="btn-map-back">
          <span>⬅️</span><span>Menü</span>
        </button>
        <div class="header-pill">
          <span>🗺️</span><span>Yolculuk Haritası</span>
        </div>
        <div class="header-pill coin-badge">
          <span>🪙</span><span class="coins-val">200</span>
        </div>
      </header>

      <div id="map-container">
        <!-- Interactive Stylized Turkey Map SVG -->
        <svg id="turkey-svg-map" viewBox="0 0 800 420">
          <defs>
            <linearGradient id="mapBgGrad" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stop-color="#1e293b" stop-opacity="0.8"/>
              <stop offset="100%" stop-color="#0f172a" stop-opacity="0.95"/>
            </linearGradient>
            <filter id="glowFilter" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="4" result="blur"/>
              <feComposite in="SourceGraphic" in2="blur" operator="over"/>
            </filter>
          </defs>

          <!-- Stylized Turkey Outline Boundary -->
          <path d="M 60,180 Q 120,130 180,95 Q 260,85 360,95 Q 480,90 600,100 Q 720,105 760,130 Q 750,210 700,240 Q 640,290 560,295 Q 460,305 340,300 Q 220,280 150,265 Q 90,260 65,220 Z" 
                fill="url(#mapBgGrad)" stroke="rgba(255, 255, 255, 0.25)" stroke-width="2.5" />

          <!-- Connecting Travel Flight / Road Routes -->
          <g id="map-routes-layer"></g>

          <!-- City Markers Layer -->
          <g id="map-cities-layer"></g>
        </svg>

        <!-- City Level Drawer / Detail Card -->
        <div id="city-drawer">
          <div class="city-drawer-header">
            <div>
              <div class="city-drawer-title" id="drawer-city-name">İzmir</div>
              <div style="font-size: 11px; color: #94a3b8;" id="drawer-city-desc">Ege'nin incisi kadim şehir</div>
            </div>
            <span class="city-drawer-plate" id="drawer-city-plate">Plaka 35</span>
          </div>

          <div class="city-drawer-levels" id="drawer-levels-list">
            <!-- Dynamically populated level items -->
          </div>
        </div>
      </div>
    </section>

    <!-- ==================== SCREEN 3: GAMEPLAY ==================== -->
    <section id="screen-gameplay" class="game-screen">
      <header id="gameplay-header">
        <button class="btn-header" id="btn-gameplay-back" title="Haritaya Dön">
          <span>🗺️</span><span>Harita</span>
        </button>

        <div class="header-pill level-pill">
          <div class="level-badge">
            <span class="sub-title" id="gameplay-region-text">İZMİR</span>
            <span class="main-title" id="gameplay-level-title-text">Bölüm 1</span>
          </div>
        </div>

        <div class="header-actions">
          <button class="btn-header daily-btn" id="btn-open-daily" title="Günlük Bulmaca">
            <span>📅</span><span id="streak-indicator">🔥 1</span>
          </button>
          <button class="btn-header" id="btn-gameplay-sound" title="Ses">
            <span id="gameplay-sound-icon">🔊</span>
          </button>
          <button class="btn-header" id="btn-open-settings" title="Ayarlar">
            <span>⚙️</span>
          </button>
          <div class="header-pill coin-badge" title="Altın Bakiyesi">
            <span>🪙</span><span class="coins-val">200</span>
          </div>
        </div>
      </header>

      <!-- Crossword Board Area -->
      <main id="board-area">
        <div id="crossword-grid" role="grid" aria-label="Çapraz Bulmaca Izgarası"></div>
      </main>

      <!-- Bottom Controls & Wheel -->
      <section id="bottom-section">
        <div id="preview-container">
          <div id="word-preview" aria-live="polite">KELİME</div>
        </div>

        <!-- Powerups Toolbar -->
        <div id="powerups-toolbar">
          <button class="btn-powerup" id="btn-shuffle" title="Harfleri Karıştır" aria-label="Karıştır (Ücretsiz)">
            <span class="icon">🔀</span>
            <span class="cost">Ücretsiz</span>
          </button>

          <button class="btn-powerup" id="btn-hint-bulb" title="Rastgele 1 Harf Aç" aria-label="Ampul: 50 Altın">
            <span class="icon">💡</span>
            <span class="cost">🪙 50</span>
          </button>

          <button class="btn-powerup" id="btn-hint-target" title="Hedef Harfi Seçip Aç" aria-label="Hedefçi: 100 Altın">
            <span class="icon">🎯</span>
            <span class="cost">🪙 100</span>
          </button>

          <button class="btn-powerup" id="btn-hint-lightning" title="3 Harf Patlat" aria-label="Şimşek: 150 Altın">
            <span class="icon">⚡</span>
            <span class="cost">🪙 150</span>
          </button>

          <button class="bonus-chest-btn" id="btn-bonus-chest" title="Kelime Sandığı" aria-label="Bonus Kelime Sandığı">
            <span class="icon">🎁</span>
            <span class="counter" id="bonus-counter">0/5</span>
          </button>
        </div>

        <!-- Letter Wheel -->
        <div id="wheel-wrapper" role="region" aria-label="Harf Çarkı">
          <div id="wheel-canvas-container"></div>
          <svg id="wheel-svg">
            <polyline id="connection-line" points=""></polyline>
          </svg>
          <div id="wheel-nodes-container"></div>
        </div>
      </section>
    </section>

  </div>

  <!-- ==================== MODALS ==================== -->

  <!-- 1. Digital Postcard UX (Tilt effect + Wax seal) -->
  <div class="modal-overlay" id="modal-postcard" role="dialog" aria-modal="true">
    <div class="modal-card">
      <div class="postcard-container">
        <div class="postcard-photo-wrap">
          <img class="postcard-photo" id="postcard-img" src="" alt="Tarihi Eser">
          <div class="wax-seal">🔴 KOLEKSİYONA EKLENDİ</div>
        </div>
        <div class="postcard-city" id="postcard-city-badge">İZMİR • 35</div>
        <h2 class="postcard-title" id="postcard-title">Celsus Kütüphanesi</h2>
        <p class="postcard-text" id="postcard-summary">Özet...</p>
        <div class="postcard-trivia" id="postcard-trivia">💡 Biliyor muydunuz? ...</div>
      </div>

      <div style="font-size: 26px; margin-bottom: 10px;" id="postcard-stars">⭐⭐⭐</div>

      <button class="btn-gold" id="btn-postcard-2x" style="margin-bottom: 8px;">
        <span>✨ 2 Katını Kazan (+50 🪙 Reklam)</span>
      </button>
      <button class="btn-secondary" id="btn-postcard-continue">
        <span>Normal Devam Et (+25 🪙)</span>
      </button>
    </div>
  </div>

  <!-- 2. Inter-City Travel Transition Modal -->
  <div class="modal-overlay" id="modal-travel" role="dialog" aria-modal="true">
    <div class="modal-card" style="max-width: 420px; padding: 22px;">
      <div style="font-size: 32px; margin-bottom: 6px;">✈️</div>
      <h2 style="font-size: 22px; font-weight: 900; margin-bottom: 4px; color: #fef08a;" id="travel-title">YENİ ŞEHRE SEYAHAT!</h2>
      <p style="color: #cbd5e1; font-size: 13px; margin-bottom: 14px;" id="travel-subtitle">İzmir tamamlandı, sıradaki durak Nevşehir!</p>

      <!-- Mini animated SVG travel route -->
      <svg id="travel-map-canvas" viewBox="0 0 400 200">
        <path d="M 40,90 Q 200,30 360,110" fill="none" stroke="#fbbf24" stroke-width="3" stroke-dasharray="8,6" />
        <circle id="travel-start-circle" cx="40" cy="90" r="8" fill="#38bdf8" />
        <circle id="travel-end-circle" cx="360" cy="110" r="10" fill="#22c55e" />
        <text x="40" y="125" fill="#f8fafc" font-size="12" font-weight="800" text-anchor="middle" id="travel-city-from">İzmir</text>
        <text x="360" y="145" fill="#fef08a" font-size="13" font-weight="900" text-anchor="middle" id="travel-city-to">Nevşehir</text>
        <!-- Gliding airplane icon -->
        <text id="travel-plane-icon" x="40" y="90" font-size="22" text-anchor="middle" dominant-baseline="central">✈️</text>
      </svg>

      <div style="background: rgba(34, 197, 94, 0.15); border: 1px solid rgba(34, 197, 94, 0.5); padding: 10px; border-radius: 12px; margin-bottom: 14px; font-weight: 800; color: #86efac; font-size: 13.5px;">
        🎉 Şehir Keşif Bonusu: +50 Altın!
      </div>

      <button class="btn-gold" id="btn-travel-continue">
        <span>Keşfe Başla ➔</span>
      </button>
    </div>
  </div>

  <!-- 3. TDK Word Meaning Modal -->
  <div class="modal-overlay" id="modal-meaning" role="dialog" aria-modal="true">
    <div class="modal-card" style="max-width: 340px; padding: 20px;">
      <div style="font-size: 32px; margin-bottom: 4px;">📖</div>
      <h2 id="meaning-word-title" style="font-size: 22px; font-weight: 900; margin-bottom: 2px; color: #fef08a; letter-spacing: 1px;">KELİME</h2>
      <span id="meaning-word-type" style="font-size: 11px; font-weight: 800; color: #38bdf8; text-transform: uppercase; letter-spacing: 0.6px;">TDK GÜNCEL SÖZLÜK</span>
      <div id="meaning-word-desc" style="font-size: 13.5px; line-height: 1.5; color: #e2e8f0; margin: 14px 0; text-align: left; background: rgba(15, 23, 42, 0.7); padding: 14px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.12);">
        Kelime açıklaması...
      </div>
      <button class="btn-secondary" id="btn-close-meaning" style="margin-top: 6px;">Kapat</button>
    </div>
  </div>

  <!-- 4. Daily Calendar Modal -->
  <div class="modal-overlay" id="modal-calendar" role="dialog" aria-modal="true">
    <div class="modal-card">
      <div style="font-size: 30px; margin-bottom: 6px;">📅</div>
      <h2 style="font-size: 22px; font-weight: 900; margin-bottom: 2px;">Günlük Bulmaca</h2>
      <p style="color: #94a3b8; font-size: 12.5px;" id="calendar-streak-text">🔥 1 Günlük Seri</p>

      <div class="calendar-grid" id="calendar-grid-container" style="display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px; margin: 12px 0;"></div>

      <button class="btn-gold" id="btn-play-daily" style="margin-bottom: 8px;">
        <span>Günün Bulmacasını Oyna (3 ⭐)</span>
      </button>
      <button class="btn-secondary" id="btn-share-daily" style="margin-bottom: 8px; display: none;">
        <span>📋 Sonucu Paylaş</span>
      </button>
      <button class="btn-secondary" id="btn-close-calendar">Kapat</button>
    </div>
  </div>

  <!-- 5. Idioms Challenge Modal -->
  <div class="modal-overlay" id="modal-idioms" role="dialog" aria-modal="true">
    <div class="modal-card">
      <div style="font-size: 32px; margin-bottom: 6px;">📜</div>
      <h2 style="font-size: 22px; font-weight: 900; margin-bottom: 2px; color: #c084fc;">Atasözü & Deyim Modu</h2>
      <p style="color: #cbd5e1; font-size: 12.5px; margin-bottom: 12px;">Türkçemizin zengin atasözlerindeki eksik kelimeleri tamamlayın.</p>

      <div style="background: rgba(168, 85, 247, 0.15); border: 1px solid rgba(168, 85, 247, 0.4); padding: 14px; border-radius: 14px; margin-bottom: 14px;">
        <div id="idiom-proverb-text" style="font-size: 16px; font-weight: 900; color: #f3e8ff; margin-bottom: 6px;">"Damlaya damlaya ___ olur."</div>
        <div id="idiom-meaning-text" style="font-size: 12px; color: #d8b4fe;">Anlamı: Küçük şeyler birike birike büyük varlık oluşturur.</div>
      </div>

      <button class="btn-gold" id="btn-play-idiom" style="margin-bottom: 8px;">
        <span>Kelimeyi Çarkta Bul ➔</span>
      </button>
      <button class="btn-secondary" id="btn-close-idioms">Kapat</button>
    </div>
  </div>

  <!-- 6. Settings Modal -->
  <div class="modal-overlay" id="modal-settings" role="dialog" aria-modal="true">
    <div class="modal-card">
      <div style="font-size: 28px; margin-bottom: 6px;">⚙️</div>
      <h2 style="font-size: 20px; font-weight: 900; margin-bottom: 12px;">Oyun Ayarları</h2>

      <div style="display: flex; flex-direction: column; gap: 10px; margin-bottom: 14px;">
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
          <span style="font-weight: 700; font-size: 13.5px;">🔊 Ses Efektleri</span>
          <input type="checkbox" id="toggle-sound" checked style="width: 20px; height: 20px; accent-color: #fbbf24;">
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
          <span style="font-weight: 700; font-size: 13.5px;">📳 Titreşim (Haptik)</span>
          <input type="checkbox" id="toggle-vibrate" checked style="width: 20px; height: 20px; accent-color: #fbbf24;">
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
          <span style="font-weight: 700; font-size: 13.5px;">📖 OpenDyslexic Yazı Tipi</span>
          <input type="checkbox" id="toggle-dyslexic" style="width: 20px; height: 20px; accent-color: #fbbf24;">
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 0;">
          <span style="font-weight: 700; font-size: 13.5px;">👁️ Yüksek Karşıtlık</span>
          <input type="checkbox" id="toggle-contrast" style="width: 20px; height: 20px; accent-color: #fbbf24;">
        </div>
      </div>

      <button class="btn-secondary" id="btn-close-settings">Kapat</button>
    </div>
  </div>

  <!-- 7. About & Cultural Credits Modal -->
  <div class="modal-overlay" id="modal-about" role="dialog" aria-modal="true">
    <div class="modal-card">
      <div style="font-size: 28px; margin-bottom: 6px;">🏛️</div>
      <h2 style="font-size: 20px; font-weight: 900; margin-bottom: 4px;">Kelime Harikaları</h2>
      <p style="font-size: 12px; color: #94a3b8; margin-bottom: 12px;">Türkiye Kültür Mirası & Kelime Oyunu</p>

      <div style="font-size: 12px; line-height: 1.5; color: #cbd5e1; text-align: left; background: rgba(15,23,42,0.6); padding: 12px; border-radius: 12px; margin-bottom: 14px;">
        <p style="margin-bottom: 8px;"><strong>Sözlük Kaynağı:</strong> Türk Dil Kurumu (TDK) Güncel Türkçe Sözlük standartları referans alınmıştır.</p>
        <p style="margin-bottom: 8px;"><strong>Görseller:</strong> Tüm tarihi ve doğal mekan fotoğrafları telifsiz ve yüksek çözünürlüklü Unsplash içerik sağlayıcısından optimize edilerek derlenmiştir.</p>
        <p><strong>Gizlilik:</strong> Oyunumuzda hiçbir kişisel veri toplanmaz, tüm kayıtlar cihazınızın kendi yerel belleğinde saklanır.</p>
      </div>

      <button class="btn-secondary" id="btn-close-about">Kapat</button>
    </div>
  </div>

  <!-- 8. Not Enough Coins Modal -->
  <div class="modal-overlay" id="modal-no-coins" role="dialog" aria-modal="true">
    <div class="modal-card">
      <div style="font-size: 32px; margin-bottom: 6px;">🪙</div>
      <h2 style="font-size: 20px; font-weight: 900; margin-bottom: 6px;">Yetersiz Altın</h2>
      <p style="color: #94a3b8; font-size: 13px; margin-bottom: 14px;">Bu ipucu için yeterli altınınız bulunmuyor.</p>

      <button class="btn-gold" id="btn-watch-ad-coins" style="margin-bottom: 8px;">
        <span>🎬 Reklam İzle (+100 🪙 Kazan)</span>
      </button>
      <button class="btn-secondary" id="btn-close-no-coins">Vazgeç</button>
    </div>
  </div>

  <!-- ==================== SCRIPT ENGINE ==================== -->
  <script>
  // Injected Comprehensive Data Packages
  const CITIES_DATA = ''' + json.dumps(cities_data, ensure_ascii=False) + ''';
  const ALL_LEVELS = ''' + json.dumps(all_levels, ensure_ascii=False) + ''';
  const IDIOMS_DATA = ''' + json.dumps(idioms_data, ensure_ascii=False) + ''';
  const TDK_DICTIONARY = ''' + json.dumps(tdk_dict, ensure_ascii=False) + ''';
  const CREDITS_DATA = ''' + json.dumps(credits_data, ensure_ascii=False) + ''';

  /* ==========================================================================
     1. STORAGE SERVICE (Fail-safe, Versioned, Migration Support)
     ========================================================================== */
  class StorageService {
    constructor() {
      this.prefix = 'kh_v2_';
      this.initMigrations();
    }
    initMigrations() {
      // Clean migration
      ['coins', 'level_idx', 'stars', 'streak'].forEach(k => {
        const legacyVal = localStorage.getItem('kh_' + k);
        if (legacyVal && !localStorage.getItem(this.prefix + k)) {
          localStorage.setItem(this.prefix + k, legacyVal);
        }
      });
    }
    get(key, defaultValue) {
      try {
        const val = localStorage.getItem(this.prefix + key);
        return val !== null ? JSON.parse(val) : defaultValue;
      } catch (e) {
        return defaultValue;
      }
    }
    set(key, value) {
      try {
        localStorage.setItem(this.prefix + key, JSON.stringify(value));
      } catch (e) {}
    }
  }

  /* ==========================================================================
     2. PROCEDURAL SOUND DESIGN (Web Audio API)
     ========================================================================== */
  class SoundManager {
    constructor() {
      this.ctx = null;
      this.muted = false;
    }
    init() {
      if (!this.ctx) {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (AudioCtx) this.ctx = new AudioCtx();
      }
      if (this.ctx && this.ctx.state === 'suspended') {
        this.ctx.resume();
      }
    }
    // Pentatonic scale for dragging letters (C4, D4, E4, G4, A4, C5, D5, E5)
    playLetterNote(index) {
      if (this.muted) return;
      this.init();
      if (!this.ctx) return;
      const freqs = [261.63, 293.66, 329.63, 392.00, 440.00, 523.25, 587.33, 659.25];
      const freq = freqs[Math.min(index, freqs.length - 1)];

      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
      gain.gain.setValueAtTime(0.18, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, this.ctx.currentTime + 0.18);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + 0.18);
    }
    // Gentle chord for successful word unlock
    playWordSuccess() {
      if (this.muted) return;
      this.init();
      if (!this.ctx) return;
      const notes = [523.25, 659.25, 783.99];
      notes.forEach((freq, idx) => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sine';
        const t = this.ctx.currentTime + idx * 0.05;
        osc.frequency.setValueAtTime(freq, t);
        gain.gain.setValueAtTime(0.15, t);
        gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.3);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(t);
        osc.stop(t + 0.3);
      });
    }
    // Soft acoustic chime for regular level completion
    playLevelChime() {
      if (this.muted) return;
      this.init();
      if (!this.ctx) return;
      const notes = [523.25, 659.25, 783.99];
      notes.forEach((freq, idx) => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sine';
        const t = this.ctx.currentTime + idx * 0.08;
        osc.frequency.setValueAtTime(freq, t);
        gain.gain.setValueAtTime(0.12, t);
        gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.35);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(t);
        osc.stop(t + 0.35);
      });
    }
    // Milestone fanfare for city completion / postcard unlock
    playMilestoneFanfare() {
      if (this.muted) return;
      this.init();
      if (!this.ctx) return;
      const motif = [
        { f: 523.25, t: 0.0, d: 0.2 },
        { f: 659.25, t: 0.12, d: 0.22 },
        { f: 783.99, t: 0.24, d: 0.26 },
        { f: 1046.50, t: 0.40, d: 0.6 }
      ];
      motif.forEach(m => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'triangle';
        const startTime = this.ctx.currentTime + m.t;
        osc.frequency.setValueAtTime(m.f, startTime);
        gain.gain.setValueAtTime(0.18, startTime);
        gain.gain.exponentialRampToValueAtTime(0.001, startTime + m.d);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(startTime);
        osc.stop(startTime + m.d);
      });
    }
    // Travel whoosh sound effect
    playTravelWhoosh() {
      if (this.muted) return;
      this.init();
      if (!this.ctx) return;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(220, this.ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(880, this.ctx.currentTime + 1.2);
      gain.gain.setValueAtTime(0.15, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 1.2);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + 1.2);
    }
    playErrorBuzz() {
      if (this.muted) return;
      this.init();
      if (!this.ctx) return;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(130, this.ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(75, this.ctx.currentTime + 0.18);
      gain.gain.setValueAtTime(0.14, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.18);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + 0.18);
    }
    playHint() {
      if (this.muted) return;
      this.init();
      if (!this.ctx) return;
      const freqs = [659.25, 830.61, 987.77];
      freqs.forEach((freq, idx) => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sine';
        const startTime = this.ctx.currentTime + idx * 0.07;
        osc.frequency.setValueAtTime(freq, startTime);
        gain.gain.setValueAtTime(0.2, startTime);
        gain.gain.exponentialRampToValueAtTime(0.001, startTime + 0.4);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(startTime);
        osc.stop(startTime + 0.4);
      });
    }
    playLightning() {
      if (this.muted) return;
      this.init();
      if (!this.ctx) return;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(90, this.ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(25, this.ctx.currentTime + 0.5);
      gain.gain.setValueAtTime(0.25, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.5);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + 0.5);
    }
    playCoinShower() {
      if (this.muted) return;
      this.init();
      if (!this.ctx) return;
      const pings = [880, 1174, 1318, 1760];
      pings.forEach((freq, i) => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sine';
        const startTime = this.ctx.currentTime + i * 0.05;
        osc.frequency.setValueAtTime(freq, startTime);
        gain.gain.setValueAtTime(0.18, startTime);
        gain.gain.exponentialRampToValueAtTime(0.001, startTime + 0.28);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(startTime);
        osc.stop(startTime + 0.28);
      });
    }
  }

  /* ==========================================================================
     3. TURKISH LANGUAGE UTILITIES
     ========================================================================== */
  const Turkish = {
    toUpper(str) {
      return (str || '').toLocaleUpperCase('tr-TR');
    },
    toLower(str) {
      return (str || '').toLocaleLowerCase('tr-TR');
    },
    getIstanbulDateString(d = new Date()) {
      try {
        const formatter = new Intl.DateTimeFormat('en-CA', {
          timeZone: 'Europe/Istanbul',
          year: 'numeric',
          month: '2-digit',
          day: '2-digit'
        });
        return formatter.format(d);
      } catch (e) {
        return d.toISOString().split('T')[0];
      }
    },
    getYesterdayIstanbulString() {
      const d = new Date();
      d.setDate(d.getDate() - 1);
      return this.getIstanbulDateString(d);
    }
  };

  /* ==========================================================================
     4. MAIN GAME STATE MACHINE & CONTROLLER
     ========================================================================== */
  class KelimeHarikalariGame {
    constructor() {
      this.storage = new StorageService();
      this.sound = new SoundManager();

      // Core State
      this.currentScreen = 'MENU';
      this.coins = this.storage.get('coins', 200);
      this.levelIdx = this.storage.get('level_idx', 0);
      this.unlockedCityIndex = this.storage.get('unlocked_city_idx', 0);
      this.stars = this.storage.get('stars', 0);
      this.streak = this.storage.get('streak', 1);
      this.completedDailyDates = this.storage.get('daily_dates', []);
      this.bonusChestCount = this.storage.get('bonus_chest', 0);

      // Runtime Level Tracking
      this.currentLevel = null;
      this.selectedCity = CITIES_DATA[0];
      this.isDailyMode = false;
      this.isIdiomMode = false;
      this.isTargetingMode = false;
      this.levelHintsUsed = 0;
      this.levelErrorCount = 0;

      // Unlocks and Tracking
      this.unlockedWordIds = new Set();
      this.revealedCellKeys = new Set();
      this.foundBonusWords = new Set();
      this.dailyStarKeys = new Set();
      this.dailyStarsCollected = new Set();

      // Gesture & Wheel
      this.isDragging = false;
      this.selectedNodeIndices = [];
      this.currentLetters = [];
      this.wheelNodePositions = [];
      this.currentWheelLetters = [];

      this.initDom();
      this.bindEvents();
      this.loadSettings();

      // Start at MENU screen
      this.switchScreen('MENU');
      this.updateTopbar();
      this.renderMap();
    }

    /* ---------------- Screen State Machine ---------------- */
    switchScreen(screenName) {
      this.currentScreen = screenName;
      document.querySelectorAll('.game-screen').forEach(s => s.classList.remove('active'));

      if (screenName === 'MENU') {
        this.dom.screenMenu.classList.add('active');
        this.updateMenuProgress();
      } else if (screenName === 'MAP_VIEW') {
        this.dom.screenMap.classList.add('active');
        this.renderMap();
        this.selectCityInMap(this.selectedCity);
      } else if (screenName === 'GAMEPLAY') {
        if (!this.currentLevel) {
          this.loadLevel(this.levelIdx);
        }
        this.dom.screenGameplay.classList.add('active');
        this.cacheWheelGeometry();
      }
    }

    updateMenuProgress() {
      const curLvl = ALL_LEVELS[this.levelIdx] || ALL_LEVELS[0];
      this.dom.menuCurrentCity.textContent = `${curLvl.city_name} (Plaka ${this.getCityPlate(curLvl.city_name)})`;
      this.dom.menuCurrentLandmark.textContent = `Bölüm ${curLvl.sub_id}: ${curLvl.landmark_name}`;
      this.dom.bgLayer.style.backgroundImage = `url('${curLvl.bg}')`;
    }

    getCityPlate(cityName) {
      const c = CITIES_DATA.find(ci => ci.name === cityName);
      return c ? c.plate : 35;
    }

    initDom() {
      this.dom = {
        bgLayer: document.getElementById('bg-layer'),
        screenMenu: document.getElementById('screen-menu'),
        screenMap: document.getElementById('screen-map'),
        screenGameplay: document.getElementById('screen-gameplay'),

        // Menu elements
        menuCurrentCity: document.getElementById('menu-current-city'),
        menuCurrentLandmark: document.getElementById('menu-current-landmark'),
        btnMenuPlay: document.getElementById('btn-menu-play'),
        btnMenuMap: document.getElementById('btn-menu-map'),
        btnMenuDaily: document.getElementById('btn-menu-daily'),
        btnMenuIdioms: document.getElementById('btn-menu-idioms'),
        btnMenuAbout: document.getElementById('btn-menu-about'),
        btnMenuSound: document.getElementById('btn-menu-sound'),
        btnMenuSettings: document.getElementById('btn-menu-settings'),
        menuSoundIcon: document.getElementById('menu-sound-icon'),

        // Map elements
        btnMapBack: document.getElementById('btn-map-back'),
        turkeySvgMap: document.getElementById('turkey-svg-map'),
        mapRoutesLayer: document.getElementById('map-routes-layer'),
        mapCitiesLayer: document.getElementById('map-cities-layer'),
        drawerCityName: document.getElementById('drawer-city-name'),
        drawerCityDesc: document.getElementById('drawer-city-desc'),
        drawerCityPlate: document.getElementById('drawer-city-plate'),
        drawerLevelsList: document.getElementById('drawer-levels-list'),

        // Gameplay elements
        btnGameplayBack: document.getElementById('btn-gameplay-back'),
        btnGameplaySound: document.getElementById('btn-gameplay-sound'),
        gameplaySoundIcon: document.getElementById('gameplay-sound-icon'),
        btnOpenSettings: document.getElementById('btn-open-settings'),
        gameplayRegionText: document.getElementById('gameplay-region-text'),
        gameplayLevelTitleText: document.getElementById('gameplay-level-title-text'),
        streakIndicator: document.getElementById('streak-indicator'),
        crosswordGrid: document.getElementById('crossword-grid'),
        wordPreview: document.getElementById('word-preview'),
        bonusCounter: document.getElementById('bonus-counter'),
        wheelWrapper: document.getElementById('wheel-wrapper'),
        wheelSvg: document.getElementById('wheel-svg'),
        connectionLine: document.getElementById('connection-line'),
        wheelNodesContainer: document.getElementById('wheel-nodes-container'),

        // Modals
        modalPostcard: document.getElementById('modal-postcard'),
        postcardImg: document.getElementById('postcard-img'),
        postcardCityBadge: document.getElementById('postcard-city-badge'),
        postcardTitle: document.getElementById('postcard-title'),
        postcardSummary: document.getElementById('postcard-summary'),
        postcardTrivia: document.getElementById('postcard-trivia'),
        postcardStars: document.getElementById('postcard-stars'),
        btnPostcardContinue: document.getElementById('btn-postcard-continue'),
        btnPostcard2x: document.getElementById('btn-postcard-2x'),

        modalTravel: document.getElementById('modal-travel'),
        travelTitle: document.getElementById('travel-title'),
        travelSubtitle: document.getElementById('travel-subtitle'),
        travelCityFrom: document.getElementById('travel-city-from'),
        travelCityTo: document.getElementById('travel-city-to'),
        travelPlaneIcon: document.getElementById('travel-plane-icon'),
        btnTravelContinue: document.getElementById('btn-travel-continue'),

        modalMeaning: document.getElementById('modal-meaning'),
        meaningWordTitle: document.getElementById('meaning-word-title'),
        meaningWordType: document.getElementById('meaning-word-type'),
        meaningWordDesc: document.getElementById('meaning-word-desc'),
        btnCloseMeaning: document.getElementById('btn-close-meaning'),

        modalCalendar: document.getElementById('modal-calendar'),
        calendarStreakText: document.getElementById('calendar-streak-text'),
        calendarGridContainer: document.getElementById('calendar-grid-container'),
        btnPlayDaily: document.getElementById('btn-play-daily'),
        btnShareDaily: document.getElementById('btn-share-daily'),
        btnCloseCalendar: document.getElementById('btn-close-calendar'),
        btnOpenDaily: document.getElementById('btn-open-daily'),

        modalIdioms: document.getElementById('modal-idioms'),
        idiomProverbText: document.getElementById('idiom-proverb-text'),
        idiomMeaningText: document.getElementById('idiom-meaning-text'),
        btnPlayIdiom: document.getElementById('btn-play-idiom'),
        btnCloseIdioms: document.getElementById('btn-close-idioms'),

        modalSettings: document.getElementById('modal-settings'),
        btnCloseSettings: document.getElementById('btn-close-settings'),
        toggleSound: document.getElementById('toggle-sound'),
        toggleVibrate: document.getElementById('toggle-vibrate'),
        toggleDyslexic: document.getElementById('toggle-dyslexic'),
        toggleContrast: document.getElementById('toggle-contrast'),

        modalAbout: document.getElementById('modal-about'),
        btnCloseAbout: document.getElementById('btn-close-about'),

        modalNoCoins: document.getElementById('modal-no-coins'),
        btnWatchAdCoins: document.getElementById('btn-watch-ad-coins'),
        btnCloseNoCoins: document.getElementById('btn-close-no-coins'),

        toastNotification: document.getElementById('toast-notification'),
        confettiCanvas: document.getElementById('confetti-canvas'),
        screenFlash: document.getElementById('screen-flash')
      };

      this.ctxConfetti = this.dom.confettiCanvas.getContext('2d');
    }

    bindEvents() {
      // Screen 1: MENU
      this.dom.btnMenuPlay.addEventListener('click', () => {
        this.sound.init();
        this.loadLevel(this.levelIdx);
        this.switchScreen('GAMEPLAY');
      });
      this.dom.btnMenuMap.addEventListener('click', () => {
        this.sound.init();
        this.switchScreen('MAP_VIEW');
      });
      this.dom.btnMenuDaily.addEventListener('click', () => {
        this.sound.init();
        this.openCalendarModal();
      });
      this.dom.btnMenuIdioms.addEventListener('click', () => {
        this.sound.init();
        this.openIdiomsModal();
      });
      this.dom.btnMenuAbout.addEventListener('click', () => this.openAboutModal());
      this.dom.btnMenuSettings.addEventListener('click', () => this.openSettingsModal());
      this.dom.btnMenuSound.addEventListener('click', () => this.toggleSound());

      // Screen 2: MAP VIEW
      this.dom.btnMapBack.addEventListener('click', () => this.switchScreen('MENU'));

      // Screen 3: GAMEPLAY
      this.dom.btnGameplayBack.addEventListener('click', () => this.switchScreen('MAP_VIEW'));
      this.dom.btnGameplaySound.addEventListener('click', () => this.toggleSound());
      this.dom.btnOpenSettings.addEventListener('click', () => this.openSettingsModal());
      this.dom.btnOpenDaily.addEventListener('click', () => this.openCalendarModal());

      // Power-ups
      document.getElementById('btn-shuffle').addEventListener('click', () => this.handleShuffle());
      document.getElementById('btn-hint-bulb').addEventListener('click', () => this.handleBulbHint());
      document.getElementById('btn-hint-target').addEventListener('click', () => this.toggleTargetingMode());
      document.getElementById('btn-hint-lightning').addEventListener('click', () => this.handleLightningHint());
      document.getElementById('btn-bonus-chest').addEventListener('click', () => this.openBonusChestModal());

      // Postcard Modal Buttons
      this.dom.btnPostcardContinue.addEventListener('click', () => {
        this.addCoins(25);
        this.dom.modalPostcard.classList.remove('active');
        this.proceedToNextLevel();
      });
      this.dom.btnPostcard2x.addEventListener('click', () => {
        this.showRewardedAd(() => {
          this.addCoins(50);
          this.dom.modalPostcard.classList.remove('active');
          this.proceedToNextLevel();
        });
      });

      // Travel Modal
      this.dom.btnTravelContinue.addEventListener('click', () => {
        this.dom.modalTravel.classList.remove('active');
        this.loadLevel(this.levelIdx);
        this.switchScreen('GAMEPLAY');
      });

      // TDK Meaning Modal
      this.dom.btnCloseMeaning.addEventListener('click', () => this.dom.modalMeaning.classList.remove('active'));
      this.dom.modalMeaning.addEventListener('click', (e) => {
        if (e.target === this.dom.modalMeaning) this.dom.modalMeaning.classList.remove('active');
      });

      // Settings Modal
      this.dom.btnCloseSettings.addEventListener('click', () => this.dom.modalSettings.classList.remove('active'));
      this.dom.toggleSound.addEventListener('change', (e) => {
        this.sound.muted = !e.target.checked;
        this.updateSoundIcons();
      });
      this.dom.toggleVibrate.addEventListener('change', (e) => {
        this.storage.set('vibrate_enabled', e.target.checked);
      });
      this.dom.toggleDyslexic.addEventListener('change', (e) => {
        document.body.classList.toggle('dyslexic-font', e.target.checked);
        this.storage.set('dyslexic_enabled', e.target.checked);
      });
      this.dom.toggleContrast.addEventListener('change', (e) => {
        document.body.classList.toggle('high-contrast', e.target.checked);
        this.storage.set('contrast_enabled', e.target.checked);
      });

      // Daily Calendar
      this.dom.btnCloseCalendar.addEventListener('click', () => this.dom.modalCalendar.classList.remove('active'));
      this.dom.btnPlayDaily.addEventListener('click', () => {
        this.dom.modalCalendar.classList.remove('active');
        this.startDailyPuzzle();
      });
      this.dom.btnShareDaily.addEventListener('click', () => this.shareDailyResult());

      // Idioms Modal
      this.dom.btnCloseIdioms.addEventListener('click', () => this.dom.modalIdioms.classList.remove('active'));
      this.dom.btnPlayIdiom.addEventListener('click', () => {
        this.dom.modalIdioms.classList.remove('active');
        this.startIdiomPuzzle();
      });

      // About Modal
      this.dom.btnCloseAbout.addEventListener('click', () => this.dom.modalAbout.classList.remove('active'));

      // No Coins Modal
      this.dom.btnCloseNoCoins.addEventListener('click', () => this.dom.modalNoCoins.classList.remove('active'));
      this.dom.btnWatchAdCoins.addEventListener('click', () => {
        this.showRewardedAd(() => {
          this.addCoins(100);
          this.dom.modalNoCoins.classList.remove('active');
          this.showToast("🎁 +100 Altın Hesabınıza Eklendi!");
        });
      });

      // Pointer interaction for letter wheel
      const wrapper = this.dom.wheelWrapper;
      wrapper.addEventListener('pointerdown', (e) => this.onPointerDown(e));
      wrapper.addEventListener('pointermove', (e) => this.onPointerMove(e));
      wrapper.addEventListener('pointerup', (e) => this.onPointerUp(e));
      wrapper.addEventListener('pointercancel', (e) => this.onPointerUp(e));

      window.addEventListener('resize', () => this.cacheWheelGeometry());
    }

    loadSettings() {
      const vib = this.storage.get('vibrate_enabled', true);
      this.dom.toggleVibrate.checked = vib;

      const dys = this.storage.get('dyslexic_enabled', false);
      this.dom.toggleDyslexic.checked = dys;
      if (dys) document.body.classList.add('dyslexic-font');

      const con = this.storage.get('contrast_enabled', false);
      this.dom.toggleContrast.checked = con;
      if (con) document.body.classList.add('high-contrast');
    }

    toggleSound() {
      this.sound.muted = !this.sound.muted;
      this.dom.toggleSound.checked = !this.sound.muted;
      this.updateSoundIcons();
    }

    updateSoundIcons() {
      const icon = this.sound.muted ? '🔇' : '🔊';
      this.dom.menuSoundIcon.textContent = icon;
      this.dom.gameplaySoundIcon.textContent = icon;
    }

    updateTopbar() {
      document.querySelectorAll('.coins-val').forEach(el => el.textContent = this.coins);
      this.dom.bonusCounter.textContent = `${this.bonusChestCount}/5`;
      this.dom.streakIndicator.textContent = `🔥 ${this.streak}`;
    }

    addCoins(amount) {
      this.coins += amount;
      this.storage.set('coins', this.coins);
      this.updateTopbar();
      this.sound.playCoinShower();
    }

    showToast(msg) {
      this.dom.toastNotification.textContent = msg;
      this.dom.toastNotification.classList.add('active');
      setTimeout(() => this.dom.toastNotification.classList.remove('active'), 2000);
    }

    vibrate(pattern) {
      if (this.storage.get('vibrate_enabled', true) && navigator.vibrate) {
        navigator.vibrate(pattern);
      }
    }

    /* ---------------- Interactive Turkey Map ---------------- */
    renderMap() {
      const routesG = this.dom.mapRoutesLayer;
      const citiesG = this.dom.mapCitiesLayer;
      routesG.innerHTML = '';
      citiesG.innerHTML = '';

      // Draw connecting flight/road paths between consecutive cities
      for (let i = 0; i < CITIES_DATA.length - 1; i++) {
        const c1 = CITIES_DATA[i].coords;
        const c2 = CITIES_DATA[i + 1].coords;
        const midX = (c1.x + c2.x) / 2;
        const midY = (c1.y + c2.y) / 2 - 25; // Slight curved arc

        const pathEl = document.createElementNS("http://www.w3.org/2000/svg", "path");
        pathEl.setAttribute("d", `M ${c1.x},${c1.y} Q ${midX},${midY} ${c2.x},${c2.y}`);
        pathEl.setAttribute("fill", "none");
        pathEl.setAttribute("stroke", i < this.unlockedCityIndex ? "#fbbf24" : "rgba(255, 255, 255, 0.2)");
        pathEl.setAttribute("stroke-width", "2.5");
        pathEl.setAttribute("stroke-dasharray", "6,5");
        routesG.appendChild(pathEl);
      }

      // Draw City Markers
      CITIES_DATA.forEach((city, idx) => {
        const isUnlocked = idx <= this.unlockedCityIndex;
        const isCurrent = (ALL_LEVELS[this.levelIdx] && ALL_LEVELS[this.levelIdx].city_id === city.id);

        const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
        g.setAttribute("class", "city-node-circle");
        g.style.cursor = "pointer";

        if (isCurrent) {
          const pulse = document.createElementNS("http://www.w3.org/2000/svg", "circle");
          pulse.setAttribute("cx", city.coords.x);
          pulse.setAttribute("cy", city.coords.y);
          pulse.setAttribute("r", "16");
          pulse.setAttribute("fill", "none");
          pulse.setAttribute("stroke", "#fbbf24");
          pulse.setAttribute("stroke-width", "2");
          pulse.setAttribute("class", "city-node-pulse");
          g.appendChild(pulse);
        }

        const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        circle.setAttribute("cx", city.coords.x);
        circle.setAttribute("cy", city.coords.y);
        circle.setAttribute("r", isCurrent ? "12" : "9");
        circle.setAttribute("fill", isUnlocked ? (isCurrent ? "#fbbf24" : "#38bdf8") : "#334155");
        circle.setAttribute("stroke", "#ffffff");
        circle.setAttribute("stroke-width", "2");
        g.appendChild(circle);

        const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
        label.setAttribute("x", city.coords.x);
        label.setAttribute("y", city.coords.y + 18);
        label.setAttribute("fill", isUnlocked ? "#f8fafc" : "#64748b");
        label.setAttribute("font-size", isCurrent ? "11.5" : "10");
        label.setAttribute("font-weight", isCurrent ? "900" : "700");
        label.setAttribute("text-anchor", "middle");
        label.textContent = city.name + (isUnlocked ? "" : " 🔒");
        g.appendChild(label);

        g.addEventListener("click", () => {
          this.sound.init();
          this.selectCityInMap(city);
        });

        citiesG.appendChild(g);
      });
    }

    selectCityInMap(city) {
      this.selectedCity = city;
      this.dom.drawerCityName.textContent = `${city.name} (${city.region_name})`;
      this.dom.drawerCityDesc.textContent = city.description;
      this.dom.drawerCityPlate.textContent = `Plaka ${city.plate}`;

      const listContainer = this.dom.drawerLevelsList;
      listContainer.innerHTML = '';

      city.levels.forEach((lvl, sIdx) => {
        const globalIdx = ALL_LEVELS.findIndex(al => al.id === lvl.id);
        const isUnlocked = globalIdx <= this.levelIdx;

        const row = document.createElement('div');
        row.className = `drawer-level-item ${isUnlocked ? 'unlocked' : ''}`;
        row.innerHTML = `
          <div>
            <span style="color:${isUnlocked ? '#fbbf24' : '#64748b'}; margin-right:4px;">${sIdx + 1}.</span>
            <span>${lvl.landmark_name}</span>
          </div>
          <div>
            ${isUnlocked ? '<button class="btn-drawer-play">Oyna</button>' : '<span style="color:#64748b;">🔒 Kilitli</span>'}
          </div>
        `;

        if (isUnlocked) {
          row.querySelector('.btn-drawer-play').addEventListener('click', () => {
            this.sound.init();
            this.levelIdx = globalIdx;
            this.storage.set('level_idx', this.levelIdx);
            this.loadLevel(this.levelIdx);
            this.switchScreen('GAMEPLAY');
          });
        }
        listContainer.appendChild(row);
      });
    }

    /* ---------------- Level Loading & Preloading ---------------- */
    loadLevel(levelIndex) {
      this.levelIdx = levelIndex;
      this.isDailyMode = false;
      this.isIdiomMode = false;
      this.isTargetingMode = false;
      this.levelHintsUsed = 0;
      this.levelErrorCount = 0;

      const idx = levelIndex % ALL_LEVELS.length;
      this.currentLevel = ALL_LEVELS[idx];
      this.unlockedWordIds.clear();
      this.revealedCellKeys.clear();
      this.foundBonusWords.clear();
      this.dailyStarKeys.clear();
      this.dailyStarsCollected.clear();

      this.setupLevelUI();

      // Preload next level's background image in memory for instant transitions!
      const nextIdx = (levelIndex + 1) % ALL_LEVELS.length;
      const nextLvl = ALL_LEVELS[nextIdx];
      if (nextLvl && nextLvl.bg) {
        const preImg = new Image();
        preImg.src = nextLvl.bg;
      }
    }

    setupLevelUI() {
      this.dom.bgLayer.style.backgroundImage = `url('${this.currentLevel.bg}')`;
      this.dom.gameplayRegionText.textContent = this.currentLevel.city_name;
      this.dom.gameplayLevelTitleText.textContent = this.isDailyMode ? "Günün Bulmacası" : (this.isIdiomMode ? "Atasözü Modu" : `Bölüm ${this.currentLevel.sub_id}: ${this.currentLevel.landmark_name}`);

      this.renderCrosswordGrid();
      this.currentWheelLetters = [...this.currentLevel.wheel];
      this.renderWheel();
      this.cacheWheelGeometry();
    }

    /* ---------------- Crossword Grid Engine ---------------- */
    renderCrosswordGrid() {
      const words = this.currentLevel.words;
      let minR = Infinity, maxR = -Infinity;
      let minC = Infinity, maxC = -Infinity;

      words.forEach(w => {
        const endR = w.row + (w.dir === 'V' ? w.word.length - 1 : 0);
        const endC = w.col + (w.dir === 'H' ? w.word.length - 1 : 0);
        minR = Math.min(minR, w.row);
        maxR = Math.max(maxR, endR);
        minC = Math.min(minC, w.col);
        maxC = Math.max(maxC, endC);
      });

      this.normMinR = minR;
      this.normMinC = minC;

      const rowsCount = maxR - minR + 1;
      const colsCount = maxC - minC + 1;

      const gridEl = this.dom.crosswordGrid;
      gridEl.innerHTML = '';
      gridEl.style.gridTemplateRows = `repeat(${rowsCount}, 1fr)`;
      gridEl.style.gridTemplateColumns = `repeat(${colsCount}, 1fr)`;

      const boardArea = document.getElementById('board-area');
      const maxW = Math.min(boardArea.clientWidth - 16, 360);
      const maxH = Math.min(boardArea.clientHeight - 16, 260);

      const cellSize = Math.min(Math.floor(maxW / colsCount), Math.floor(maxH / rowsCount), 48);
      gridEl.style.width = `${cellSize * colsCount + (colsCount - 1) * 5}px`;
      gridEl.style.height = `${cellSize * rowsCount + (rowsCount - 1) * 5}px`;

      this.gridLetterMap = new Map();
      words.forEach(w => {
        for (let i = 0; i < w.word.length; i++) {
          const r = w.row - minR + (w.dir === 'V' ? i : 0);
          const c = w.col - minC + (w.dir === 'H' ? i : 0);
          const key = `${r}_${c}`;
          if (!this.gridLetterMap.has(key)) {
            this.gridLetterMap.set(key, { char: w.word[i], words: [w] });
          } else {
            this.gridLetterMap.get(key).words.push(w);
          }
        }
      });

      for (let r = 0; r < rowsCount; r++) {
        for (let c = 0; c < colsCount; c++) {
          const key = `${r}_${c}`;
          const cellEl = document.createElement('div');
          cellEl.className = 'crossword-cell';
          cellEl.dataset.key = key;

          if (this.gridLetterMap.has(key)) {
            const cellData = this.gridLetterMap.get(key);
            const isRevealed = this.revealedCellKeys.has(key);

            cellEl.innerHTML = `
              <div class="cell-inner">
                <div class="cell-front"></div>
                <div class="cell-back">${cellData.char}</div>
              </div>
            `;
            if (isRevealed) cellEl.classList.add('revealed');
            cellEl.addEventListener('click', () => this.onCellClicked(key));
          } else {
            cellEl.classList.add('hidden');
          }
          gridEl.appendChild(cellEl);
        }
      }
    }

    onCellClicked(cellKey) {
      if (!this.isTargetingMode) {
        // TDK Word Meaning Click: If revealed, show authentic dictionary entry!
        if (this.revealedCellKeys.has(cellKey)) {
          const cellData = this.gridLetterMap.get(cellKey);
          if (cellData && cellData.words && cellData.words.length > 0) {
            const unlockedWord = cellData.words.find(w => this.unlockedWordIds.has(w.id)) || cellData.words[0];
            if (unlockedWord) {
              this.showWordMeaningModal(unlockedWord.word);
            }
          }
        }
        return;
      }
      if (this.revealedCellKeys.has(cellKey)) {
        this.showToast("Bu kutucuk zaten açık!");
        return;
      }

      this.coins -= 100;
      this.storage.set('coins', this.coins);
      this.updateTopbar();
      this.sound.playHint();
      this.levelHintsUsed++;

      this.isTargetingMode = false;
      document.getElementById('btn-hint-target').classList.remove('active-tool');
      document.body.classList.remove('targeting-mode');
      this.revealSingleCell(cellKey);
    }

    showWordMeaningModal(rawWord) {
      const word = Turkish.toUpper(rawWord);
      const dictEntry = (typeof TDK_DICTIONARY !== 'undefined' && TDK_DICTIONARY[word]) ? TDK_DICTIONARY[word] : {
        type: "TDK GÜNCEL SÖZLÜK",
        meaning: `"${word}" sözcüğü: Türk Dil Kurumu standartlarına uygun, Türkçe kökenli veya dilimize yerleşmiş geçerli sözcük.`
      };

      const modal = this.dom.modalMeaning;
      if (!modal) return;
      this.dom.meaningWordTitle.textContent = word;
      this.dom.meaningWordType.textContent = dictEntry.type || "TDK GÜNCEL SÖZLÜK";
      this.dom.meaningWordDesc.textContent = dictEntry.meaning;
      modal.classList.add('active');
    }

    /* ---------------- Wheel & Interaction ---------------- */
    renderWheel() {
      const container = this.dom.wheelNodesContainer;
      container.innerHTML = '';

      const letters = this.currentWheelLetters;
      const count = letters.length;
      const radius = (this.dom.wheelWrapper.clientWidth / 2) - 30;
      const center = this.dom.wheelWrapper.clientWidth / 2;

      this.wheelNodePositions = [];
      letters.forEach((char, idx) => {
        const angle = (idx * (2 * Math.PI / count)) - (Math.PI / 2);
        const x = center + radius * Math.cos(angle);
        const y = center + radius * Math.sin(angle);

        const node = document.createElement('div');
        node.className = 'wheel-node';
        node.textContent = char;
        node.style.left = `${x}px`;
        node.style.top = `${y}px`;
        node.dataset.index = idx;

        container.appendChild(node);
        this.wheelNodePositions.push({ index: idx, char: char, x: x, y: y, element: node });
      });
    }

    cacheWheelGeometry() {
      if (!this.currentWheelLetters) return;
      this.renderWheel();
    }

    handleShuffle() {
      this.vibrate(20);
      this.dom.wheelNodesContainer.style.transition = 'transform 0.35s cubic-bezier(0.34, 1.56, 0.64, 1)';
      this.dom.wheelNodesContainer.style.transform = 'rotate(360deg)';

      setTimeout(() => {
        this.currentWheelLetters.sort(() => 0.5 - Math.random());
        this.dom.wheelNodesContainer.style.transition = 'none';
        this.dom.wheelNodesContainer.style.transform = 'rotate(0deg)';
        this.renderWheel();
      }, 350);
    }

    onPointerDown(e) {
      this.sound.init();
      this.isDragging = true;
      this.selectedNodeIndices = [];
      this.currentLetters = [];
      this.dom.wheelWrapper.setPointerCapture(e.pointerId);
      this.checkPointerCollision(e.clientX, e.clientY);
    }

    onPointerMove(e) {
      if (!this.isDragging) return;
      this.checkPointerCollision(e.clientX, e.clientY);
      this.updateConnectionLine(e.clientX, e.clientY);
    }

    onPointerUp(e) {
      if (!this.isDragging) return;
      this.isDragging = false;

      if (this.currentLetters.length > 0) {
        const formed = Turkish.toUpper(this.currentLetters.join(''));
        this.submitWord(formed);
      }

      this.selectedNodeIndices = [];
      this.currentLetters = [];
      this.dom.connectionLine.setAttribute('points', '');
      this.dom.wordPreview.classList.remove('active');
      document.querySelectorAll('.wheel-node.selected').forEach(n => n.classList.remove('selected'));
    }

    checkPointerCollision(clientX, clientY) {
      const rect = this.dom.wheelWrapper.getBoundingClientRect();
      const relX = clientX - rect.left;
      const relY = clientY - rect.top;
      const hitRadius = 34;

      for (let i = 0; i < this.wheelNodePositions.length; i++) {
        const node = this.wheelNodePositions[i];
        const dx = relX - node.x;
        const dy = relY - node.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist <= hitRadius) {
          if (!this.selectedNodeIndices.includes(i)) {
            this.selectedNodeIndices.push(i);
            this.currentLetters.push(node.char);
            node.element.classList.add('selected');

            this.vibrate(12);
            this.sound.playLetterNote(this.selectedNodeIndices.length - 1);

            const word = this.currentLetters.join('');
            this.dom.wordPreview.textContent = word;
            this.dom.wordPreview.classList.add('active');
          } else if (this.selectedNodeIndices.length > 1 &&
                     this.selectedNodeIndices[this.selectedNodeIndices.length - 2] === i) {
            const popped = this.selectedNodeIndices.pop();
            this.currentLetters.pop();
            this.wheelNodePositions[popped].element.classList.remove('selected');

            this.vibrate(10);
            const word = this.currentLetters.join('');
            this.dom.wordPreview.textContent = word;
            if (this.currentLetters.length === 0) {
              this.dom.wordPreview.classList.remove('active');
            }
          }
          break;
        }
      }
    }

    updateConnectionLine(pointerClientX, pointerClientY) {
      if (this.selectedNodeIndices.length === 0) {
        this.dom.connectionLine.setAttribute('points', '');
        return;
      }
      const rect = this.dom.wheelWrapper.getBoundingClientRect();
      const relX = pointerClientX - rect.left;
      const relY = pointerClientY - rect.top;

      let pointsStr = '';
      this.selectedNodeIndices.forEach(idx => {
        const node = this.wheelNodePositions[idx];
        pointsStr += `${node.x},${node.y} `;
      });
      pointsStr += `${relX},${relY}`;
      this.dom.connectionLine.setAttribute('points', pointsStr);
    }

    /* ---------------- Word Submission ---------------- */
    submitWord(word) {
      const matchLevelWord = this.currentLevel.words.find(w => Turkish.toUpper(w.word) === word);

      if (matchLevelWord) {
        if (this.unlockedWordIds.has(matchLevelWord.id)) {
          this.showToast("Bu kelime zaten açık!");
          this.sound.playErrorBuzz();
        } else {
          this.unlockCrosswordWord(matchLevelWord);
        }
      } else if (this.currentLevel.bonus && this.currentLevel.bonus.map(b => Turkish.toUpper(b)).includes(word)) {
        if (this.foundBonusWords.has(word)) {
          this.showToast("Bu bonus kelime zaten bulundu!");
          this.sound.playErrorBuzz();
        } else {
          this.foundBonusWords.add(word);
          this.sound.playWordSuccess();
          this.showToast(`✨ Bonus Kelime: ${word}`);

          this.bonusChestCount++;
          if (this.bonusChestCount >= 5) {
            this.bonusChestCount = 0;
            this.addCoins(30);
            this.showToast("🎁 Bonus Sandığı Açıldı: +30 Altın!");
          }
          this.storage.set('bonus_chest', this.bonusChestCount);
          this.updateTopbar();
        }
      } else {
        this.levelErrorCount++;
        this.sound.playErrorBuzz();
        this.vibrate([20, 40, 20]);
      }
    }

    unlockCrosswordWord(wordObj) {
      this.unlockedWordIds.add(wordObj.id);
      this.sound.playWordSuccess();
      this.vibrate(30);

      const normR = wordObj.row - this.normMinR;
      const normC = wordObj.col - this.normMinC;

      const previewRect = this.dom.wordPreview.getBoundingClientRect();
      const originX = previewRect.left + previewRect.width / 2;
      const originY = previewRect.top + previewRect.height / 2;

      for (let i = 0; i < wordObj.word.length; i++) {
        const r = normR + (wordObj.dir === 'V' ? i : 0);
        const c = normC + (wordObj.dir === 'H' ? i : 0);
        const key = `${r}_${c}`;

        const cellEl = document.querySelector(`.crossword-cell[data-key="${key}"]`);
        if (cellEl) {
          const cellRect = cellEl.getBoundingClientRect();
          const targetX = cellRect.left + cellRect.width / 2;
          const targetY = cellRect.top + cellRect.height / 2;

          this.spawnSpark(originX, originY, targetX, targetY, i * 70, () => {
            cellEl.classList.add('revealed');
            this.revealedCellKeys.add(key);
            this.checkLevelCompletion();
          });
        }
      }
    }

    spawnSpark(startX, startY, endX, endY, delayMs, onArrive) {
      setTimeout(() => {
        const spark = document.createElement('div');
        spark.className = 'spark-projectile';
        spark.style.left = `${startX}px`;
        spark.style.top = `${startY}px`;
        document.body.appendChild(spark);
        spark.getBoundingClientRect();
        spark.style.transform = `translate(${endX - startX}px, ${endY - startY}px) scale(1.5)`;

        setTimeout(() => {
          spark.remove();
          if (onArrive) onArrive();
        }, 420);
      }, delayMs);
    }

    /* ---------------- Victory & Milestone Flow ---------------- */
    checkLevelCompletion() {
      if (this.unlockedWordIds.size === this.currentLevel.words.length) {
        setTimeout(() => this.triggerVictory(), 500);
      }
    }

    triggerVictory() {
      if (this.isDailyMode) {
        const todayStr = Turkish.getIstanbulDateString();
        const yesterdayStr = Turkish.getYesterdayIstanbulString();

        if (!this.completedDailyDates.includes(todayStr)) {
          if (this.completedDailyDates.includes(yesterdayStr)) {
            this.streak++;
          } else {
            this.streak = 1;
          }
          this.completedDailyDates.push(todayStr);
          this.storage.set('daily_dates', this.completedDailyDates);
          this.storage.set('streak', this.streak);
          this.updateTopbar();
        }
        this.sound.playMilestoneFanfare();
        this.startConfetti();
        this.openCalendarModal();
        return;
      }

      if (this.isIdiomMode) {
        this.sound.playLevelChime();
        this.addCoins(25);
        this.showToast("🎉 Tebrikler! Atasözü Tamamlandı (+25 🪙)");
        setTimeout(() => this.openNextIdiom(), 1200);
        return;
      }

      // REGULAR GAMEPLAY FLOW:
      const isSubLevel5 = (this.currentLevel.sub_id === 5);

      if (isSubLevel5) {
        // City completed! Show Digital Postcard and prepare travel transition!
        this.sound.playMilestoneFanfare();
        this.startConfetti();
        this.openPostcardModal();
      } else {
        // Normal level (1, 2, 3, 4): Fast, pleasant, addictive auto-progression!
        this.sound.playLevelChime();
        this.addCoins(25);
        this.showToast(`🎉 Bölüm ${this.currentLevel.sub_id} Tamamlandı! (+25 🪙)`);

        document.querySelectorAll('.crossword-cell.revealed .cell-back').forEach(el => {
          el.style.boxShadow = '0 0 16px rgba(251, 191, 36, 0.9)';
          setTimeout(() => el.style.boxShadow = '', 800);
        });

        setTimeout(() => this.proceedToNextLevel(), 1100);
      }
    }

    openPostcardModal() {
      const pc = this.currentLevel.postcard;
      this.dom.postcardImg.src = pc.bg;
      this.dom.postcardCityBadge.textContent = `${pc.city.toUpperCase('tr-TR')} • PLAKA ${pc.plate}`;
      this.dom.postcardTitle.textContent = pc.title;
      this.dom.postcardSummary.textContent = pc.summary;
      this.dom.postcardTrivia.innerHTML = `💡 Biliyor muydunuz? ${pc.trivia}`;

      let starCount = 3;
      if (this.levelHintsUsed > 1 || this.levelErrorCount > 4) starCount = 1;
      else if (this.levelHintsUsed > 0 || this.levelErrorCount > 1) starCount = 2;
      this.dom.postcardStars.textContent = '⭐'.repeat(starCount) + '☆'.repeat(3 - starCount);

      this.dom.modalPostcard.classList.add('active');
    }

    proceedToNextLevel() {
      this.stopConfetti();
      const currentSubId = this.currentLevel.sub_id;

      if (currentSubId === 5) {
        // Check if there is a next city to travel to!
        const currentCityIndex = CITIES_DATA.findIndex(c => c.id === this.currentLevel.city_id);
        const nextCityIndex = currentCityIndex + 1;

        if (nextCityIndex < CITIES_DATA.length) {
          // Unlock next city!
          this.unlockedCityIndex = Math.max(this.unlockedCityIndex, nextCityIndex);
          this.storage.set('unlocked_city_idx', this.unlockedCityIndex);

          // Launch travel animation!
          this.triggerTravelTransition(CITIES_DATA[currentCityIndex], CITIES_DATA[nextCityIndex]);
          return;
        }
      }

      this.levelIdx = (this.levelIdx + 1) % ALL_LEVELS.length;
      this.storage.set('level_idx', this.levelIdx);
      this.loadLevel(this.levelIdx);
    }

    triggerTravelTransition(cityFrom, cityTo) {
      this.sound.playTravelWhoosh();
      this.dom.travelCityFrom.textContent = cityFrom.name;
      this.dom.travelCityTo.textContent = cityTo.name;
      this.dom.travelTitle.textContent = `${cityTo.name.toUpperCase('tr-TR')}'E SEYAHAT!`;
      this.dom.travelSubtitle.textContent = `${cityFrom.name} tamamlandı, yeni rota ${cityTo.name}!`;

      // Animate plane icon along path
      const plane = this.dom.travelPlaneIcon;
      plane.style.transition = 'transform 1.8s cubic-bezier(0.25, 1, 0.5, 1)';
      plane.style.transform = 'translate(320px, 20px)';

      this.dom.modalTravel.classList.add('active');
      this.startConfetti();

      // Setup next city first level
      this.levelIdx = (this.levelIdx + 1) % ALL_LEVELS.length;
      this.storage.set('level_idx', this.levelIdx);
    }

    /* ---------------- Power-ups ---------------- */
    handleBulbHint() {
      if (this.coins < 50) {
        this.dom.modalNoCoins.classList.add('active');
        return;
      }
      this.coins -= 50;
      this.storage.set('coins', this.coins);
      this.updateTopbar();
      this.sound.playHint();
      this.levelHintsUsed++;

      const lockedKeys = Array.from(this.gridLetterMap.keys()).filter(k => !this.revealedCellKeys.has(k));
      if (lockedKeys.length > 0) {
        const randKey = lockedKeys[Math.floor(Math.random() * lockedKeys.length)];
        this.revealSingleCell(randKey);
      }
    }

    toggleTargetingMode() {
      if (this.coins < 100) {
        this.dom.modalNoCoins.classList.add('active');
        return;
      }
      this.isTargetingMode = !this.isTargetingMode;
      document.getElementById('btn-hint-target').classList.toggle('active-tool', this.isTargetingMode);
      document.body.classList.toggle('targeting-mode', this.isTargetingMode);
    }

    handleLightningHint() {
      if (this.coins < 150) {
        this.dom.modalNoCoins.classList.add('active');
        return;
      }
      this.coins -= 150;
      this.storage.set('coins', this.coins);
      this.updateTopbar();
      this.sound.playLightning();
      this.levelHintsUsed += 2;

      this.dom.screenFlash.style.opacity = '0.8';
      setTimeout(() => this.dom.screenFlash.style.opacity = '0', 120);

      const lockedKeys = Array.from(this.gridLetterMap.keys()).filter(k => !this.revealedCellKeys.has(k));
      const count = Math.min(3, lockedKeys.length);
      lockedKeys.sort(() => 0.5 - Math.random());

      for (let i = 0; i < count; i++) {
        setTimeout(() => this.revealSingleCell(lockedKeys[i]), i * 140);
      }
    }

    revealSingleCell(cellKey) {
      const cellEl = document.querySelector(`.crossword-cell[data-key="${cellKey}"]`);
      if (!cellEl) return;

      cellEl.classList.add('revealed');
      this.revealedCellKeys.add(cellKey);

      // Check word unlock
      this.currentLevel.words.forEach(w => {
        if (!this.unlockedWordIds.has(w.id)) {
          const normR = w.row - this.normMinR;
          const normC = w.col - this.normMinC;
          let allOpen = true;
          for (let i = 0; i < w.word.length; i++) {
            const r = normR + (w.dir === 'V' ? i : 0);
            const c = normC + (w.dir === 'H' ? i : 0);
            if (!this.revealedCellKeys.has(`${r}_${c}`)) {
              allOpen = false;
              break;
            }
          }
          if (allOpen) this.unlockedWordIds.add(w.id);
        }
      });
      this.checkLevelCompletion();
    }

    /* ---------------- Calendar & Daily ---------------- */
    openCalendarModal() {
      const now = new Date();
      const currentYear = now.getFullYear();
      const currentMonth = now.getMonth();
      const todayStr = Turkish.getIstanbulDateString();
      const todayDate = parseInt(todayStr.split('-')[2], 10);

      this.dom.calendarStreakText.textContent = `🔥 ${this.streak} Günlük Seri`;
      const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
      const firstDayIndex = new Date(currentYear, currentMonth, 1).getDay();
      const startCol = (firstDayIndex + 6) % 7;

      const container = this.dom.calendarGridContainer;
      container.innerHTML = '';

      ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'].forEach(dh => {
        const headerCell = document.createElement('div');
        headerCell.style.fontSize = "10px";
        headerCell.style.fontWeight = "800";
        headerCell.style.color = "#94a3b8";
        headerCell.style.textAlign = "center";
        headerCell.textContent = dh;
        container.appendChild(headerCell);
      });

      for (let i = 0; i < startCol; i++) container.appendChild(document.createElement('div'));

      for (let day = 1; day <= daysInMonth; day++) {
        const dayCell = document.createElement('div');
        dayCell.style.height = "32px";
        dayCell.style.borderRadius = "6px";
        dayCell.style.display = "flex";
        dayCell.style.alignItems = "center";
        dayCell.style.justifyContent = "center";
        dayCell.style.fontSize = "11px";
        dayCell.style.fontWeight = "800";
        dayCell.style.background = "rgba(15, 23, 42, 0.6)";
        dayCell.style.border = "1px solid rgba(255, 255, 255, 0.08)";
        dayCell.textContent = day;

        const dateStr = `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
        if (this.completedDailyDates.includes(dateStr)) {
          dayCell.style.background = "rgba(34, 197, 94, 0.3)";
          dayCell.style.borderColor = "rgba(34, 197, 94, 0.6)";
          dayCell.style.color = "#86efac";
        }
        if (day === todayDate) {
          dayCell.style.border = "2px solid #fbbf24";
        }
        container.appendChild(dayCell);
      }

      this.dom.modalCalendar.classList.add('active');
    }

    startDailyPuzzle() {
      this.isDailyMode = true;
      this.isIdiomMode = false;
      const dateStr = Turkish.getIstanbulDateString();
      let seedVal = 0;
      for (let i = 0; i < dateStr.length; i++) seedVal = (seedVal * 31 + dateStr.charCodeAt(i)) >>> 0;
      const dailyLevelIndex = seedVal % ALL_LEVELS.length;

      this.currentLevel = JSON.parse(JSON.stringify(ALL_LEVELS[dailyLevelIndex]));
      this.currentLevel.title = "Günün Bulmacası";
      this.currentLevel.city_name = "GÜNLÜK GÖREV";
      this.unlockedWordIds.clear();
      this.revealedCellKeys.clear();
      this.foundBonusWords.clear();

      this.setupLevelUI();
      this.switchScreen('GAMEPLAY');
    }

    shareDailyResult() {
      const todayStr = Turkish.getIstanbulDateString();
      const shareText = `Kelime Harikaları Günlük #${todayStr}\n⭐ 3/3 Yıldız Toplandı\n🔥 ${this.streak} Günlük Seri\nOyna: https://umutcandemircan.github.io/kelime-harikalari/`;
      if (navigator.share) {
        navigator.share({ title: "Kelime Harikaları", text: shareText }).catch(() => {});
      } else if (navigator.clipboard) {
        navigator.clipboard.writeText(shareText).then(() => this.showToast("📋 Paylaşım metni panoya kopyalandı!"));
      }
    }

    /* ---------------- Idioms ---------------- */
    openIdiomsModal() {
      this.selectedIdiom = IDIOMS_DATA[Math.floor(Math.random() * IDIOMS_DATA.length)];
      this.dom.idiomProverbText.textContent = `"${this.selectedIdiom.text}"`;
      this.dom.idiomMeaningText.textContent = `Anlamı: ${this.selectedIdiom.meaning}`;
      this.dom.modalIdioms.classList.add('active');
    }

    startIdiomPuzzle() {
      this.isIdiomMode = true;
      this.isDailyMode = false;
      const word = Turkish.toUpper(this.selectedIdiom.answer);
      const wheelLetters = word.split('').sort(() => 0.5 - Math.random());

      this.currentLevel = {
        id: "idiom",
        sub_id: 1,
        title: "Atasözü Tamamlama",
        city_name: "TÜRKÇE KÜLTÜR",
        landmark_name: this.selectedIdiom.text,
        bg: "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?auto=format&fit=crop&w=1080&q=75",
        wheel: wheelLetters,
        words: [{ id: "iw1", word: word, row: 0, col: 0, dir: "H" }],
        bonus: []
      };

      this.unlockedWordIds.clear();
      this.revealedCellKeys.clear();
      this.foundBonusWords.clear();
      this.setupLevelUI();
      this.switchScreen('GAMEPLAY');
    }

    openNextIdiom() {
      this.openIdiomsModal();
    }

    openBonusChestModal() {
      this.showToast(`🎁 Bonus Sandığı: ${this.bonusChestCount}/5 kelime`);
    }

    openSettingsModal() {
      this.dom.modalSettings.classList.add('active');
    }

    openAboutModal() {
      this.dom.modalAbout.classList.add('active');
    }

    /* ---------------- Ad Hooks ---------------- */
    showRewardedAd(onReward) {
      this.showToast("🎬 Reklam yükleniyor (3 sn)...");
      setTimeout(() => {
        if (onReward) onReward();
      }, 1500);
    }

    /* ---------------- Confetti Particles ---------------- */
    startConfetti() {
      const canvas = this.dom.confettiCanvas;
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      const colors = ['#f59e0b', '#fbbf24', '#22c55e', '#38bdf8', '#a855f7', '#ec4899'];
      this.confettiParticles = [];

      for (let i = 0; i < 70; i++) {
        this.confettiParticles.push({
          x: Math.random() * canvas.width,
          y: Math.random() * -canvas.height,
          size: Math.random() * 7 + 5,
          color: colors[Math.floor(Math.random() * colors.length)],
          vx: Math.random() * 4 - 2,
          vy: Math.random() * 5 + 3,
          rot: Math.random() * 360,
          vRot: Math.random() * 6 - 3
        });
      }

      const animate = () => {
        this.ctxConfetti.clearRect(0, 0, canvas.width, canvas.height);
        this.confettiParticles.forEach(p => {
          p.x += p.vx;
          p.y += p.vy;
          p.rot += p.vRot;
          this.ctxConfetti.save();
          this.ctxConfetti.translate(p.x, p.y);
          this.ctxConfetti.rotate((p.rot * Math.PI) / 180);
          this.ctxConfetti.fillStyle = p.color;
          this.ctxConfetti.fillRect(-p.size / 2, -p.size / 2, p.size, p.size);
          this.ctxConfetti.restore();

          if (p.y > canvas.height + 20) {
            p.y = -20;
            p.x = Math.random() * canvas.width;
          }
        });
        this.confettiAnimId = requestAnimationFrame(animate);
      };
      animate();
    }

    stopConfetti() {
      if (this.confettiAnimId) cancelAnimationFrame(this.confettiAnimId);
      this.ctxConfetti.clearRect(0, 0, this.dom.confettiCanvas.width, this.dom.confettiCanvas.height);
      this.confettiParticles = [];
    }
  }

  // Safe Global Initialization
  window.addEventListener('DOMContentLoaded', () => {
    window.game = new KelimeHarikalariGame();
  });

  // PWA Service Worker Registration
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('sw.js').catch(() => {});
    });
  }
  </script>
</body>
</html>
'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("v3 Masterpiece index.html built successfully!")
