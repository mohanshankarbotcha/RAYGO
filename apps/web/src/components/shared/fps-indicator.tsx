"use client";

import { useEffect, useState } from "react";
import { Activity } from "lucide-react";

export function RefreshRateIndicator() {
  const [fps, setFps] = useState<number | null>(null);
  const [detectedHz, setDetectedHz] = useState<string>("120Hz Mode");

  useEffect(() => {
    let frameCount = 0;
    let lastTime = performance.now();
    let animationFrameId: number;

    const measure = (now: number) => {
      frameCount++;
      const delta = now - lastTime;
      if (delta >= 1000) {
        const measuredFps = Math.round((frameCount * 1000) / delta);
        setFps(measuredFps);
        if (measuredFps >= 100) {
          setDetectedHz("120Hz ProMotion");
        } else if (measuredFps >= 80) {
          setDetectedHz("90Hz High-Refresh");
        } else {
          setDetectedHz("60Hz Standard");
        }
        frameCount = 0;
        lastTime = now;
      }
      animationFrameId = requestAnimationFrame(measure);
    };

    animationFrameId = requestAnimationFrame(measure);
    return () => cancelAnimationFrame(animationFrameId);
  }, []);

  return (
    <div 
      title={`Live Display Frame Rate: ${fps ?? "..."} FPS (${detectedHz})`}
      className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-50 border border-emerald-200/80 text-emerald-700 text-xs font-mono font-medium shadow-2xs select-none transition-all hover:bg-emerald-100/60"
    >
      <span className="relative flex h-2 w-2">
        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
        <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
      </span>
      <Activity size={12} className="text-emerald-600" />
      <span>{fps !== null ? `${fps} FPS` : "Calibrating..."}</span>
      <span className="text-emerald-600/70 text-[10px] hidden md:inline font-sans">
        ({detectedHz})
      </span>
    </div>
  );
}
