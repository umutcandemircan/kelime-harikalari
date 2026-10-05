# -*- coding: utf-8 -*-
"""
Full Compiler for Kelime Harikaları v2.0.0
Generates index.html with embedded configuration, verified 100 levels, 150 idioms, and cultural credits.
"""
import json

with open("credits.json", "r", encoding="utf-8") as f:
    credits_data = json.load(f)

with open("idioms.json", "r", encoding="utf-8") as f:
    idioms_data = json.load(f)

with open("levels_100.json", "r", encoding="utf-8") as f:
    levels_data = json.load(f)

HTML_CONTENT = r'''<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>Kelime Harikaları - Türkçe Çapraz Bulmaca ve Kelime Oyunu</title>
  <meta name="description" content="Anadolu'nun ve dünyanın kültürel harikalarını keşfederek Türkçe kelime dağarcığını geliştireceğin, adil ve akıcı çapraz bulmaca oyunu.">
  <meta name="theme-color" content="#020617">
  
  <!-- Open Graph / Sosyal Paylaşım -->
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
      
      --wheel-size: min(220px, 32vh, 65vw);
      --node-size: 50px;
    }

    /* Accessibility: Dyslexia Mode */
    body.dyslexia-font {
      --font-main: var(--font-dyslexia);
      letter-spacing: 0.8px;
    }

    /* Accessibility: High Contrast Mode */
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
      background: rgba(0, 0, 0, 0.85) !important;
    }
    body.high-contrast .cell-back {
      border: 3px solid #ffff00 !important;
      background: #ffffff !important;
      color: #000000 !important;
    }

    /* Accessibility: Reduced Motion */
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

    /* Dynamic Background with Smooth Crossfade */
    #bg-layer {
      position: absolute;
      inset: 0;
      background-size: cover;
      background-position: center;
      filter: brightness(0.60) saturate(1.2);
      transition: background-image 0.7s cubic-bezier(0.4, 0, 0.2, 1);
      z-index: 0;
    }

    #bg-gradient {
      position: absolute;
      inset: 0;
      background: radial-gradient(circle at 50% 30%, rgba(15, 23, 42, 0.25) 0%, rgba(2, 6, 23, 0.90) 100%);
      z-index: 1;
    }

    /* Master App Container */
    #app-container {
      position: relative;
      z-index: 2;
      width: 100%;
      max-width: 480px;
      height: 100%;
      height: 100dvh;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: max(8px, env(safe-area-inset-top)) 10px max(10px, env(safe-area-inset-bottom)) 10px;
    }

    /* Top Navigation Bar */
    header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 48px;
      gap: 6px;
      flex-shrink: 0;
    }

    .header-pill {
      display: flex;
      align-items: center;
      gap: 5px;
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      padding: 5px 10px;
      border-radius: 999px;
      border: 1px solid rgba(255, 255, 255, 0.15);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
      font-weight: 700;
      font-size: 12px;
    }

    .level-badge {
      display: flex;
      flex-direction: column;
      line-height: 1.1;
    }
    .level-badge .sub-title {
      font-size: 9px;
      color: #94a3b8;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .level-badge .main-title {
      font-size: 13px;
      color: #f8fafc;
      font-weight: 800;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 100px;
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 4px;
    }

    .btn-header {
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 3px;
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 999px;
      padding: 5px 8px;
      color: #fff;
      font-size: 11px;
      font-weight: 800;
      min-height: 32px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.25);
      transition: transform 0.15s, background-color 0.15s;
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

    /* Grid Cell */
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

    /* Star Badge on Daily Challenge Cell */
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

    /* Targeting Instruction Banner */
    #targeting-banner {
      display: none;
      position: absolute;
      top: 56px;
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
    @keyframes bounceBanner {
      0% { transform: translate(-50%, 0); }
      100% { transform: translate(-50%, -3px); }
    }

    /* Bottom Controls */
    #bottom-section {
      display: flex;
      flex-direction: column;
      align-items: center;
      flex-shrink: 0;
    }

    /* Word Preview Pill */
    #preview-container {
      height: 34px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 2px;
    }

    #word-preview {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-width: 70px;
      height: 32px;
      padding: 0 16px;
      border-radius: 999px;
      background: rgba(15, 23, 42, 0.88);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border: 1.5px solid rgba(255, 255, 255, 0.2);
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4);
      font-size: 16px;
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
      justify-content: space-between;
      width: 100%;
      max-width: 360px;
      margin: 0 auto 4px auto;
      padding: 0 6px;
      gap: 6px;
    }

    .btn-powerup {
      cursor: pointer;
      position: relative;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      flex: 1;
      max-width: 54px;
      height: 48px;
      border-radius: 14px;
      background: linear-gradient(135deg, rgba(30, 41, 59, 0.88), rgba(15, 23, 42, 0.95));
      backdrop-filter: blur(10px);
      border: 1.5px solid rgba(255, 255, 255, 0.18);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
      color: #fff;
      transition: transform 0.15s, border-color 0.2s, box-shadow 0.2s;
    }
    .btn-powerup:active {
      transform: scale(0.92);
    }
    .btn-powerup .icon {
      font-size: 17px;
      line-height: 1;
    }
    .btn-powerup .cost {
      font-size: 9px;
      font-weight: 800;
      color: #fef08a;
      margin-top: 2px;
      display: flex;
      align-items: center;
      gap: 1px;
    }
    .btn-powerup.active-tool {
      border-color: #38bdf8;
      box-shadow: 0 0 14px rgba(56, 189, 248, 0.8);
      background: rgba(14, 165, 233, 0.35);
    }

    /* Bonus Chest Badge */
    .bonus-chest-btn {
      cursor: pointer;
      position: relative;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      flex: 1;
      max-width: 54px;
      height: 48px;
      border-radius: 14px;
      background: linear-gradient(135deg, rgba(168, 85, 247, 0.35), rgba(126, 34, 206, 0.65));
      border: 1.5px solid rgba(216, 180, 254, 0.4);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
      color: #fff;
      transition: transform 0.15s;
    }
    .bonus-chest-btn:active {
      transform: scale(0.92);
    }
    .bonus-chest-btn .counter {
      font-size: 9px;
      font-weight: 800;
      color: #f3e8ff;
      margin-top: 2px;
    }

    /* Wheel Container */
    #wheel-wrapper {
      position: relative;
      width: var(--wheel-size);
      height: var(--wheel-size);
      margin: 0 auto 6px auto;
      display: flex;
      align-items: center;
      justify-content: center;
      touch-action: none; /* Crucial: isolates gestures to wheel without disabling page zoom */
    }

    #wheel-canvas-container {
      position: absolute;
      inset: 0;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.85) 100%);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 2px solid rgba(255, 255, 255, 0.18);
      box-shadow: 0 8px 26px rgba(0, 0, 0, 0.5), inset 0 0 18px rgba(255, 255, 255, 0.06);
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

    /* Wheel Letter Nodes */
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
      font-size: 22px;
      font-weight: 900;
      box-shadow: 0 5px 12px rgba(0, 0, 0, 0.3), inset 0 2px 4px rgba(255, 255, 255, 0.9);
      border: 2px solid rgba(255, 255, 255, 0.8);
      z-index: 20;
      transition: transform 0.18s cubic-bezier(0.34, 1.56, 0.64, 1), background 0.18s, box-shadow 0.18s;
      transform: translate(-50%, -50%);
    }

    .wheel-node.selected {
      background: linear-gradient(135deg, #fbbf24, #f59e0b);
      color: #ffffff;
      transform: translate(-50%, -50%) scale(1.16);
      box-shadow: 0 0 20px rgba(245, 158, 11, 0.9), inset 0 2px 4px rgba(255, 255, 255, 0.5);
      border-color: #fef08a;
    }

    /* Screen Flash */
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

    /* Spark & Star Projectiles */
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

    /* Floating Toast */
    .floating-toast {
      position: fixed;
      bottom: 220px;
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

    /* Calendar Grid */
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

    /* Settings Switch Row */
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

    /* Confetti Canvas */
    #confetti-canvas {
      position: fixed;
      inset: 0;
      pointer-events: none;
      z-index: 4000;
    }
  </style>
</head>
<body>

  <!-- Dynamic Backdrop -->
  <div id="bg-layer"></div>
  <div id="bg-gradient"></div>

  <!-- Screen Flash for Thunder -->
  <div id="screen-flash"></div>

  <!-- Confetti Canvas -->
  <canvas id="confetti-canvas"></canvas>

  <!-- Targeting Mode Banner -->
  <div id="targeting-banner">🎯 Açmak istediğin kutucuğa dokun!</div>

  <!-- App Wrapper -->
  <div id="app-container">

    <!-- Top Header -->
    <header>
      <div class="header-pill">
        <div class="level-badge">
          <span class="sub-title" id="region-text">KAPADOKYA</span>
          <span class="main-title" id="level-title-text">Bölüm 1</span>
        </div>
      </div>

      <div class="header-actions">
        <!-- Daily Challenge Button -->
        <button class="btn-header daily-btn" id="btn-open-daily" aria-label="Günlük Bulmaca">
          <span>📅</span> Günlük <span id="streak-indicator">🔥 1</span>
        </button>

        <!-- Proverbs Mode Button -->
        <button class="btn-header idiom-btn" id="btn-open-idioms" aria-label="Atasözü ve Deyim Modu">
          <span>📜</span> Deyim
        </button>

        <!-- Settings Button -->
        <button class="btn-header" id="btn-open-settings" aria-label="Ayarlar">
          <span>⚙️</span>
        </button>

        <!-- About Button -->
        <button class="btn-header" id="btn-open-about" aria-label="Hakkında ve Kaynaklar">
          <span>ℹ️</span>
        </button>

        <!-- Sound Toggle -->
        <button class="btn-header" id="btn-sound-toggle" aria-label="Sesi Aç veya Kapat">
          <span id="sound-icon">🔊</span>
        </button>

        <!-- Coins Badge -->
        <div class="header-pill coin-badge" id="btn-coins-info" title="Altın Bakiyesi">
          <span>🪙</span> <span id="coins-display">200</span>
        </div>
      </div>
    </header>

    <!-- Crossword Grid Board -->
    <main id="board-area">
      <div id="crossword-grid" role="grid" aria-label="Çapraz Bulmaca Izgarası"></div>
    </main>

    <!-- Bottom Controls & Wheel Section -->
    <section id="bottom-section">

      <!-- Current Word Preview Pill -->
      <div id="preview-container">
        <div id="word-preview" aria-live="polite">KELİME</div>
      </div>

      <!-- Power-ups Toolbar -->
      <div id="powerups-toolbar">
        <!-- Shuffle -->
        <button class="btn-powerup" id="btn-shuffle" title="Harfleri Karıştır" aria-label="Harfleri Karıştır (Ücretsiz)">
          <span class="icon">🔀</span>
          <span class="cost">Ücretsiz</span>
        </button>

        <!-- Bulb Hint (50) -->
        <button class="btn-powerup" id="btn-hint-bulb" title="Rastgele 1 Harf Aç" aria-label="Ampul İpucu: 50 Altın">
          <span class="icon">💡</span>
          <span class="cost">🪙 50</span>
        </button>

        <!-- Target Magnifier (90) -->
        <button class="btn-powerup" id="btn-hint-target" title="Hedef Harfi Seçip Aç" aria-label="Hedefçi Büyüteç: 90 Altın">
          <span class="icon">🎯</span>
          <span class="cost">🪙 90</span>
        </button>

        <!-- Lightning Fireworks (140) -->
        <button class="btn-powerup" id="btn-hint-lightning" title="3-4 Harf Patlat" aria-label="Şimşek: 140 Altın">
          <span class="icon">⚡</span>
          <span class="cost">🪙 140</span>
        </button>

        <!-- Bonus Chest Button -->
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

  <!-- ==================== MODALS ==================== -->

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

      <!-- 2X Bonus Button -->
      <button class="btn-gold" id="btn-victory-2x" style="margin-bottom:8px; font-size:14px;">
        <span>🎁 2 Katı Kazan: +60 Altın</span>
      </button>

      <!-- Standard Continue -->
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

      <!-- Calendar Month Days -->
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

      <button class="btn-gold" id="btn-close-settings" style="margin-top:16px;">
        Tamam
      </button>
    </div>
  </div>

  <!-- 7. About & Credits Modal -->
  <div class="modal-overlay" id="modal-about" role="dialog" aria-modal="true">
    <div class="modal-card" style="text-align: left;">
      <h2 style="font-size:20px; font-weight:900; margin-bottom:6px; text-align:center;">Kelime Harikaları</h2>
      <p style="font-size:11.5px; color:#94a3b8; text-align:center; margin-bottom:14px;">Sürüm 2.0.0 • Anadolu & Dünya Kültürel Mirası</p>

      <div style="font-size:12px; color:#cbd5e1; line-height:1.5; margin-bottom:14px;">
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

      <div style="font-size:12px; color:#cbd5e1; line-height:1.5; margin-bottom:14px;">
        <strong>Sözlük & İmla:</strong>
        <p style="margin-top:4px;">Kelimeler ve atasözleri Türk Dil Kurumu (TDK) güncel yazım kılavuzu esas alınarak derlenmiştir.</p>
      </div>

      <div style="font-size:11.5px; color:#86efac; background:rgba(34, 197, 94, 0.15); padding:8px; border-radius:8px; border:1px solid rgba(34, 197, 94, 0.4); margin-bottom:16px;">
        🛡️ <strong>Gizlilik & KVKK:</strong> Kelime Harikaları hiçbir kişisel veri toplamaz, çerez kullanmaz. Tüm oyun kaydınız yalnızca cihazınızda güvenle tutulur.
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

  <!-- ==================== LOGIC ENGINE ==================== -->
  <script>
    /* GAME ENGINE v2.0.0 INJECTION */
    __JS_ENGINE_INJECTION__
  </script>
</body>
</html>
'''

