# -*- coding: utf-8 -*-
"""
Clean, Production-Grade Compiler for Kelime Harikaları v2.0.0
"""
import json

with open("credits.json", "r", encoding="utf-8") as f:
    credits_data = json.load(f)

with open("idioms.json", "r", encoding="utf-8") as f:
    idioms_data = json.load(f)

with open("levels_100.json", "r", encoding="utf-8") as f:
    levels_data = json.load(f)

# Update level 1 bg to official Kapadokya balloon photo
levels_data[0]["bg"] = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Hot_air_balloon_over_Cappadocia.jpg/1280px-Hot_air_balloon_over_Cappadocia.jpg"

HTML_TEMPLATE = r'''<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>Kelime Harikaları - Türkçe Çapraz Bulmaca ve Kelime Oyunu</title>
  <meta name="description" content="Anadolu'nun ve dünyanın kültürel harikalarını keşfederek Türkçe kelime dağarcığını geliştireceğin, adil ve akıcı çapraz bulmaca oyunu.">
  <meta name="theme-color" content="#020617">
  
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://umutcandemircan.github.io/kelime-harikalari/">
  <meta property="og:title" content="Kelime Harikaları - Türkçe Çapraz Bulmaca">
  <meta property="og:description" content="Harfleri birleştir, gizli kelimeleri çöz, Türkiye'nin kültürel mirasını adım adım keşfet!">
  <meta property="og:image" content="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Hot_air_balloon_over_Cappadocia.jpg/1280px-Hot_air_balloon_over_Cappadocia.jpg">
  
  <link rel="manifest" href="manifest.json">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700;800;900&display=swap" rel="stylesheet">
  
  <style>
    :root {
      --font-main: 'Outfit', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-dyslexia: 'Comic Sans MS', 'OpenDyslexic', cursive, sans-serif;
      
      --gold: #f59e0b;
      --gold-light: #fef08a;
      --gold-glow: rgba(245, 158, 11, 0.4);
      --green: #22c55e;
      --green-glow: rgba(34, 197, 94, 0.4);
      --cyan: #06b6d4;
      --cyan-glow: rgba(6, 182, 212, 0.4);
      --purple: #a855f7;
      --navy-900: #020617;
      --navy-800: #0f172a;
      --navy-700: #1e293b;
      
      --wheel-size: min(205px, 29vh, 60vw);
      --node-size: 46px;
    }

    /* Dyslexia Mode */
    body.dyslexia-font {
      --font-main: var(--font-dyslexia);
      letter-spacing: 0.8px;
    }

    /* High Contrast Mode */
    body.high-contrast {
      --navy-900: #000000;
      --navy-800: #111111;
      --gold: #ffff00;
      --gold-light: #ffffff;
      --green: #00ff00;
      --cyan: #00ffff;
    }
    body.high-contrast .cell-front {
      border: 2px solid #ffffff !important;
      background: rgba(0, 0, 0, 0.9) !important;
    }
    body.high-contrast .cell-back {
      border: 3px solid #ffff00 !important;
      background: #ffffff !important;
      color: #000000 !important;
    }

    /* Reduced Motion */
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
      background: #020617;
      color: #fff;
    }

    #bg-layer {
      position: absolute;
      inset: 0;
      background-size: cover;
      background-position: center;
      filter: brightness(0.55) saturate(1.25);
      transition: background-image 0.7s cubic-bezier(0.4, 0, 0.2, 1);
      z-index: 0;
    }

    #bg-gradient {
      position: absolute;
      inset: 0;
      background: radial-gradient(circle at 50% 30%, rgba(15, 23, 42, 0.2) 0%, rgba(2, 6, 23, 0.92) 100%);
      z-index: 1;
    }

    #app-container {
      position: relative;
      z-index: 2;
      width: 100%;
      max-width: 440px;
      height: 100%;
      height: 100dvh;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: max(8px, env(safe-area-inset-top)) 8px max(8px, env(safe-area-inset-bottom)) 8px;
    }

    /* Top Navigation Bar */
    header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 44px;
      gap: 4px;
      flex-shrink: 0;
      width: 100%;
    }

    .header-pill {
      display: flex;
      align-items: center;
      gap: 5px;
      background: rgba(15, 23, 42, 0.88);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      padding: 4px 8px;
      border-radius: 999px;
      border: 1px solid rgba(255, 255, 255, 0.16);
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
      font-weight: 700;
      font-size: 11.5px;
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
      background: rgba(15, 23, 42, 0.88);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.16);
      border-radius: 999px;
      padding: 4px 7px;
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

    /* Crossword Board Area */
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

    /* Crossword Cells */
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

    /* Targeting mode pulse */
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

    /* Targeting Banner: Hidden by default, visible only in targeting mode */
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

    /* Bottom Section */
    #bottom-section {
      display: flex;
      flex-direction: column;
      align-items: center;
      flex-shrink: 0;
    }

    /* Word Preview Pill */
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
      -webkit-backdrop-filter: blur(14px);
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

    /* Power-ups Toolbar */
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

    /* Wheel Container */
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

    #screen-flash {
      position: fixed;
      inset: 0;
      background: #fff;
      opacity: 0;
      pointer-events: none;
      z-index: 9999;
      transition: opacity 0.1s ease-out;
    }
    #screen-flash.flash {
      opacity: 0.85;
    }

    .spark-projectile {
      position: fixed;
      width: 12px;
      height: 12px;
      border-radius: 50%;
      background: #fbbf24;
      box-shadow: 0 0 14px #fbbf24, 0 0 24px #f59e0b;
      pointer-events: none;
      z-index: 1000;
      transition: all 0.42s cubic-bezier(0.25, 1, 0.5, 1);
    }

    .star-projectile {
      position: fixed;
      font-size: 20px;
      pointer-events: none;
      z-index: 1001;
      filter: drop-shadow(0 0 10px rgba(245, 158, 11, 0.9));
      transition: all 0.60s cubic-bezier(0.2, 0.8, 0.2, 1);
    }

    .floating-toast {
      position: fixed;
      bottom: 210px;
      left: 50%;
      transform: translateX(-50%) translateY(0);
      background: rgba(15, 23, 42, 0.92);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.2);
      padding: 7px 18px;
      border-radius: 999px;
      font-weight: 800;
      font-size: 13px;
      color: #fef08a;
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.45);
      z-index: 2000;
      pointer-events: none;
      animation: toastAnim 1.5s forwards;
    }
    @keyframes toastAnim {
      0% { opacity: 0; transform: translateX(-50%) translateY(12px); }
      15% { opacity: 1; transform: translateX(-50%) translateY(0); }
      75% { opacity: 1; transform: translateX(-50%) translateY(-4px); }
      100% { opacity: 0; transform: translateX(-50%) translateY(-22px); }
    }

    /* Modals System */
    .modal-overlay {
      position: fixed;
      inset: 0;
      background: rgba(2, 6, 23, 0.85);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      z-index: 5000;
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
      max-width: 420px;
      max-height: 90vh;
      overflow-y: auto;
      background: linear-gradient(135deg, rgba(30, 41, 59, 0.96), rgba(15, 23, 42, 0.98));
      border: 1.5px solid rgba(255, 255, 255, 0.18);
      border-radius: 22px;
      padding: 20px;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), 0 0 30px rgba(245, 158, 11, 0.2);
      text-align: center;
      transform: scale(0.92);
      transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .modal-overlay.active .modal-card {
      transform: scale(1);
    }

    .discovery-img {
      width: 100%;
      height: 190px;
      border-radius: 14px;
      object-fit: cover;
      margin-bottom: 12px;
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
      border: 1.5px solid rgba(255, 255, 255, 0.2);
    }
    .discovery-badge {
      display: inline-block;
      background: rgba(245, 158, 11, 0.2);
      border: 1px solid rgba(245, 158, 11, 0.6);
      color: #fef08a;
      font-size: 11px;
      font-weight: 800;
      padding: 3px 10px;
      border-radius: 999px;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      margin-bottom: 6px;
    }
    .discovery-title {
      font-size: 19px;
      font-weight: 900;
      color: #fff;
      margin-bottom: 8px;
    }
    .discovery-trivia {
      font-size: 12.5px;
      line-height: 1.5;
      color: #cbd5e1;
      margin-bottom: 16px;
      background: rgba(15, 23, 42, 0.6);
      padding: 10px;
      border-radius: 12px;
      border: 1px solid rgba(255, 255, 255, 0.1);
      text-align: left;
    }

    .btn-gold {
      cursor: pointer;
      width: 100%;
      padding: 13px 18px;
      border-radius: 999px;
      border: none;
      background: linear-gradient(135deg, #fbbf24, #d97706);
      color: #0f172a;
      font-weight: 900;
      font-size: 15px;
      box-shadow: 0 6px 18px rgba(245, 158, 11, 0.4);
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
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

    .calendar-grid {
      display: grid;
      grid-template-columns: repeat(7, 1fr);
      gap: 5px;
      margin: 14px 0;
    }
    .calendar-day-header {
      font-size: 10px;
      font-weight: 800;
      color: #94a3b8;
      text-transform: uppercase;
    }
    .calendar-day-cell {
      height: 34px;
      border-radius: 6px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      font-size: 11px;
      font-weight: 800;
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid rgba(255, 255, 255, 0.08);
      position: relative;
    }
    .calendar-day-cell.completed {
      background: rgba(34, 197, 94, 0.25);
      border-color: rgba(34, 197, 94, 0.6);
      color: #86efac;
    }
    .calendar-day-cell.today {
      border: 2px solid #fbbf24;
      box-shadow: 0 0 10px rgba(251, 191, 36, 0.5);
    }
    .calendar-day-cell .check {
      font-size: 9px;
      color: #22c55e;
      position: absolute;
      bottom: 1px;
    }

    .setting-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 10px 0;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      font-size: 13px;
      text-align: left;
    }
    .setting-toggle {
      cursor: pointer;
      width: 44px;
      height: 24px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.2);
      position: relative;
      transition: background-color 0.2s;
    }
    .setting-toggle::after {
      content: '';
      position: absolute;
      top: 2px;
      left: 2px;
      width: 20px;
      height: 20px;
      border-radius: 50%;
      background: #fff;
      transition: transform 0.2s;
    }
    .setting-toggle.active {
      background: #22c55e;
    }
    .setting-toggle.active::after {
      transform: translateX(20px);
    }

    #confetti-canvas {
      position: fixed;
      inset: 0;
      pointer-events: none;
      z-index: 4000;
    }
  </style>
</head>
<body>

  <div id="bg-layer"></div>
  <div id="bg-gradient"></div>
  <div id="screen-flash"></div>
  <canvas id="confetti-canvas"></canvas>
  <div id="targeting-banner">🎯 Açmak istediğin kutucuğa dokun!</div>

  <div id="app-container">

    <!-- Top Navigation Header -->
    <header>
      <div class="header-pill">
        <div class="level-badge">
          <span class="sub-title" id="region-text">KAPADOKYA</span>
          <span class="main-title" id="level-title-text">Bölüm 1</span>
        </div>
      </div>

      <div class="header-actions">
        <button class="btn-header daily-btn" id="btn-open-daily" aria-label="Günlük Bulmaca" title="Günlük Bulmaca">
          <span>📅</span><span id="streak-indicator">🔥 1</span>
        </button>
        <button class="btn-header idiom-btn" id="btn-open-idioms" aria-label="Atasözü ve Deyim Modu" title="Atasözü Modu">
          <span>📜</span><span>Deyim</span>
        </button>
        <div class="header-pill coin-badge" id="btn-coins-info" title="Altın Bakiyesi">
          <span>🪙</span><span id="coins-display">200</span>
        </div>
        <button class="btn-header" id="btn-open-settings" aria-label="Ayarlar ve Ses" title="Ayarlar">
          <span>⚙️</span>
        </button>
      </div>
    </header>

    <!-- Crossword Board Area -->
    <main id="board-area">
      <div id="crossword-grid" role="grid" aria-label="Çapraz Bulmaca Izgarası"></div>
    </main>

    <!-- Bottom Controls & Wheel Section -->
    <section id="bottom-section">

      <!-- Word Preview Pill -->
      <div id="preview-container">
        <div id="word-preview" aria-live="polite">KELİME</div>
      </div>

      <!-- Power-ups Toolbar -->
      <div id="powerups-toolbar">
        <button class="btn-powerup" id="btn-shuffle" title="Harfleri Karıştır" aria-label="Harfleri Karıştır (Ücretsiz)">
          <span class="icon">🔀</span>
          <span class="cost">Ücretsiz</span>
        </button>

        <button class="btn-powerup" id="btn-hint-bulb" title="Rastgele 1 Harf Aç" aria-label="Ampul İpucu: 50 Altın">
          <span class="icon">💡</span>
          <span class="cost">🪙 50</span>
        </button>

        <button class="btn-powerup" id="btn-hint-target" title="Hedef Harfi Seçip Aç" aria-label="Hedefçi Büyüteç: 90 Altın">
          <span class="icon">🎯</span>
          <span class="cost">🪙 90</span>
        </button>

        <button class="btn-powerup" id="btn-hint-lightning" title="3-4 Harf Patlat" aria-label="Şimşek: 140 Altın">
          <span class="icon">⚡</span>
          <span class="cost">🪙 140</span>
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

  </div>

  <!-- Modals -->
  <!-- 1. Cultural Discovery Card Modal -->
  <div class="modal-overlay" id="modal-discovery" role="dialog" aria-modal="true">
    <div class="modal-card">
      <img class="discovery-img" id="discovery-img" src="" alt="Tarihi ve Doğal Mekan">
      <span class="discovery-badge" id="discovery-region">BÖLGE</span>
      <h2 class="discovery-title" id="discovery-title">Mekan Adı</h2>
      <div class="discovery-trivia" id="discovery-trivia">Mekan açıklaması...</div>
      <button class="btn-gold" id="btn-discovery-continue">
        <span>Devam Et</span> ➔
      </button>
    </div>
  </div>

  <!-- 2. Victory Modal with Balanced 2X Bonus -->
  <div class="modal-overlay" id="modal-victory" role="dialog" aria-modal="true">
    <div class="modal-card">
      <div id="victory-stars-display" style="font-size:36px; margin-bottom:10px; filter: drop-shadow(0 0 12px rgba(245, 158, 11, 0.8));">⭐⭐⭐</div>
      <h2 style="font-size:24px; font-weight:900; margin-bottom:4px;">Bölüm Tamamlandı!</h2>
      <p style="color:#94a3b8; font-size:13px; margin-bottom:14px;" id="victory-eval-text">Kusursuz çözüm!</p>

      <div style="background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.4); padding: 10px; border-radius: 12px; font-weight: 900; font-size: 16px; color: #fef08a; margin-bottom: 14px;">
        <span>Kazanılan Ödül:</span>
        <span style="color:#fbbf24;" id="victory-coins-earned">+30 Altın</span>
      </div>

      <button class="btn-gold" id="btn-victory-2x" style="margin-bottom:8px; font-size:14px;">
        <span>🎁 2 Katı Kazan: +60 Altın</span>
      </button>

      <button class="btn-secondary" id="btn-victory-normal">
        Normal Devam (+30 Altın)
      </button>
    </div>
  </div>

  <!-- 3. Daily Challenge & Calendar Modal -->
  <div class="modal-overlay" id="modal-calendar" role="dialog" aria-modal="true">
    <div class="modal-card">
      <h2 style="font-size:20px; font-weight:900; margin-bottom:2px;">📅 Günlük Bulmaca</h2>
      <p style="color:#fef08a; font-weight:800; font-size:13px;" id="calendar-streak-text">🔥 1 Günlük Seri</p>

      <div class="calendar-grid" id="calendar-grid-container"></div>

      <div style="font-size:11.5px; color:#cbd5e1; margin-bottom:12px;" id="daily-status-desc">
        Günün bulmacasında 3 parlayan yıldızı toplayarak serini devam ettir!
      </div>

      <button class="btn-gold" id="btn-play-daily">
        <span>Günün Bulmacasını Oyna</span> 🌟
      </button>

      <button class="btn-secondary" id="btn-share-daily" style="display:none; background: rgba(34, 197, 94, 0.25); border-color: rgba(34, 197, 94, 0.5); color: #86efac;">
        <span>📋 Sonucu Paylaş</span>
      </button>

      <button class="btn-secondary" id="btn-close-calendar">
        Kapat
      </button>
    </div>
  </div>

  <!-- 4. Proverbs & Idioms Mode Modal -->
  <div class="modal-overlay" id="modal-idioms" role="dialog" aria-modal="true">
    <div class="modal-card">
      <span style="font-size:11px; background: rgba(168, 85, 247, 0.25); border: 1px solid rgba(168, 85, 247, 0.6); color: #f3e8ff; padding: 2px 10px; border-radius: 999px; font-weight: 800;">TÜRKÇE ATASÖZÜ & DEYİM</span>
      <h2 style="font-size:18px; font-weight:900; margin:10px 0 6px 0;" id="idiom-proverb-text">"Damlaya damlaya ___ olur."</h2>
      <p style="font-size:12px; color:#cbd5e1; margin-bottom:16px; font-style:italic;" id="idiom-meaning-text">Anlamı yükleniyor...</p>

      <button class="btn-gold" id="btn-start-idiom-puzzle">
        <span>Eksik Kelimeyi Çöz (+25 🪙)</span>
      </button>

      <button class="btn-secondary" id="btn-close-idioms">
        Vazgeç
      </button>
    </div>
  </div>

  <!-- 5. Bonus Chest Modal -->
  <div class="modal-overlay" id="modal-bonus-chest" role="dialog" aria-modal="true">
    <div class="modal-card">
      <div style="font-size:36px; margin-bottom:6px;">🎁</div>
      <h2 style="font-size:20px; font-weight:900; margin-bottom:4px;">Kelime Sandığı</h2>
      <p style="color:#cbd5e1; font-size:12.5px; line-height:1.4; margin-bottom:14px;">
        Çapraz bulmacada yer almayan ama Türkçede geçerli olan kelimeleri buldukça bu sandık dolar. Her 5 kelimede bir <strong>+35 Altın</strong> kazanırsın!
      </p>

      <div style="background: rgba(15, 23, 42, 0.7); padding: 10px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 14px;">
        <div style="font-size:13px; font-weight:800; color:#fef08a; margin-bottom:6px;">
          İlerleme: <span id="modal-chest-progress">0/5</span>
        </div>
        <div style="font-size:11.5px; color:#94a3b8;" id="modal-chest-words-list">
          Bu bölümde henüz bonus kelime bulunmadı.
        </div>
      </div>

      <button class="btn-gold" id="btn-close-bonus-chest">
        Harika, Anladım!
      </button>
    </div>
  </div>

  <!-- 6. Accessibility & Settings Modal -->
  <div class="modal-overlay" id="modal-settings" role="dialog" aria-modal="true">
    <div class="modal-card">
      <h2 style="font-size:20px; font-weight:900; margin-bottom:14px;">⚙️ Ayarlar ve Erişilebilirlik</h2>

      <div class="setting-row">
        <span>🔊 Ses Efektleri</span>
        <div class="setting-toggle active" id="toggle-sound"></div>
      </div>

      <div class="setting-row">
        <span>📳 Titreşim (Haptic)</span>
        <div class="setting-toggle active" id="toggle-haptic"></div>
      </div>

      <div class="setting-row">
        <span>♿ Disleksi Dostu Yazı Tipi</span>
        <div class="setting-toggle" id="toggle-dyslexia"></div>
      </div>

      <div class="setting-row">
        <span>🎨 Yüksek Kontrast Modu</span>
        <div class="setting-toggle" id="toggle-contrast"></div>
      </div>

      <div class="setting-row">
        <span>⚡ Hareketi Azalt (Reduced Motion)</span>
        <div class="setting-toggle" id="toggle-motion"></div>
      </div>

      <button class="btn-secondary" id="btn-open-about-from-settings" style="margin-top:12px; background: rgba(56, 189, 248, 0.15); border-color: rgba(56, 189, 248, 0.4); color: #7dd3fc;">
        <span>ℹ️ Oyun Hakkında, Kaynaklar ve KVKK</span>
      </button>

      <button class="btn-gold" id="btn-close-settings" style="margin-top:12px;">
        Tamam
      </button>
    </div>
  </div>

  <!-- 7. About & Credits Modal -->
  <div class="modal-overlay" id="modal-about" role="dialog" aria-modal="true">
    <div class="modal-card" style="text-align: left;">
      <h2 style="font-size:20px; font-weight:900; margin-bottom:4px; text-align:center;">Kelime Harikaları</h2>
      <p style="font-size:11.5px; color:#94a3b8; text-align:center; margin-bottom:14px;">Sürüm 2.0.0 • Anadolu & Dünya Kültürel Mirası</p>

      <div style="font-size:12px; color:#cbd5e1; line-height:1.5; margin-bottom:12px;">
        <strong>Kültürel Görseller ve Lisanslar:</strong>
        <p style="margin-top:4px;">Oyundaki tüm tarihi mekan görselleri Wikimedia Commons üzerinden Creative Commons (CC BY-SA / CC0) lisanslarıyla temin edilmiştir.</p>
        <ul style="margin: 6px 0 0 16px; font-size:11px; color:#94a3b8;">
          <li>Kapadokya: Yusuf Kaya (CC BY-SA 4.0)</li>
          <li>Pamukkale: Antoine Taveneaux (CC BY-SA 3.0)</li>
          <li>Galata Kulesi: Arild Vågen (CC BY-SA 4.0)</li>
          <li>Efes Celsus: Benh LIEU SONG (CC BY-SA 3.0)</li>
          <li>Nemrut Dağı: Bernard Gagnon (CC BY-SA 3.0)</li>
          <li>Göbeklitepe: Teomancimit (CC BY-SA 3.0)</li>
        </ul>
      </div>

      <div style="font-size:12px; color:#cbd5e1; line-height:1.5; margin-bottom:12px;">
        <strong>Sözlük & İmla:</strong>
        <p style="margin-top:4px;">Kelimeler ve atasözleri Türk Dil Kurumu (TDK) güncel yazım kılavuzu esas alınarak derlenmiştir.</p>
      </div>

      <div style="font-size:11.5px; color:#86efac; background:rgba(34, 197, 94, 0.15); padding:8px; border-radius:8px; border:1px solid rgba(34, 197, 94, 0.4); margin-bottom:14px;">
        🛡️ <strong>Gizlilik & KVKK:</strong> Kelime Harikaları hiçbir kişisel veri toplamaz, çerez kullanmaz. Tüm oyun kaydınız yalnızca cihazınızda saklanır.
      </div>

      <button class="btn-gold" id="btn-close-about">
        Kapat
      </button>
    </div>
  </div>

  <!-- 8. Insufficient Coins Modal -->
  <div class="modal-overlay" id="modal-no-coins" role="dialog" aria-modal="true">
    <div class="modal-card">
      <div style="font-size:36px; margin-bottom:6px;">🪙</div>
      <h2 style="font-size:20px; font-weight:900; margin-bottom:4px;">Yetersiz Altın</h2>
      <p style="color:#cbd5e1; font-size:12.5px; margin-bottom:16px;">
        Bu gücü kullanmak için altının yetersiz. Bugünkü ücretsiz ipucunu kullanabilir veya bonus kelimeler bularak altın kazanabilirsin!
      </p>

      <button class="btn-gold" id="btn-claim-free-hint" style="margin-bottom:8px;">
        <span>🎁 Bugünkü Ücretsiz İpucu (1 Adet)</span>
      </button>

      <button class="btn-secondary" id="btn-close-no-coins">
        Vazgeç
      </button>
    </div>
  </div>

  <!-- Script Engine Injection -->
  <script>
    __JS_ENGINE_INJECTION__
  </script>
</body>
</html>
'''

