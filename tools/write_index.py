# -*- coding: utf-8 -*-
import json

HTML_TEMPLATE = r'''<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>Kelime Harikaları - Words of Wonders</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@600;700;800;900&display=swap" rel="stylesheet">
  <style>
    :root {
      --font-main: 'Outfit', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --gold: #f59e0b;
      --gold-light: #fef3c7;
      --gold-glow: rgba(245, 158, 11, 0.4);
      --green: #22c55e;
      --green-glow: rgba(34, 197, 94, 0.4);
      --cyan: #06b6d4;
      --cyan-glow: rgba(6, 182, 212, 0.4);
      --navy-900: #0f172a;
      --navy-800: #1e293b;
      --navy-700: #334155;
      --wheel-size: 240px;
      --node-size: 56px;
    }

    @media (max-height: 750px) {
      :root {
        --wheel-size: 210px;
        --node-size: 50px;
      }
    }
    @media (max-height: 650px) {
      :root {
        --wheel-size: 180px;
        --node-size: 44px;
      }
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      user-select: none;
      -webkit-user-select: none;
      -webkit-tap-highlight-color: transparent;
      touch-action: manipulation;
    }

    html, body {
      width: 100%;
      height: 100%;
      overflow: hidden;
      font-family: var(--font-main);
      background: #020617;
      color: #fff;
    }

    /* Screen Background with dynamic overlay */
    #bg-layer {
      position: absolute;
      inset: 0;
      background-size: cover;
      background-position: center;
      filter: brightness(0.65) saturate(1.15);
      transition: background-image 0.8s cubic-bezier(0.4, 0, 0.2, 1);
      z-index: 0;
    }

    #bg-gradient {
      position: absolute;
      inset: 0;
      background: radial-gradient(circle at 50% 30%, rgba(15, 23, 42, 0.3) 0%, rgba(2, 6, 23, 0.85) 100%);
      z-index: 1;
    }

    /* Game App Container */
    #app-container {
      position: relative;
      z-index: 2;
      width: 100%;
      max-width: 500px;
      height: 100%;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: env(safe-area-inset-top, 12px) 12px env(safe-area-inset-bottom, 12px) 12px;
    }

    /* Header Bar */
    header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 52px;
      padding: 0 4px;
      gap: 8px;
    }

    .header-pill {
      display: flex;
      align-items: center;
      gap: 6px;
      background: rgba(15, 23, 42, 0.75);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      padding: 6px 12px;
      border-radius: 999px;
      border: 1px solid rgba(255, 255, 255, 0.15);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
      font-weight: 700;
      font-size: 13px;
    }

    .level-badge {
      display: flex;
      flex-direction: column;
      line-height: 1.1;
    }
    .level-badge .sub-title {
      font-size: 10px;
      color: #94a3b8;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .level-badge .main-title {
      font-size: 14px;
      color: #f8fafc;
      font-weight: 800;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 130px;
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .btn-header {
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 5px;
      background: rgba(15, 23, 42, 0.75);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 999px;
      padding: 6px 10px;
      color: #fff;
      font-size: 13px;
      font-weight: 800;
      box-shadow: 0 4px 12px rgba(0,0,0,0.25);
      transition: transform 0.15s, background-color 0.15s;
    }
    .btn-header:active {
      transform: scale(0.92);
    }
    .btn-header.daily-btn {
      background: linear-gradient(135deg, rgba(245, 158, 11, 0.3), rgba(217, 119, 6, 0.5));
      border-color: rgba(245, 158, 11, 0.6);
      color: #fef08a;
    }

    .coin-badge {
      color: #fef08a;
      text-shadow: 0 0 8px var(--gold-glow);
    }

    /* Crossword Board Area */
    #board-area {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 160px;
      position: relative;
      padding: 8px;
    }

    #crossword-grid {
      display: grid;
      gap: 6px;
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
      transition: transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
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
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.35);
    }

    /* Front (Locked state) */
    .cell-front {
      background: rgba(255, 255, 255, 0.16);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      border: 1.5px solid rgba(255, 255, 255, 0.35);
      color: transparent;
      cursor: pointer;
      transition: border-color 0.2s, box-shadow 0.2s, background-color 0.2s;
    }

    /* Targeting mode pulse for locked cells */
    body.targeting-mode .cell-front {
      border: 2px solid #38bdf8 !important;
      box-shadow: 0 0 16px rgba(56, 189, 248, 0.8) !important;
      animation: pulseTarget 1s infinite alternate;
      cursor: crosshair;
    }
    @keyframes pulseTarget {
      0% { transform: scale(0.96); background: rgba(56, 189, 248, 0.2); }
      100% { transform: scale(1.04); background: rgba(56, 189, 248, 0.4); }
    }

    /* Back (Revealed state) */
    .cell-back {
      background: linear-gradient(135deg, #ffffff, #f1f5f9);
      border: 2px solid #fbbf24;
      color: #0f172a;
      transform: rotateY(180deg);
      font-size: 20px;
      text-shadow: 0 1px 1px rgba(0, 0, 0, 0.1);
      box-shadow: 0 0 14px rgba(251, 191, 36, 0.5), inset 0 2px 4px rgba(255, 255, 255, 0.8);
    }

    /* Star Badge on Daily Challenge Cell */
    .star-badge {
      position: absolute;
      top: -6px;
      right: -6px;
      font-size: 14px;
      z-index: 5;
      animation: floatStar 1.8s ease-in-out infinite alternate;
      filter: drop-shadow(0 0 6px rgba(245, 158, 11, 0.9));
    }
    @keyframes floatStar {
      0% { transform: translateY(0) scale(1); }
      100% { transform: translateY(-4px) scale(1.15); }
    }

    /* Targeting Banner */
    #targeting-banner {
      display: none;
      position: absolute;
      top: 65px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(14, 165, 233, 0.9);
      backdrop-filter: blur(10px);
      padding: 6px 16px;
      border-radius: 999px;
      font-size: 13px;
      font-weight: 800;
      color: #fff;
      box-shadow: 0 4px 16px rgba(14, 165, 233, 0.5);
      z-index: 20;
      animation: bounceBanner 0.6s infinite alternate;
    }
    @keyframes bounceBanner {
      0% { transform: translate(-50%, 0); }
      100% { transform: translate(-50%, -4px); }
    }

    /* Preview Pill */
    #preview-container {
      height: 40px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 4px;
    }

    #word-preview {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-width: 80px;
      height: 36px;
      padding: 0 18px;
      border-radius: 999px;
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1.5px solid rgba(255, 255, 255, 0.2);
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
      font-size: 18px;
      font-weight: 900;
      letter-spacing: 2px;
      color: #f8fafc;
      opacity: 0;
      transform: scale(0.85);
      transition: opacity 0.2s, transform 0.2s, border-color 0.2s;
    }
    #word-preview.active {
      opacity: 1;
      transform: scale(1);
      border-color: #fbbf24;
      box-shadow: 0 0 20px var(--gold-glow);
    }

    /* Power-ups Toolbar */
    #powerups-toolbar {
      display: flex;
      align-items: center;
      justify-content: space-around;
      width: 100%;
      max-width: 380px;
      margin: 0 auto 6px auto;
      padding: 0 10px;
    }

    .btn-powerup {
      cursor: pointer;
      position: relative;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      width: 52px;
      height: 52px;
      border-radius: 50%;
      background: linear-gradient(135deg, rgba(30, 41, 59, 0.85), rgba(15, 23, 42, 0.95));
      backdrop-filter: blur(10px);
      border: 1.5px solid rgba(255, 255, 255, 0.2);
      box-shadow: 0 6px 14px rgba(0, 0, 0, 0.35);
      color: #fff;
      transition: transform 0.15s, border-color 0.2s, box-shadow 0.2s;
    }
    .btn-powerup:active {
      transform: scale(0.9);
    }
    .btn-powerup .icon {
      font-size: 19px;
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
      box-shadow: 0 0 16px rgba(56, 189, 248, 0.8);
      background: rgba(14, 165, 233, 0.3);
    }

    /* Bonus Chest Badge */
    .bonus-chest-btn {
      cursor: pointer;
      position: relative;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      width: 52px;
      height: 52px;
      border-radius: 50%;
      background: linear-gradient(135deg, rgba(168, 85, 247, 0.35), rgba(126, 34, 206, 0.65));
      border: 1.5px solid rgba(216, 180, 254, 0.4);
      box-shadow: 0 6px 14px rgba(0, 0, 0, 0.35);
      color: #fff;
      transition: transform 0.15s;
    }
    .bonus-chest-btn:active {
      transform: scale(0.9);
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
      margin: 0 auto 12px auto;
      display: flex;
      align-items: center;
      justify-content: center;
      touch-action: none;
    }

    #wheel-canvas-container {
      position: absolute;
      inset: 0;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.8) 100%);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 2px solid rgba(255, 255, 255, 0.18);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), inset 0 0 20px rgba(255, 255, 255, 0.05);
      pointer-events: none;
    }

    /* SVG Connector Line Layer */
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
      stroke-width: 12;
      stroke-linecap: round;
      stroke-linejoin: round;
      filter: drop-shadow(0 0 8px rgba(251, 191, 36, 0.9));
      transition: stroke-dashoffset 0.05s linear;
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
      font-size: 24px;
      font-weight: 900;
      box-shadow: 0 6px 14px rgba(0, 0, 0, 0.3), inset 0 2px 4px rgba(255, 255, 255, 0.9);
      border: 2px solid rgba(255, 255, 255, 0.8);
      z-index: 20;
      transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), background 0.2s, box-shadow 0.2s, color 0.2s;
      transform: translate(-50%, -50%);
    }

    .wheel-node.selected {
      background: linear-gradient(135deg, #fbbf24, #f59e0b);
      color: #ffffff;
      transform: translate(-50%, -50%) scale(1.18);
      box-shadow: 0 0 22px rgba(245, 158, 11, 0.9), inset 0 2px 4px rgba(255, 255, 255, 0.5);
      border-color: #fef08a;
    }

    /* Screen Flash Effect for Lightning */
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

    /* Flying Spark Projectile */
    .spark-projectile {
      position: fixed;
      width: 14px;
      height: 14px;
      border-radius: 50%;
      background: #fbbf24;
      box-shadow: 0 0 16px #fbbf24, 0 0 28px #f59e0b;
      pointer-events: none;
      z-index: 1000;
      transition: all 0.45s cubic-bezier(0.25, 1, 0.5, 1);
    }

    /* Flying Star Projectile */
    .star-projectile {
      position: fixed;
      font-size: 22px;
      pointer-events: none;
      z-index: 1001;
      filter: drop-shadow(0 0 10px rgba(245, 158, 11, 0.9));
      transition: all 0.65s cubic-bezier(0.2, 0.8, 0.2, 1);
    }

    /* Flying Word Toast */
    .floating-toast {
      position: fixed;
      bottom: 240px;
      left: 50%;
      transform: translateX(-50%) translateY(0);
      background: rgba(15, 23, 42, 0.9);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.2);
      padding: 8px 20px;
      border-radius: 999px;
      font-weight: 800;
      font-size: 14px;
      color: #fef08a;
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
      z-index: 2000;
      pointer-events: none;
      animation: toastAnim 1.6s forwards;
    }
    @keyframes toastAnim {
      0% { opacity: 0; transform: translateX(-50%) translateY(15px); }
      15% { opacity: 1; transform: translateX(-50%) translateY(0); }
      75% { opacity: 1; transform: translateX(-50%) translateY(-5px); }
      100% { opacity: 0; transform: translateX(-50%) translateY(-25px); }
    }

    /* Modals Glassmorphism */
    .modal-overlay {
      position: fixed;
      inset: 0;
      background: rgba(2, 6, 23, 0.85);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      z-index: 5000;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 16px;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.3s ease;
    }
    .modal-overlay.active {
      opacity: 1;
      pointer-events: auto;
    }

    .modal-card {
      width: 100%;
      max-width: 420px;
      background: linear-gradient(135deg, rgba(30, 41, 59, 0.95), rgba(15, 23, 42, 0.98));
      border: 1.5px solid rgba(255, 255, 255, 0.18);
      border-radius: 24px;
      padding: 24px;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), 0 0 30px rgba(245, 158, 11, 0.2);
      text-align: center;
      transform: scale(0.9);
      transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .modal-overlay.active .modal-card {
      transform: scale(1);
    }

    /* Discovery Card Modal */
    .discovery-img {
      width: 100%;
      height: 200px;
      border-radius: 16px;
      object-fit: cover;
      margin-bottom: 14px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
      border: 1.5px solid rgba(255, 255, 255, 0.2);
    }
    .discovery-badge {
      display: inline-block;
      background: rgba(245, 158, 11, 0.2);
      border: 1px solid rgba(245, 158, 11, 0.6);
      color: #fef08a;
      font-size: 11px;
      font-weight: 800;
      padding: 4px 12px;
      border-radius: 999px;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 6px;
    }
    .discovery-title {
      font-size: 20px;
      font-weight: 900;
      color: #fff;
      margin-bottom: 10px;
    }
    .discovery-trivia {
      font-size: 13px;
      line-height: 1.5;
      color: #cbd5e1;
      margin-bottom: 20px;
      background: rgba(15, 23, 42, 0.6);
      padding: 12px;
      border-radius: 12px;
      border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Buttons */
    .btn-gold {
      cursor: pointer;
      width: 100%;
      padding: 14px 20px;
      border-radius: 999px;
      border: none;
      background: linear-gradient(135deg, #fbbf24, #d97706);
      color: #0f172a;
      font-weight: 900;
      font-size: 16px;
      box-shadow: 0 8px 20px rgba(245, 158, 11, 0.4);
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: transform 0.15s, box-shadow 0.15s;
    }
    .btn-gold:active {
      transform: scale(0.96);
    }

    .btn-secondary {
      cursor: pointer;
      width: 100%;
      padding: 12px 20px;
      border-radius: 999px;
      border: 1px solid rgba(255, 255, 255, 0.2);
      background: rgba(30, 41, 59, 0.6);
      color: #cbd5e1;
      font-weight: 800;
      font-size: 14px;
      margin-top: 10px;
      transition: transform 0.15s, background 0.15s;
    }
    .btn-secondary:active {
      transform: scale(0.96);
    }

    /* Victory Modal Special */
    .victory-stars {
      display: flex;
      justify-content: center;
      gap: 12px;
      font-size: 38px;
      margin-bottom: 12px;
      filter: drop-shadow(0 0 14px rgba(245, 158, 11, 0.8));
    }
    .reward-box {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      background: rgba(245, 158, 11, 0.15);
      border: 1px solid rgba(245, 158, 11, 0.4);
      padding: 10px;
      border-radius: 14px;
      font-weight: 900;
      font-size: 18px;
      color: #fef08a;
      margin-bottom: 18px;
    }

    /* Calendar Grid */
    .calendar-grid {
      display: grid;
      grid-template-columns: repeat(7, 1fr);
      gap: 6px;
      margin: 16px 0;
    }
    .calendar-day-header {
      font-size: 11px;
      font-weight: 800;
      color: #94a3b8;
      text-transform: uppercase;
    }
    .calendar-day-cell {
      height: 38px;
      border-radius: 8px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      font-size: 12px;
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
      font-size: 10px;
      color: #22c55e;
      position: absolute;
      bottom: 2px;
    }

    /* Ad Simulators */
    .ad-screen {
      position: fixed;
      inset: 0;
      background: #000;
      z-index: 9000;
      display: none;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      color: #fff;
      text-align: center;
      padding: 24px;
    }
    .ad-screen.active {
      display: flex;
    }
    .ad-countdown {
      position: absolute;
      top: 20px;
      right: 20px;
      background: rgba(255, 255, 255, 0.2);
      border: 1px solid rgba(255, 255, 255, 0.4);
      padding: 6px 14px;
      border-radius: 999px;
      font-weight: 800;
      font-size: 14px;
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

  <!-- Background Layer -->
  <div id="bg-layer"></div>
  <div id="bg-gradient"></div>

  <!-- Screen Flash for Thunder/Lightning -->
  <div id="screen-flash"></div>

  <!-- Confetti Canvas -->
  <canvas id="confetti-canvas"></canvas>

  <!-- Targeting Instruction Banner -->
  <div id="targeting-banner">🎯 Açmak istediğin kutucuğa dokun!</div>

  <!-- Main Game App -->
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
        <button class="btn-header daily-btn" id="btn-open-daily">
          <span>📅</span> Günlük <span id="streak-indicator">🔥 1</span>
        </button>
        <button class="btn-header" id="btn-sound-toggle">
          <span id="sound-icon">🔊</span>
        </button>
        <div class="header-pill coin-badge">
          <span>🪙</span> <span id="coins-display">200</span>
        </div>
      </div>
    </header>

    <!-- Crossword Grid Area -->
    <main id="board-area">
      <div id="crossword-grid"></div>
    </main>

    <!-- Bottom Controls & Wheel Area -->
    <section id="bottom-section">

      <!-- Word Preview Pill -->
      <div id="preview-container">
        <div id="word-preview">KELİME</div>
      </div>

      <!-- Power-ups Toolbar -->
      <div id="powerups-toolbar">
        <!-- Shuffle -->
        <button class="btn-powerup" id="btn-shuffle" title="Harfleri Karıştır">
          <span class="icon">🔀</span>
          <span class="cost">Ücretsiz</span>
        </button>

        <!-- Bulb Hint (50) -->
        <button class="btn-powerup" id="btn-hint-bulb" title="Rastgele Harf Aç">
          <span class="icon">💡</span>
          <span class="cost">🪙 50</span>
        </button>

        <!-- Target Magnifier (100) -->
        <button class="btn-powerup" id="btn-hint-target" title="Hedef Harfi Aç">
          <span class="icon">🎯</span>
          <span class="cost">🪙 100</span>
        </button>

        <!-- Lightning Fireworks (150) -->
        <button class="btn-powerup" id="btn-hint-lightning" title="3 Harf Patlat">
          <span class="icon">⚡</span>
          <span class="cost">🪙 150</span>
        </button>

        <!-- Bonus Words Chest -->
        <button class="bonus-chest-btn" id="btn-bonus-chest" title="Ekstra Kelime Sandığı">
          <span class="icon">🎁</span>
          <span class="counter" id="bonus-counter">0/5</span>
        </button>
      </div>

      <!-- Letter Wheel -->
      <div id="wheel-wrapper">
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
  <div class="modal-overlay" id="modal-discovery">
    <div class="modal-card">
      <img class="discovery-img" id="discovery-img" src="" alt="Landmark">
      <span class="discovery-badge" id="discovery-region">BÖLGE</span>
      <h2 class="discovery-title" id="discovery-title">Tarihi Yapı</h2>
      <p class="discovery-trivia" id="discovery-trivia">Eser hakkında kültürel bilgi burada yer alacak.</p>
      <button class="btn-gold" id="btn-discovery-continue">
        <span>Devam Et</span> ➔
      </button>
    </div>
  </div>

  <!-- 2. Victory Modal with 2X Monetization -->
  <div class="modal-overlay" id="modal-victory">
    <div class="modal-card">
      <div class="victory-stars">⭐⭐⭐</div>
      <h2 style="font-size:26px; font-weight:900; margin-bottom:6px;">Bölüm Tamamlandı!</h2>
      <p style="color:#94a3b8; font-size:14px; margin-bottom:16px;">Tüm kelimeleri ustalıkla çözdün.</p>

      <div class="reward-box">
        <span>Kazanılan Ödül:</span>
        <span style="color:#fbbf24;">+25 Altın</span>
      </div>

      <!-- 2X Rewarded Ad Button -->
      <button class="btn-gold" id="btn-victory-2x" style="margin-bottom:8px; font-size:15px;">
        <span>🎁 2 Katı Kazan: +50 Altın</span>
        <span style="font-size:11px; background:rgba(0,0,0,0.25); padding:2px 6px; border-radius:6px;">Reklam</span>
      </button>

      <!-- Standard Continue -->
      <button class="btn-secondary" id="btn-victory-normal">
        Normal Devam (+25 Altın)
      </button>
    </div>
  </div>

  <!-- 3. Daily Challenge & Calendar Modal -->
  <div class="modal-overlay" id="modal-calendar">
    <div class="modal-card" style="max-width: 440px;">
      <h2 style="font-size:22px; font-weight:900; margin-bottom:4px;">📅 Günlük Bulmaca</h2>
      <p style="color:#fef08a; font-weight:800; font-size:14px;" id="calendar-streak-text">🔥 1 Günlük Seri</p>

      <!-- Calendar Month Days -->
      <div class="calendar-grid" id="calendar-grid-container">
        <!-- Rendered by JS -->
      </div>

      <div style="font-size:12px; color:#94a3b8; margin-bottom:14px;" id="daily-status-desc">
        Günün bulmacasında 3 parlayan yıldızı toplayarak serini devam ettir!
      </div>

      <button class="btn-gold" id="btn-play-daily">
        <span>Günün Bulmacasını Oyna</span> 🌟
      </button>

      <button class="btn-secondary" id="btn-close-calendar">
        Kapat
      </button>
    </div>
  </div>

  <!-- 4. Insufficient Coins Modal -->
  <div class="modal-overlay" id="modal-no-coins">
    <div class="modal-card">
      <div style="font-size:40px; margin-bottom:8px;">🪙</div>
      <h2 style="font-size:22px; font-weight:900; margin-bottom:6px;">Yetersiz Altın!</h2>
      <p style="color:#cbd5e1; font-size:13px; margin-bottom:18px;">
        Bu gücü kullanmak için yeterli altının yok. Kısa bir reklam izleyerek hemen +100 Altın kazanabilirsin!
      </p>
      <button class="btn-gold" id="btn-watch-ad-for-coins">
        <span>🎥 Reklam İzle: +100 Altın</span>
      </button>
      <button class="btn-secondary" id="btn-close-no-coins">
        Vazgeç
      </button>
    </div>
  </div>

  <!-- 5. Simulated Rewarded Ad Overlay -->
  <div class="ad-screen" id="rewarded-ad-screen">
    <div class="ad-countdown" id="rewarded-ad-timer">Ödüllü Reklam - 5s</div>
    <div style="font-size:56px; margin-bottom:16px;">🎮</div>
    <h2 style="font-size:26px; font-weight:900; margin-bottom:8px;">Kelime Harikaları</h2>
    <p style="color:#94a3b8; max-width:280px; font-size:14px; margin-bottom:24px;">
      Harika oyunları keşfetmeye devam et! Sponsor video oynatılıyor...
    </p>
    <div style="width:180px; height:8px; background:rgba(255,255,255,0.2); border-radius:999px; overflow:hidden;">
      <div id="rewarded-ad-progress" style="width:0%; height:100%; background:#fbbf24; transition:width 1s linear;"></div>
    </div>
  </div>

  <!-- 6. Simulated Interstitial Ad Overlay -->
  <div class="ad-screen" id="interstitial-ad-screen">
    <div class="ad-countdown" id="interstitial-ad-timer">Geçiş Reklamı - 3s</div>
    <div style="font-size:50px; margin-bottom:14px;">✨</div>
    <h2 style="font-size:24px; font-weight:900; margin-bottom:6px;">Bölüm Arası Sponsoru</h2>
    <p style="color:#94a3b8; font-size:13px;">Oyun yükleniyor, lütfen bekleyin...</p>
  </div>

  <!-- ==================== LOGIC ENGINE ==================== -->
  <script>
    /* GAME DATABASE & SOUND & CORE CONTROLLER */
    __GAME_SCRIPT_INJECTION__
  </script>
</body>
</html>
'''

with open("index_template.html", "w", encoding="utf-8") as f:
    f.write(HTML_TEMPLATE)

print("Template ready")