# Let's assemble the JavaScript Engine
JS_ENGINE = f'''
  // Injected Data Packages
  const CREDITS_DATA = {json.dumps(credits_data, ensure_ascii=False)};
  const IDIOMS_DATA = {json.dumps(idioms_data, ensure_ascii=False)};
  const LEVELS_DATA = {json.dumps(levels_data, ensure_ascii=False)};

  /* ==========================================================================
     1. STORAGE SERVICE (FAIL-SAFE, VERSIONED, MIGRATION SUPPORT)
     ========================================================================== */
  class StorageService {{
    constructor() {
      this.prefix = 'kh_';
      this.memoryFallback = {};
      this.init();
    }

    init() {
      // Migrate legacy 'wow_' keys to 'kh_' keys if they exist
      try {
        const legacyKeys = ['coins', 'level_idx', 'streak', 'daily_dates', 'stars', 'bonus_chest', 'sound_muted'];
        legacyKeys.forEach(k => {
          const oldVal = localStorage.getItem('wow_' + k);
          if (oldVal !== null && localStorage.getItem(this.prefix + k) === null) {
            localStorage.setItem(this.prefix + k, oldVal);
          }
        });
      } catch (e) {
        console.warn('Storage migration fallback active');
      }
    }

    get(key, defaultValue) {
      try {
        const val = localStorage.getItem(this.prefix + key);
        if (val === null || val === undefined) return defaultValue;
        return JSON.parse(val);
      } catch (e) {
        return this.memoryFallback[key] !== undefined ? this.memoryFallback[key] : defaultValue;
      }
    }

    set(key, value) {
      try {
        localStorage.setItem(this.prefix + key, JSON.stringify(value));
      } catch (e) {
        this.memoryFallback[key] = value;
      }
    }
  }

  /* ==========================================================================
     2. PROCEDURAL WEB AUDIO SYNTHESIZER
     ========================================================================== */
  class SoundEngine {
    constructor(storage) {
      this.storage = storage;
      this.ctx = null;
      this.muted = this.storage.get('sound_muted', false);
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

    toggleMute() {
      this.muted = !this.muted;
      this.storage.set('sound_muted', this.muted);
      return this.muted;
    }

    playLetterNote(index) {
      if (this.muted) return;
      this.init();
      if (!this.ctx) return;
      const freqs = [261.63, 293.66, 329.63, 392.00, 440.00, 523.25, 659.25, 783.99];
      const freq = freqs[Math.min(index, freqs.length - 1)];

      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
      gain.gain.setValueAtTime(0.2, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.22);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + 0.22);
    }

    playWordSuccess() {
      if (this.muted) return;
      this.init();
      if (!this.ctx) return;
      const notes = [523.25, 659.25, 783.99, 1046.50];
      notes.forEach((freq, idx) => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'triangle';
        const startTime = this.ctx.currentTime + idx * 0.06;
        osc.frequency.setValueAtTime(freq, startTime);
        gain.gain.setValueAtTime(0.2, startTime);
        gain.gain.exponentialRampToValueAtTime(0.001, startTime + 0.4);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(startTime);
        osc.stop(startTime + 0.4);
      });
    }

    playErrorBuzz() {
      if (this.muted) return;
      this.init();
      if (!this.ctx) return;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(130, this.ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(75, this.ctx.currentTime + 0.2);
      gain.gain.setValueAtTime(0.18, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.2);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + 0.2);
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
        gain.gain.setValueAtTime(0.22, startTime);
        gain.gain.exponentialRampToValueAtTime(0.001, startTime + 0.45);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(startTime);
        osc.stop(startTime + 0.45);
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
      osc.frequency.exponentialRampToValueAtTime(25, this.ctx.currentTime + 0.55);
      gain.gain.setValueAtTime(0.3, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.55);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + 0.55);
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

    playFanfare() {
      if (this.muted) return;
      this.init();
      if (!this.ctx) return;
      const motif = [
        {{ f: 523.25, t: 0.0, d: 0.14 }},
        {{ f: 659.25, t: 0.14, d: 0.14 }},
        {{ f: 783.99, t: 0.28, d: 0.18 }},
        {{ f: 1046.50, t: 0.46, d: 0.55 }}
      ];
      motif.forEach(m => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'triangle';
        const startTime = this.ctx.currentTime + m.t;
        osc.frequency.setValueAtTime(m.f, startTime);
        gain.gain.setValueAtTime(0.22, startTime);
        gain.gain.exponentialRampToValueAtTime(0.001, startTime + m.d);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(startTime);
        osc.stop(startTime + m.d);
      });
    }
  }

  /* ==========================================================================
     3. TURKISH LANGUAGE & HELPER UTILITIES
     ========================================================================== */
  const Turkish = {{
    toUpper(str) {{
      return (str || '').toLocaleUpperCase('tr-TR');
    }},
    toLower(str) {{
      return (str || '').toLocaleLowerCase('tr-TR');
    }},
    // Istanbul Date YYYY-MM-DD
    getIstanbulDateString(d = new Date()) {{
      try {{
        const formatter = new Intl.DateTimeFormat('en-CA', {{
          timeZone: 'Europe/Istanbul',
          year: 'numeric',
          month: '2-digit',
          day: '2-digit'
        }});
        return formatter.format(d);
      }} catch (e) {{
        return d.toISOString().split('T')[0];
      }}
    }},
    getYesterdayIstanbulString() {{
      const d = new Date();
      d.setDate(d.getDate() - 1);
      return this.getIstanbulDateString(d);
    }},
    // Turkish Suffix Pattern Matching (Kök-Ek engine)
    isRootSuffixPair(base, target) {{
      if (!target.startsWith(base) || target === base) return false;
      const suffix = target.slice(base.length);
      const commonSuffixes = ['LER', 'LAR', 'Cİ', 'CÜ', 'ÇI', 'Çİ', 'ÇU', 'ÇÜ', 'LİK', 'LUK', 'LÜK', 'Lİ', 'LI', 'LU', 'LÜ', 'SİZ', 'SIZ', 'SUZ', 'SÜZ', 'DE', 'DA', 'DEN', 'DAN', 'E', 'A', 'İ', 'I', 'İM', 'İN', 'İK'];
      return commonSuffixes.includes(suffix);
    }}
  }};

  /* ==========================================================================
     4. HONEST AD PROVIDER (NO DECEPTIVE FAKE ADS IN PROD)
     ========================================================================== */
  class AdProvider {{
    constructor() {{
      const params = new URLSearchParams(window.location.search);
      this.isDevMode = params.get('dev') === '1';
    }}

    async showRewarded(reason = "Ödüllü Reklam") {{
      if (this.isDevMode) {{
        return new Promise((resolve) => {{
          const banner = document.createElement('div');
          banner.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.92);color:#fff;z-index:99999;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:20px;';
          banner.innerHTML = `
            <div style="font-size:44px;margin-bottom:12px;">🎮</div>
            <h2 style="font-size:22px;margin-bottom:8px;">TEST REKLAMI (Geliştirici Modu)</h2>
            <p style="color:#94a3b8;font-size:13px;margin-bottom:18px;">Sebep: ${reason}</p>
            <div id="test-ad-countdown" style="font-size:18px;font-weight:900;color:#fbbf24;">4s...</div>
          `;
          document.body.appendChild(banner);

          let sec = 4;
          const interval = setInterval(() => {{
            sec--;
            const timer = document.getElementById('test-ad-countdown');
            if (timer) timer.textContent = `${sec}s...`;
            if (sec <= 0) {{
              clearInterval(interval);
              banner.remove();
              resolve(true);
            }}
          }}, 1000);
        }});
      }}
      // In production mode, grant reward directly without showing deceptive fake video countdowns!
      return true;
    }}
  }}

  /* ==========================================================================
     5. MASTER GAME CONTROLLER
     ========================================================================== */
  class KelimeHarikalariGame {{
    constructor() {{
      this.storage = new StorageService();
      this.sound = new SoundEngine(this.storage);
      this.adProvider = new AdProvider();

      // State
      this.coins = this.storage.get('coins', 200);
      this.stars = this.storage.get('stars', 0);
      this.levelIdx = this.storage.get('level_idx', 0);
      this.streak = this.storage.get('streak', 1);
      this.completedDailyDates = this.storage.get('daily_dates', []);
      this.bonusChestCount = this.storage.get('bonus_chest', 0);

      // Settings
      this.hapticEnabled = this.storage.get('haptic_enabled', true);
      this.dyslexiaFont = this.storage.get('dyslexia_font', false);
      this.highContrast = this.storage.get('high_contrast', false);
      this.reducedMotion = this.storage.get('reduced_motion', false);

      // Runtime level tracking
      this.currentLevel = null;
      this.isDailyMode = false;
      this.isIdiomMode = false;
      this.isTargetingMode = false;
      this.levelRewardClaimed = false;
      this.levelErrorCount = 0;
      this.levelHintsUsed = 0;

      this.unlockedWordIds = new Set();
      this.revealedCellKeys = new Set();
      this.foundBonusWords = new Set();
      this.dailyStarKeys = new Set();
      this.dailyStarsCollected = new Set();

      // Wheel touch geometry
      this.isDragging = false;
      this.selectedNodeIndices = [];
      this.currentLetters = [];
      this.wheelNodePositions = [];
      this.currentWheelLetters = [];

      this.initDom();
      this.applySettings();
      this.initEvents();
      this.updateTopbar();
      this.loadLevel(this.levelIdx);

      // Register PWA Service Worker
      if ('serviceWorker' in navigator) {{
        window.addEventListener('load', () => {{
          navigator.serviceWorker.register('./sw.js').catch(() => {{}});
        }});
      }}
    }}

    initDom() {{
      this.dom = {{
        bgLayer: document.getElementById('bg-layer'),
        regionText: document.getElementById('region-text'),
        levelTitleText: document.getElementById('level-title-text'),
        streakIndicator: document.getElementById('streak-indicator'),
        soundIcon: document.getElementById('sound-icon'),
        coinsDisplay: document.getElementById('coins-display'),
        crosswordGrid: document.getElementById('crossword-grid'),
        wordPreview: document.getElementById('word-preview'),
        wheelWrapper: document.getElementById('wheel-wrapper'),
        wheelNodesContainer: document.getElementById('wheel-nodes-container'),
        connectionLine: document.getElementById('connection-line'),
        targetingBanner: document.getElementById('targeting-banner'),
        bonusCounter: document.getElementById('bonus-counter'),
        screenFlash: document.getElementById('screen-flash'),
        confettiCanvas: document.getElementById('confetti-canvas'),
        // Modals
        modalDiscovery: document.getElementById('modal-discovery'),
        discoveryImg: document.getElementById('discovery-img'),
        discoveryRegion: document.getElementById('discovery-region'),
        discoveryTitle: document.getElementById('discovery-title'),
        discoveryTrivia: document.getElementById('discovery-trivia'),
        modalVictory: document.getElementById('modal-victory'),
        victoryStarsDisplay: document.getElementById('victory-stars-display'),
        victoryEvalText: document.getElementById('victory-eval-text'),
        victoryCoinsEarned: document.getElementById('victory-coins-earned'),
        modalCalendar: document.getElementById('modal-calendar'),
        calendarStreakText: document.getElementById('calendar-streak-text'),
        calendarGridContainer: document.getElementById('calendar-grid-container'),
        btnShareDaily: document.getElementById('btn-share-daily'),
        modalIdioms: document.getElementById('modal-idioms'),
        idiomProverbText: document.getElementById('idiom-proverb-text'),
        idiomMeaningText: document.getElementById('idiom-meaning-text'),
        modalBonusChest: document.getElementById('modal-bonus-chest'),
        modalChestProgress: document.getElementById('modal-chest-progress'),
        modalChestWordsList: document.getElementById('modal-chest-words-list'),
        modalSettings: document.getElementById('modal-settings'),
        modalAbout: document.getElementById('modal-about'),
        modalNoCoins: document.getElementById('modal-no-coins')
      }};

      this.ctxConfetti = this.dom.confettiCanvas.getContext('2d');
      this.confettiParticles = [];
      this.confettiAnimId = null;
    }}

    applySettings() {{
      document.body.classList.toggle('dyslexia-font', this.dyslexiaFont);
      document.body.classList.toggle('high-contrast', this.highContrast);
      if (this.reducedMotion) {{
        document.body.classList.add('reduced-motion');
      }}

      // Toggle buttons
      document.getElementById('toggle-sound').classList.toggle('active', !this.sound.muted);
      document.getElementById('toggle-haptic').classList.toggle('active', this.hapticEnabled);
      document.getElementById('toggle-dyslexia').classList.toggle('active', this.dyslexiaFont);
      document.getElementById('toggle-contrast').classList.toggle('active', this.highContrast);
      document.getElementById('toggle-motion').classList.toggle('active', this.reducedMotion);
    }}

    vibrate(pattern = 15) {{
      if (this.hapticEnabled && 'vibrate' in navigator) {{
        try {{ navigator.vibrate(pattern); }} catch (e) {{}}
      }}
    }}

    updateTopbar() {{
      this.dom.coinsDisplay.textContent = this.coins;
      this.dom.streakIndicator.textContent = `🔥 ${this.streak}`;
      this.dom.bonusCounter.textContent = `${this.bonusChestCount}/5`;
      this.dom.soundIcon.textContent = this.sound.muted ? '🔇' : '🔊';
    }}

    addCoins(amount) {{
      this.coins = Math.max(0, this.coins + amount);
      this.storage.set('coins', this.coins);
      this.sound.playCoinShower();
      this.updateTopbar();
    }}

    showToast(message) {{
      const toast = document.createElement('div');
      toast.className = 'floating-toast';
      toast.textContent = message;
      document.body.appendChild(toast);
      setTimeout(() => toast.remove(), 1500);
    }}

    /* ---------------- Events Setup ---------------- */
    initEvents() {{
      // Sound Toggle
      document.getElementById('btn-sound-toggle').addEventListener('click', () => {{
        this.sound.init();
        const isMuted = this.sound.toggleMute();
        this.dom.soundIcon.textContent = isMuted ? '🔇' : '🔊';
        document.getElementById('toggle-sound').classList.toggle('active', !isMuted);
      }});

      // Topbar Modals
      document.getElementById('btn-open-daily').addEventListener('click', () => this.openCalendarModal());
      document.getElementById('btn-open-idioms').addEventListener('click', () => this.openIdiomsModal());
      document.getElementById('btn-open-settings').addEventListener('click', () => this.openSettingsModal());
      document.getElementById('btn-open-about').addEventListener('click', () => {{
        this.dom.modalAbout.classList.add('active');
      }});
      document.getElementById('btn-close-about').addEventListener('click', () => {{
        this.dom.modalAbout.classList.remove('active');
      }});

      // Power-up Buttons
      document.getElementById('btn-shuffle').addEventListener('click', () => this.handleShuffle());
      document.getElementById('btn-hint-bulb').addEventListener('click', () => this.handleBulbHint());
      document.getElementById('btn-hint-target').addEventListener('click', () => this.handleTargetMagnifier());
      document.getElementById('btn-hint-lightning').addEventListener('click', () => this.handleLightning());
      document.getElementById('btn-bonus-chest').addEventListener('click', () => this.openBonusChestModal());
      document.getElementById('btn-close-bonus-chest').addEventListener('click', () => {{
        this.dom.modalBonusChest.classList.remove('active');
      }});

      // Discovery & Victory
      document.getElementById('btn-discovery-continue').addEventListener('click', () => {{
        this.dom.modalDiscovery.classList.remove('active');
        this.openVictoryModal();
      }});

      document.getElementById('btn-victory-normal').addEventListener('click', () => {{
        if (this.levelRewardClaimed) return;
        this.levelRewardClaimed = true;
        this.dom.modalVictory.classList.remove('active');
        this.addCoins(30);
        this.proceedToNextLevel();
      }});

      document.getElementById('btn-victory-2x').addEventListener('click', async () => {{
        if (this.levelRewardClaimed) return;
        this.levelRewardClaimed = true;
        this.dom.modalVictory.classList.remove('active');
        await this.adProvider.showRewarded("2X Bölüm Zafer Bonusu");
        this.addCoins(60);
        this.proceedToNextLevel();
      }});

      // Calendar Play & Share
      document.getElementById('btn-close-calendar').addEventListener('click', () => {{
        this.dom.modalCalendar.classList.remove('active');
      }});
      document.getElementById('btn-play-daily').addEventListener('click', () => {{
        this.dom.modalCalendar.classList.remove('active');
        this.startDailyChallenge();
      }});
      document.getElementById('btn-share-daily').addEventListener('click', () => this.shareDailyResult());

      // Idiom Game
      document.getElementById('btn-close-idioms').addEventListener('click', () => {{
        this.dom.modalIdioms.classList.remove('active');
      }});
      document.getElementById('btn-start-idiom-puzzle').addEventListener('click', () => {{
        this.dom.modalIdioms.classList.remove('active');
        this.startIdiomLevel();
      }});

      // Settings Toggles
      document.getElementById('btn-close-settings').addEventListener('click', () => {{
        this.dom.modalSettings.classList.remove('active');
      }});
      document.getElementById('toggle-sound').addEventListener('click', () => {{
        const isMuted = this.sound.toggleMute();
        document.getElementById('toggle-sound').classList.toggle('active', !isMuted);
        this.dom.soundIcon.textContent = isMuted ? '🔇' : '🔊';
      }});
      document.getElementById('toggle-haptic').addEventListener('click', () => {{
        this.hapticEnabled = !this.hapticEnabled;
        this.storage.set('haptic_enabled', this.hapticEnabled);
        document.getElementById('toggle-haptic').classList.toggle('active', this.hapticEnabled);
      }});
      document.getElementById('toggle-dyslexia').addEventListener('click', () => {{
        this.dyslexiaFont = !this.dyslexiaFont;
        this.storage.set('dyslexia_font', this.dyslexiaFont);
        this.applySettings();
      }});
      document.getElementById('toggle-contrast').addEventListener('click', () => {{
        this.highContrast = !this.highContrast;
        this.storage.set('high_contrast', this.highContrast);
        this.applySettings();
      }});
      document.getElementById('toggle-motion').addEventListener('click', () => {{
        this.reducedMotion = !this.reducedMotion;
        this.storage.set('reduced_motion', this.reducedMotion);
        this.applySettings();
      }});

      // No Coins Modal
      document.getElementById('btn-close-no-coins').addEventListener('click', () => {{
        this.dom.modalNoCoins.classList.remove('active');
      }});
      document.getElementById('btn-claim-free-hint').addEventListener('click', () => {{
        this.dom.modalNoCoins.classList.remove('active');
        this.showToast("🎁 Günlük ücretsiz ipucun tahtada açıldı!");
        this.sound.playHint();
        this.revealRandomCell();
      }});

      // Pointer Wheel Interaction
      const wrapper = this.dom.wheelWrapper;
      wrapper.addEventListener('pointerdown', (e) => this.onPointerDown(e));
      wrapper.addEventListener('pointermove', (e) => this.onPointerMove(e));
      wrapper.addEventListener('pointerup', (e) => this.onPointerUp(e));
      wrapper.addEventListener('pointercancel', (e) => this.onPointerUp(e));

      // Resize
      window.addEventListener('resize', () => {{
        this.cacheWheelGeometry();
        this.resizeCrosswordBoard();
      }});
    }}

    /* ---------------- Level Management ---------------- */
    loadLevel(levelIndex) {{
      this.isDailyMode = false;
      this.isIdiomMode = false;
      this.levelRewardClaimed = false;
      this.levelErrorCount = 0;
      this.levelHintsUsed = 0;

      const idx = levelIndex % LEVELS_DATA.length;
      this.currentLevel = LEVELS_DATA[idx];
      this.unlockedWordIds.clear();
      this.revealedCellKeys.clear();
      this.foundBonusWords.clear();
      this.dailyStarKeys.clear();
      this.dailyStarsCollected.clear();

      this.setupLevelUI();
    }}

    startDailyChallenge() {{
      this.isDailyMode = true;
      this.isIdiomMode = false;
      this.levelRewardClaimed = false;
      this.levelErrorCount = 0;
      this.levelHintsUsed = 0;

      // Seed daily level deterministically from Istanbul date
      const dateStr = Turkish.getIstanbulDateString();
      let seedVal = 0;
      for (let i = 0; i < dateStr.length; i++) {{
        seedVal = (seedVal * 31 + dateStr.charCodeAt(i)) >>> 0;
      }}
      const dailyLevelIndex = seedVal % LEVELS_DATA.length;
      this.currentLevel = JSON.parse(JSON.stringify(LEVELS_DATA[dailyLevelIndex]));
      this.currentLevel.title = "Günün Özel Bulmacası";
      this.currentLevel.region = "GÜNLÜK GÖREV";

      this.unlockedWordIds.clear();
      this.revealedCellKeys.clear();
      this.foundBonusWords.clear();
      this.dailyStarKeys.clear();
      this.dailyStarsCollected.clear();

      this.setupLevelUI();
    }}

    startIdiomLevel() {{
      if (!this.selectedIdiom) return;
      this.isDailyMode = false;
      this.isIdiomMode = true;
      this.levelRewardClaimed = false;
      this.levelErrorCount = 0;
      this.levelHintsUsed = 0;

      const word = Turkish.toUpper(this.selectedIdiom.answer);
      const wheelLetters = word.split('').sort(() => 0.5 - Math.random());

      this.currentLevel = {{
        id: "idiom",
        title: "Atasözü Tamamlama",
        region: "TÜRKÇE KÜLTÜR",
        bg: "https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Galata_Tower_Istanbul.jpg/1280px-Galata_Tower_Istanbul.jpg",
        wheel: wheelLetters,
        words: [{{ id: "iw1", word: word, row: 0, col: 0, dir: "H" }}],
        bonus: []
      }};

      this.unlockedWordIds.clear();
      this.revealedCellKeys.clear();
      this.foundBonusWords.clear();

      this.setupLevelUI();
      this.showToast(`📜 Eksik kelimeyi kur: ${word.length} harf!`);
    }}

    setupLevelUI() {{
      this.dom.bgLayer.style.backgroundImage = `url('${this.currentLevel.bg}')`;
      this.dom.regionText.textContent = this.currentLevel.region;
      this.dom.levelTitleText.textContent = this.isDailyMode ? "Günün Bulmacası" : (this.isIdiomMode ? "Atasözü Modu" : `Bölüm ${this.currentLevel.id}`);

      this.renderCrosswordGrid();
      this.currentWheelLetters = [...this.currentLevel.wheel];
      this.renderWheel();
    }}

    /* ---------------- Crossword Grid Engine ---------------- */
    renderCrosswordGrid() {{
      const words = this.currentLevel.words;

      let minR = Infinity, maxR = -Infinity;
      let minC = Infinity, maxC = -Infinity;

      words.forEach(w => {{
        const len = w.word.length;
        const endR = w.dir === 'V' ? w.row + len - 1 : w.row;
        const endC = w.dir === 'H' ? w.col + len - 1 : w.col;
        minR = Math.min(minR, w.row);
        maxR = Math.max(maxR, endR);
        minC = Math.min(minC, w.col);
        maxC = Math.max(maxC, endC);
      }});

      this.normMinR = minR;
      this.normMinC = minC;
      this.gridRows = maxR - minR + 1;
      this.gridCols = maxC - minC + 1;

      this.gridLetterMap = new Map();
      words.forEach(w => {{
        const normR = w.row - minR;
        const normC = w.col - minC;
        for (let i = 0; i < w.word.length; i++) {{
          const r = normR + (w.dir === 'V' ? i : 0);
          const c = normC + (w.dir === 'H' ? i : 0);
          const key = `${{r}}_${{c}}`;
          const ch = Turkish.toUpper(w.word[i]);

          if (!this.gridLetterMap.has(key)) {{
            this.gridLetterMap.set(key, {{ char: ch, wordIds: [w.id], r, c }});
          }} else {{
            this.gridLetterMap.get(key).wordIds.push(w.id);
          }}
        }}
      }});

      if (this.isDailyMode) {{
        const keys = Array.from(this.gridLetterMap.keys()).sort(() => 0.5 - Math.random());
        keys.slice(0, Math.min(3, keys.length)).forEach(k => this.dailyStarKeys.add(k));
      }}

      this.resizeCrosswordBoard();
    }}

    resizeCrosswordBoard() {{
      if (!this.gridRows || !this.gridCols) return;
      const board = document.getElementById('board-area');
      const maxW = board.clientWidth - 16;
      const maxH = board.clientHeight - 16;

      const cellW = Math.floor(maxW / this.gridCols);
      const cellH = Math.floor(maxH / this.gridRows);
      let cellSize = Math.min(cellW, cellH);
      cellSize = Math.max(30, Math.min(cellSize, 54));

      const gridEl = this.dom.crosswordGrid;
      gridEl.style.gridTemplateColumns = `repeat(${this.gridCols}, ${{cellSize}}px)`;
      gridEl.style.gridTemplateRows = `repeat(${this.gridRows}, ${{cellSize}}px)`;
      gridEl.innerHTML = '';

      for (let r = 0; r < this.gridRows; r++) {{
        for (let c = 0; c < this.gridCols; c++) {{
          const key = `${{r}}_${{c}}`;
          const cellEl = document.createElement('div');
          cellEl.className = 'crossword-cell';
          cellEl.dataset.key = key;

          if (this.gridLetterMap.has(key)) {{
            const cellData = this.gridLetterMap.get(key);
            const isRevealed = this.revealedCellKeys.has(key);

            cellEl.innerHTML = `
              <div class="cell-inner">
                <div class="cell-front"></div>
                <div class="cell-back">${{cellData.char}}</div>
              </div>
            `;

            if (isRevealed) {{
              cellEl.classList.add('revealed');
            }}

            if (this.isDailyMode && this.dailyStarKeys.has(key) && !this.dailyStarsCollected.has(key)) {{
              const starEl = document.createElement('div');
              starEl.className = 'star-badge';
              starEl.textContent = '⭐';
              cellEl.appendChild(starEl);
            }}

            cellEl.addEventListener('click', () => this.onCellClicked(key));
          }} else {{
            cellEl.classList.add('hidden');
          }}

          gridEl.appendChild(cellEl);
        }}
      }}
    }}

    /* ---------------- Wheel & Interaction ---------------- */
    renderWheel() {{
      const container = this.dom.wheelNodesContainer;
      container.innerHTML = '';

      const letters = this.currentWheelLetters;
      const count = letters.length;
      const radius = (this.dom.wheelWrapper.clientWidth / 2) - 30;
      const center = this.dom.wheelWrapper.clientWidth / 2;

      this.wheelNodePositions = [];

      letters.forEach((char, idx) => {{
        const angle = (idx * (2 * Math.PI / count)) - (Math.PI / 2);
        const x = center + radius * Math.cos(angle);
        const y = center + radius * Math.sin(angle);

        const node = document.createElement('div');
        node.className = 'wheel-node';
        node.textContent = char;
        node.style.left = `${{x}}px`;
        node.style.top = `${{y}}px`;
        node.dataset.index = idx;

        container.appendChild(node);
        this.wheelNodePositions.push({{ index: idx, char: char, x: x, y: y, element: node }});
      }});
    }}

    cacheWheelGeometry() {{
      if (!this.currentWheelLetters) return;
      this.renderWheel();
    }}

    handleShuffle() {{
      this.vibrate(20);
      this.dom.wheelNodesContainer.style.transition = 'transform 0.35s cubic-bezier(0.34, 1.56, 0.64, 1)';
      this.dom.wheelNodesContainer.style.transform = 'rotate(360deg)';

      setTimeout(() => {{
        this.currentWheelLetters.sort(() => 0.5 - Math.random());
        this.dom.wheelNodesContainer.style.transition = 'none';
        this.dom.wheelNodesContainer.style.transform = 'rotate(0deg)';
        this.renderWheel();
      }}, 350);
    }}

    onPointerDown(e) {{
      this.sound.init();
      this.isDragging = true;
      this.selectedNodeIndices = [];
      this.currentLetters = [];
      this.dom.wheelWrapper.setPointerCapture(e.pointerId);
      this.checkPointerCollision(e.clientX, e.clientY);
    }}

    onPointerMove(e) {{
      if (!this.isDragging) return;
      this.checkPointerCollision(e.clientX, e.clientY);
      this.updateConnectionLine(e.clientX, e.clientY);
    }}

    onPointerUp(e) {{
      if (!this.isDragging) return;
      this.isDragging = false;

      if (this.currentLetters.length > 0) {{
        const formed = Turkish.toUpper(this.currentLetters.join(''));
        this.submitWord(formed);
      }}

      this.selectedNodeIndices = [];
      this.currentLetters = [];
      this.dom.connectionLine.setAttribute('points', '');
      this.dom.wordPreview.classList.remove('active');
      document.querySelectorAll('.wheel-node.selected').forEach(n => n.classList.remove('selected'));
    }}

    checkPointerCollision(clientX, clientY) {{
      const rect = this.dom.wheelWrapper.getBoundingClientRect();
      const relX = clientX - rect.left;
      const relY = clientY - rect.top;
      const hitRadius = 34;

      for (let i = 0; i < this.wheelNodePositions.length; i++) {{
        const node = this.wheelNodePositions[i];
        const dx = relX - node.x;
        const dy = relY - node.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist <= hitRadius) {{
          if (!this.selectedNodeIndices.includes(i)) {{
            this.selectedNodeIndices.push(i);
            this.currentLetters.push(node.char);
            node.element.classList.add('selected');

            this.vibrate(15);
            this.sound.playLetterNote(this.selectedNodeIndices.length - 1);

            const word = this.currentLetters.join('');
            this.dom.wordPreview.textContent = word;
            this.dom.wordPreview.classList.add('active');
          }} else if (this.selectedNodeIndices.length > 1 &&
                     this.selectedNodeIndices[this.selectedNodeIndices.length - 2] === i) {{
            const popped = this.selectedNodeIndices.pop();
            this.currentLetters.pop();
            this.wheelNodePositions[popped].element.classList.remove('selected');

            this.vibrate(10);
            const word = this.currentLetters.join('');
            this.dom.wordPreview.textContent = word;
            if (this.currentLetters.length === 0) {{
              this.dom.wordPreview.classList.remove('active');
            }}
          }}
          break;
        }}
      }}
    }}

    updateConnectionLine(pointerClientX, pointerClientY) {{
      if (this.selectedNodeIndices.length === 0) {{
        this.dom.connectionLine.setAttribute('points', '');
        return;
      }}
      const rect = this.dom.wheelWrapper.getBoundingClientRect();
      const relX = pointerClientX - rect.left;
      const relY = pointerClientY - rect.top;

      let pointsStr = '';
      this.selectedNodeIndices.forEach(idx => {{
        const node = this.wheelNodePositions[idx];
        pointsStr += `${{node.x}},${{node.y}} `;
      }});
      pointsStr += `${{relX}},${{relY}}`;
      this.dom.connectionLine.setAttribute('points', pointsStr);
    }}

    /* ---------------- Word Submission ---------------- */
    submitWord(word) {{
      const matchLevelWord = this.currentLevel.words.find(w => Turkish.toUpper(w.word) === word);

      if (matchLevelWord) {{
        if (this.unlockedWordIds.has(matchLevelWord.id)) {{
          this.showToast("Bu kelime zaten açık!");
          this.sound.playErrorBuzz();
        }} else {{
          this.unlockCrosswordWord(matchLevelWord);
        }}
      }} else if (this.currentLevel.bonus && this.currentLevel.bonus.map(b => Turkish.toUpper(b)).includes(word)) {{
        if (this.foundBonusWords.has(word)) {{
          this.showToast("Bu bonus kelime zaten bulundu!");
          this.sound.playErrorBuzz();
        }} else {{
          this.foundBonusWords.add(word);
          this.sound.playWordSuccess();
          this.showToast(`✨ Bonus Kelime: ${word}`);

          // Kök-Ek Bonusu Check: Did user discover a suffix of an unlocked word?
          this.checkRootSuffixBonus(word);

          this.bonusChestCount++;
          if (this.bonusChestCount >= 5) {{
            this.bonusChestCount = 0;
            this.addCoins(35);
            this.showToast("🎁 Kelime Sandığı Patladı! +35 Altın!");
          }}
          this.storage.set('bonus_chest', this.bonusChestCount);
          this.updateTopbar();
        }}
      }} else {{
        this.levelErrorCount++;
        this.sound.playErrorBuzz();
        this.vibrate([20, 40, 20]);
      }}
    }}

    checkRootSuffixBonus(bonusWord) {{
      this.currentLevel.words.forEach(w => {{
        const base = Turkish.toUpper(w.word);
        if (Turkish.isRootSuffixPair(base, bonusWord)) {{
          this.addCoins(15);
          this.showToast(`🌟 Kök-Ek Bonusu: ${base} ➔ ${bonusWord} (+15 🪙)!`);
        }}
      }});
    }}

    unlockCrosswordWord(wordObj) {{
      this.unlockedWordIds.add(wordObj.id);
      this.sound.playWordSuccess();
      this.vibrate(30);

      const normR = wordObj.row - this.normMinR;
      const normC = wordObj.col - this.normMinC;

      const previewRect = this.dom.wordPreview.getBoundingClientRect();
      const originX = previewRect.left + previewRect.width / 2;
      const originY = previewRect.top + previewRect.height / 2;

      for (let i = 0; i < wordObj.word.length; i++) {{
        const r = normR + (wordObj.dir === 'V' ? i : 0);
        const c = normC + (wordObj.dir === 'H' ? i : 0);
        const key = `${{r}}_${{c}}`;

        const cellEl = document.querySelector(`.crossword-cell[data-key="${{key}}"]`);
        if (cellEl) {{
          const cellRect = cellEl.getBoundingClientRect();
          const targetX = cellRect.left + cellRect.width / 2;
          const targetY = cellRect.top + cellRect.height / 2;

          this.spawnSpark(originX, originY, targetX, targetY, i * 70, () => {{
            cellEl.classList.add('revealed');
            this.revealedCellKeys.add(key);

            if (this.isDailyMode && this.dailyStarKeys.has(key) && !this.dailyStarsCollected.has(key)) {{
              this.collectDailyStar(key, cellEl);
            }}

            this.checkLevelCompletion();
          }});
        }}
      }}
    }}

    spawnSpark(startX, startY, endX, endY, delayMs, onArrive) {{
      setTimeout(() => {{
        const spark = document.createElement('div');
        spark.className = 'spark-projectile';
        spark.style.left = `${{startX}}px`;
        spark.style.top = `${{startY}}px`;
        document.body.appendChild(spark);
        spark.getBoundingClientRect();
        spark.style.transform = `translate(${{endX - startX}}px, ${{endY - startY}}px) scale(1.5)`;

        setTimeout(() => {{
          spark.remove();
          if (onArrive) onArrive();
        }}, 420);
      }}, delayMs);
    }}

    collectDailyStar(cellKey, cellEl) {{
      this.dailyStarsCollected.add(cellKey);
      const starBadge = cellEl.querySelector('.star-badge');
      if (starBadge) starBadge.remove();

      const rect = cellEl.getBoundingClientRect();
      const star = document.createElement('div');
      star.className = 'star-projectile';
      star.textContent = '⭐';
      star.style.left = `${{rect.left + rect.width / 2}}px`;
      star.style.top = `${{rect.top + rect.height / 2}}px`;
      document.body.appendChild(star);

      const targetEl = document.getElementById('btn-open-daily');
      const targetRect = targetEl.getBoundingClientRect();
      star.getBoundingClientRect();
      star.style.transform = `translate(${{targetRect.left - rect.left}}px, ${{targetRect.top - rect.top}}px) scale(0.6)`;

      setTimeout(() => {{
        star.remove();
        this.stars++;
        this.storage.set('stars', this.stars);
        this.showToast("⭐ Parlayan Yıldız Koleksiyona Eklendi!");
      }}, 600);
    }}

    checkLevelCompletion() {{
      if (this.unlockedWordIds.size === this.currentLevel.words.length) {{
        setTimeout(() => this.triggerVictory(), 500);
      }}
    }}

    triggerVictory() {{
      this.sound.playFanfare();
      this.startConfetti();

      // Daily streak management
      if (this.isDailyMode) {{
        const todayStr = Turkish.getIstanbulDateString();
        const yesterdayStr = Turkish.getYesterdayIstanbulString();

        if (!this.completedDailyDates.includes(todayStr)) {{
          if (this.completedDailyDates.includes(yesterdayStr)) {{
            this.streak++;
          }} else {{
            this.streak = 1; // reset streak if a day was missed!
          }}
          this.completedDailyDates.push(todayStr);
          this.storage.set('daily_dates', this.completedDailyDates);
          this.storage.set('streak', this.streak);
          this.updateTopbar();
        }}
      }}

      // Calculate Stars based on hints & errors
      let starCount = 3;
      let evalText = "Harika! Sıfır ipucu ile kusursuz tamamladın.";
      if (this.levelHintsUsed > 1 || this.levelErrorCount > 4) {{
        starCount = 1;
        evalText = "Zorlu bir mücadeleydi, tebrikler!";
      }} else if (this.levelHintsUsed > 0 || this.levelErrorCount > 1) {{
        starCount = 2;
        evalText = "Çok iyi performans!";
      }}
      this.dom.victoryStarsDisplay.textContent = '⭐'.repeat(starCount) + '☆'.repeat(3 - starCount);
      this.dom.victoryEvalText.textContent = evalText;

      // Pop Discovery Card if regular level with registered credit
      const credit = CREDITS_DATA.find(c => c.id === this.currentLevel.region_id);
      if (credit && !this.isDailyMode && !this.isIdiomMode) {{
        this.openDiscoveryCard(credit);
      }} else {{
        this.openVictoryModal();
      }}
    }}

    openDiscoveryCard(credit) {{
      this.dom.discoveryImg.src = credit.image_url;
      this.dom.discoveryRegion.textContent = credit.location;
      this.dom.discoveryTitle.textContent = credit.title;
      this.dom.discoveryTrivia.innerHTML = `
        <p style="margin-bottom:6px;">${{credit.summary}}</p>
        <p style="color:#fef08a;font-weight:700;">💡 Biliyor muydunuz? ${{credit.trivia}}</p>
        <p style="font-size:10.5px;color:#94a3b8;margin-top:6px;">Fotoğraf: ${{credit.author}} (${{credit.license}})</p>
      `;
      this.dom.modalDiscovery.classList.add('active');
    }}

    openVictoryModal() {{
      this.dom.modalVictory.classList.add('active');
    }}

    proceedToNextLevel() {{
      this.stopConfetti();
      if (this.isDailyMode || this.isIdiomMode) {{
        this.loadLevel(this.levelIdx);
      }} else {{
        this.levelIdx = (this.levelIdx + 1) % LEVELS_DATA.length;
        this.storage.set('level_idx', this.levelIdx);
        this.loadLevel(this.levelIdx);
      }}
    }}

    /* ---------------- Power-ups ---------------- */
    handleBulbHint() {{
      if (this.coins < 50) {{
        this.dom.modalNoCoins.classList.add('active');
        return;
      }}
      this.coins -= 50;
      this.storage.set('coins', this.coins);
      this.updateTopbar();
      this.sound.playHint();
      this.levelHintsUsed++;
      this.revealRandomCell();
    }}

    handleTargetMagnifier() {{
      if (this.coins < 90) {{
        this.dom.modalNoCoins.classList.add('active');
        return;
      }}
      this.isTargetingMode = !this.isTargetingMode;
      const btn = document.getElementById('btn-hint-target');

      if (this.isTargetingMode) {{
        btn.classList.add('active-tool');
        document.body.classList.add('targeting-mode');
        this.dom.targetingBanner.style.display = 'block';
        this.showToast("🎯 Açmak istediğin kutucuğa dokun!");
      }} else {{
        btn.classList.remove('active-tool');
        document.body.classList.remove('targeting-mode');
        this.dom.targetingBanner.style.display = 'none';
      }}
    }}

    onCellClicked(cellKey) {{
      if (!this.isTargetingMode) return;
      if (this.revealedCellKeys.has(cellKey)) {{
        this.showToast("Bu kutucuk zaten açık!");
        return;
      }}

      this.coins -= 90;
      this.storage.set('coins', this.coins);
      this.updateTopbar();
      this.sound.playHint();
      this.levelHintsUsed++;

      this.isTargetingMode = false;
      document.getElementById('btn-hint-target').classList.remove('active-tool');
      document.body.classList.remove('targeting-mode');
      this.dom.targetingBanner.style.display = 'none';

      this.revealSingleCell(cellKey);
    }}

    handleLightning() {{
      if (this.coins < 140) {{
        this.dom.modalNoCoins.classList.add('active');
        return;
      }}
      const unrevealed = Array.from(this.gridLetterMap.keys()).filter(k => !this.revealedCellKeys.has(k));
      if (unrevealed.length === 0) return;

      this.coins -= 140;
      this.storage.set('coins', this.coins);
      this.updateTopbar();
      this.levelHintsUsed += 2;

      this.dom.screenFlash.classList.add('flash');
      setTimeout(() => this.dom.screenFlash.classList.remove('flash'), 160);
      this.sound.playLightning();
      this.vibrate([40, 50, 40]);

      const count = Math.min(unrevealed.length, Math.floor(Math.random() * 2) + 3);
      const chosen = unrevealed.sort(() => 0.5 - Math.random()).slice(0, count);

      chosen.forEach((key, idx) => {{
        setTimeout(() => this.revealSingleCell(key), idx * 110);
      }});
    }}

    revealRandomCell() {{
      const unrevealed = Array.from(this.gridLetterMap.keys()).filter(k => !this.revealedCellKeys.has(k));
      if (unrevealed.length === 0) return;
      const randomKey = unrevealed[Math.floor(Math.random() * unrevealed.length)];
      this.revealSingleCell(randomKey);
    }}

    revealSingleCell(cellKey) {{
      const cellEl = document.querySelector(`.crossword-cell[data-key="${{cellKey}}"]`);
      if (!cellEl) return;

      cellEl.classList.add('revealed');
      this.revealedCellKeys.add(cellKey);

      if (this.isDailyMode && this.dailyStarKeys.has(cellKey) && !this.dailyStarsCollected.has(cellKey)) {{
        this.collectDailyStar(cellKey, cellEl);
      }}

      // Check word unlock
      this.currentLevel.words.forEach(w => {{
        if (!this.unlockedWordIds.has(w.id)) {{
          const normR = w.row - this.normMinR;
          const normC = w.col - this.normMinC;
          let allOpen = true;
          for (let i = 0; i < w.word.length; i++) {{
            const r = normR + (w.dir === 'V' ? i : 0);
            const c = normC + (w.dir === 'H' ? i : 0);
            if (!this.revealedCellKeys.has(`${{r}}_${{c}}`)) {{
              allOpen = false;
              break;
            }}
          }}
          if (allOpen) {{
            this.unlockedWordIds.add(w.id);
          }}
        }}
      }});

      this.checkLevelCompletion();
    }}

    /* ---------------- Calendar & Daily ---------------- */
    openCalendarModal() {{
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

      ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'].forEach(dh => {{
        const headerCell = document.createElement('div');
        headerCell.className = 'calendar-day-header';
        headerCell.textContent = dh;
        container.appendChild(headerCell);
      }});

      for (let i = 0; i < startCol; i++) {{
        container.appendChild(document.createElement('div'));
      }}

      for (let day = 1; day <= daysInMonth; day++) {{
        const dayCell = document.createElement('div');
        dayCell.className = 'calendar-day-cell';
        dayCell.textContent = day;

        const dateStr = `${{currentYear}}-${{String(currentMonth + 1).padStart(2, '0')}}-${{String(day).padStart(2, '0')}}`;
        if (this.completedDailyDates.includes(dateStr)) {{
          dayCell.classList.add('completed');
          const check = document.createElement('span');
          check.className = 'check';
          check.textContent = '✔';
          dayCell.appendChild(check);
        }}

        if (day === todayDate) {{
          dayCell.classList.add('today');
        }}

        container.appendChild(dayCell);
      }}

      const isTodayCompleted = this.completedDailyDates.includes(todayStr);
      const playBtn = document.getElementById('btn-play-daily');
      if (isTodayCompleted) {{
        playBtn.textContent = "Bugünkü Görev Tamamlandı!";
        playBtn.disabled = true;
        playBtn.style.opacity = '0.6';
        this.dom.btnShareDaily.style.display = 'block';
      }} else {{
        playBtn.textContent = "Günün Bulmacasını Oyna (3 ⭐)";
        playBtn.disabled = false;
        playBtn.style.opacity = '1';
        this.dom.btnShareDaily.style.display = 'none';
      }}

      this.dom.modalCalendar.classList.add('active');
    }}

    shareDailyResult() {{
      const todayStr = Turkish.getIstanbulDateString();
      const shareText = `Kelime Harikaları Günlük #${{todayStr}}\n⭐ 3/3 Yıldız Toplandı\n🔥 ${{this.streak}} Günlük Seri\n🟩🟩🟩\n🟩⭐🟩\n🟩🟩🟩\nOyna: https://umutcandemircan.github.io/kelime-harikalari/`;

      if (navigator.share) {{
        navigator.share({{ title: "Kelime Harikaları", text: shareText }}).catch(() => {{}});
      }} else if (navigator.clipboard) {{
        navigator.clipboard.writeText(shareText).then(() => {{
          this.showToast("📋 Günlük sonuç panoya kopyalandı!");
        }});
      }}
    }}

    /* ---------------- Idioms & Bonus Chest Modals ---------------- */
    openIdiomsModal() {{
      this.selectedIdiom = IDIOMS_DATA[Math.floor(Math.random() * IDIOMS_DATA.length)];
      this.dom.idiomProverbText.textContent = `"${{this.selectedIdiom.text}}"`;
      this.dom.idiomMeaningText.textContent = `Anlamı: ${{this.selectedIdiom.meaning}}`;
      this.dom.modalIdioms.classList.add('active');
    }}

    openBonusChestModal() {{
      this.dom.modalChestProgress.textContent = `${{this.bonusChestCount}}/5`;
      if (this.foundBonusWords.size > 0) {{
        this.dom.modalChestWordsList.textContent = `Bulunanlar: ${{Array.from(this.foundBonusWords).join(', ')}}`;
      }} else {{
        this.dom.modalChestWordsList.textContent = "Bu bölümde henüz bonus kelime bulunmadı.";
      }}
      this.dom.modalBonusChest.classList.add('active');
    }}

    openSettingsModal() {{
      this.dom.modalSettings.classList.add('active');
    }}

    /* ---------------- Confetti Particles ---------------- */
    startConfetti() {{
      const canvas = this.dom.confettiCanvas;
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      const colors = ['#f59e0b', '#fbbf24', '#22c55e', '#38bdf8', '#a855f7', '#ec4899'];
      this.confettiParticles = [];

      for (let i = 0; i < 80; i++) {{
        this.confettiParticles.push({{
          x: Math.random() * canvas.width,
          y: Math.random() * -canvas.height,
          size: Math.random() * 7 + 5,
          color: colors[Math.floor(Math.random() * colors.length)],
          vx: Math.random() * 4 - 2,
          vy: Math.random() * 5 + 3,
          rot: Math.random() * 360,
          vRot: Math.random() * 6 - 3
        }});
      }}

      const animate = () => {{
        this.ctxConfetti.clearRect(0, 0, canvas.width, canvas.height);
        this.confettiParticles.forEach(p => {{
          p.x += p.vx;
          p.y += p.vy;
          p.rot += p.vRot;
          this.ctxConfetti.save();
          this.ctxConfetti.translate(p.x, p.y);
          this.ctxConfetti.rotate((p.rot * Math.PI) / 180);
          this.ctxConfetti.fillStyle = p.color;
          this.ctxConfetti.fillRect(-p.size / 2, -p.size / 2, p.size, p.size);
          this.ctxConfetti.restore();

          if (p.y > canvas.height + 20) {{
            p.y = -20;
            p.x = Math.random() * canvas.width;
          }}
        }});
        this.confettiAnimId = requestAnimationFrame(animate);
      }};
      animate();
    }}

    stopConfetti() {{
      if (this.confettiAnimId) cancelAnimationFrame(this.confettiAnimId);
      this.ctxConfetti.clearRect(0, 0, this.dom.confettiCanvas.width, this.dom.confettiCanvas.height);
      this.confettiParticles = [];
    }}
  }}

  window.addEventListener('DOMContentLoaded', () => {{
    window.game = new KelimeHarikalariGame();
  }});
'''

full_html = HTML_CONTENT.replace("__JS_ENGINE_INJECTION__", JS_ENGINE)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(full_html)

print(f"Generated index.html successfully! Size: {len(full_html)} bytes.")