# Let's read JS engine from compile_v2_safe.py
with open("compile_v2_safe.py", "r", encoding="utf-8") as f:
    safe_code = f.read()

start_marker = "js_engine_template = code[start_js:end_js]"
# We can extract js_engine directly from compile_v2.py
with open("compile_v2.py", "r", encoding="utf-8") as f:
    orig_code = f.read()

start_js = orig_code.find("JS_ENGINE = f'''") + len("JS_ENGINE = f'''")
end_js = orig_code.rfind("'''\n\nfull_html =")
raw_js = orig_code[start_js:end_js].replace("{{", "{").replace("}}", "}")

raw_js = raw_js.replace("{json.dumps(credits_data, ensure_ascii=False)}", json.dumps(credits_data, ensure_ascii=False))
raw_js = raw_js.replace("{json.dumps(idioms_data, ensure_ascii=False)}", json.dumps(idioms_data, ensure_ascii=False))
raw_js = raw_js.replace("{json.dumps(levels_data, ensure_ascii=False)}", json.dumps(levels_data, ensure_ascii=False))

# Safe guard: add click handler for btn-open-about-from-settings
about_fix = """
      document.getElementById('btn-open-about-from-settings').addEventListener('click', () => {
        this.dom.modalSettings.classList.remove('active');
        this.dom.modalAbout.classList.add('active');
      });
"""
raw_js = raw_js.replace("document.getElementById('btn-close-about').addEventListener", about_fix + "\n      document.getElementById('btn-close-about').addEventListener")

full_html = HTML_TEMPLATE.replace("__JS_ENGINE_INJECTION__", raw_js)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(full_html)

print("SUCCESS: index.html re-compiled cleanly! Size:", len(full_html))
