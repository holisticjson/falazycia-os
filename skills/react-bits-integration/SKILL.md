---
name: ckm:react-bits-integration
description: Biblioteka gotowych, animowanych komponentów React Bits dla premium frontendu (Tailwind + Framer Motion).
author: Tomasz Duda & Antigravity
version: 1.0.0
---

# 🎨 ckm:react-bits-integration — Premium UI Animation Hub

Ten skill dostarcza gotowe do wdrożenia, zoptymalizowane pod kątem wydajności wzorce animacji i interaktywnych komponentów z biblioteki **React Bits** (Tailwind CSS + Framer Motion / Vanilla CSS). 
Służy do szybkiego podnoszenia estetyki aplikacji (SaaS, landing pages, ADHD dashboards) do poziomu premium.

---

## 🚀 Szybki Start (Instalacja Zależności)
Przed użyciem komponentów upewnij się, że projekt posiada zainstalowane niezbędne biblioteki:
```bash
npm install framer-motion lucide-react clsx tailwind-merge
```
*Dla projektów Streamlit: animacje osadzamy przez komponenty iframe z kompilacją HTML/JS lub przez dedykowane injecty CSS.*

---

## 📦 Katalog Komponentów (Premium Blueprints)

### 1. 🌌 Spotlight Card (Karta z Reflektorem)
Karta z dynamicznym tłem podążającym za kursorem myszy (efekt glassmorphism/glow). Idealna do sekcji cennika (Pricing) i zalet produktu (Features).

#### Kod Komponentu:
```jsx
import React, { useRef, useState } from "react";

export function SpotlightCard({ children, className = "" }) {
  const divRef = useRef(null);
  const [isFocused, setIsFocused] = useState(false);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [opacity, setIsOpacity] = useState(0);

  const handleMouseMove = (e) => {
    if (!divRef.current || isFocused) return;
    const rect = divRef.current.getBoundingClientRect();
    setPosition({ x: e.clientX - rect.left, y: e.clientY - rect.top });
  };

  const handleFocus = () => {
    setIsFocused(true);
    setIsOpacity(1);
  };

  const handleBlur = () => {
    setIsFocused(false);
    setIsOpacity(0);
  };

  const handleMouseEnter = () => {
    setIsOpacity(1);
  };

  const handleMouseLeave = () => {
    setIsOpacity(0);
  };

  return (
    <div
      ref={divRef}
      onMouseMove={handleMouseMove}
      onFocus={handleFocus}
      onBlur={handleBlur}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      className={`relative overflow-hidden rounded-xl border border-slate-800 bg-[#121620] p-8 ${className}`}
    >
      <div
        className="pointer-events-none absolute -inset-px opacity-0 transition duration-300"
        style={{
          opacity,
          background: `radial-gradient(600px circle at ${position.x}px ${position.y}px, rgba(139, 92, 246, 0.15), transparent 40%)`,
        }}
      />
      {children}
    </div>
  );
}
```

---

### 2. ✍️ Text Wave (Pulsacyjny Tekst)
Efektowna, płynna animacja pojawiania się tekstu litera po literze z opóźnieniem (staggered).

#### Kod Komponentu:
```jsx
import React from "react";
import { motion } from "framer-motion";

export function TextWave({ text, className = "" }) {
  const letters = Array.from(text);

  const container = {
    hidden: { opacity: 0 },
    visible: (i = 1) => ({
      opacity: 1,
      transition: { staggerChildren: 0.04, delayChildren: 0.04 * i },
    }),
  };

  const child = {
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        type: "spring",
        damping: 12,
        stiffness: 100,
      },
    },
    hidden: {
      opacity: 0,
      y: 20,
      transition: {
        type: "spring",
        damping: 12,
        stiffness: 100,
      },
    },
  };

  return (
    <motion.h1
      className={`flex flex-wrap overflow-hidden ${className}`}
      variants={container}
      initial="hidden"
      animate="visible"
    >
      {letters.map((letter, index) => (
        <motion.span variants={child} key={index} className="mr-[0.05em]">
          {letter === " " ? "\u00A0" : letter}
        </motion.span>
      ))}
    </motion.h1>
  );
}
```

---

### 3. 🌀 Aurora Background (Zorza Polarna)
Ekskluzywne, animowane gradientowe tło symulujące zorzę polarną. Doskonałe dla nagłówków Hero (Hero Section).

#### Kod CSS (Tailwind Config extension):
```css
@keyframes aurora {
  from {
    background-position: 50% 50%, 50% 50%;
  }
  to {
    background-position: 350% 50%, 350% 50%;
  }
}

.animate-aurora {
  animation: aurora 60s linear infinite;
}
```

#### Kod Komponentu:
```jsx
import React from "react";

export function AuroraBackground({ children, className = "" }) {
  return (
    <div className={`relative flex flex-col items-center justify-center bg-[#08090C] text-white transition-colors ${className}`}>
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -inset-[10px] opacity-50 filter blur-[100px] saturate-150 animate-aurora
          bg-[radial-gradient(circle_at_50%_120%,#3b82f6,#0000_50%),radial-gradient(circle_at_0%_0%,#8b5cf6,#0000_50%),radial-gradient(circle_at_100%_0%,#ec4899,#0000_50%),radial-gradient(circle_at_50%_0%,#10b981,#0000_50%)]"
        />
      </div>
      <div className="relative z-10">{children}</div>
    </div>
  );
}
```

---

## ⚡ Integracja ze Streamlit (Bypass dla Pythonistów)
Jeśli pracujesz bezpośrednio w `app.py` bez frameworka React, możesz wyrenderować te komponenty przy użyciu osadzania HTML/JS (Custom Components) lub customowego CSS:

```python
import streamlit as st

def inject_spotlight_css():
    st.markdown("""
    <style>
    .premium-card {
        background: #121620;
        border: 1px solid #1E293B;
        border-radius: 12px;
        padding: 24px;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    .premium-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: radial-gradient(circle at var(--mouse-x, 0px) var(--mouse-y, 0px), rgba(139, 92, 246, 0.15) 0%, transparent 60%);
        opacity: 0;
        transition: opacity 0.3s ease;
        pointer-events: none;
    }
    .premium-card:hover::before {
        opacity: 1;
    }
    </style>
    
    <script>
    const cards = document.querySelectorAll('.premium-card');
    cards.forEach(card => {
        card.addEventListener('mousemove', e => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            card.style.setProperty('--mouse-x', `${x}px`);
            card.style.setProperty('--mouse-y', `${y}px`);
        });
    });
    </script>
    """, unsafe_allow_html=True)
```

---

## 🛡️ Złote Zasady (Guardrails)
1. **Wydajność:** Ograniczaj liczbę równoległych animacji Framer Motion na jednej stronie. Zbyt duża ich ilość wywoła "lagowanie" na starszych komputerach.
2. **ADHD Accessibility:** Animacje nie mogą być zbyt szybkie ani agresywne. Stosuj delikatne przejścia (transitions `0.3s` - `0.6s`) oraz niską częstotliwość mrugania (neon, strobe).
3. **Spójność kolorystyczna:** Dostosuj gradienty i podświetlenia (glow) do barw Holistic OS (`#8B5CF6` fiolet, `#EC4899` róż, `#08090C` głęboka czerń).
