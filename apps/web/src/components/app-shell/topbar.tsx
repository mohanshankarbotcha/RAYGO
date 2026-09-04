"use client";

import { useState } from "react";
import { Search, Bell, HelpCircle } from "lucide-react";
import { merchant } from "@/data/fixtures/demo-scenario";
import { RefreshRateIndicator } from "@/components/shared/fps-indicator";
import { CopilotDrawer } from "@/components/shared/copilot-drawer";

export function Topbar() {
  const [copilotOpen, setCopilotOpen] = useState(false);

  return (
    <>
      <header className="sticky top-0 z-20 glass-surface flex items-center justify-between gap-4 h-16 px-6">
        <div className="flex items-center gap-3 min-w-0">
          <div className="flex items-center justify-center w-8 h-8 rounded-full bg-primary text-on-primary font-label-bold text-label-bold shrink-0">
            {merchant.name.charAt(0)}
          </div>
          <div className="min-w-0">
            <p className="font-label-bold text-label-bold text-on-surface truncate">{merchant.name}</p>
            <p className="font-body-sm text-body-sm text-on-surface-variant truncate">{merchant.category}</p>
          </div>
        </div>

        <div 
          onClick={() => setCopilotOpen(true)}
          className="flex-1 max-w-md hidden md:flex items-center gap-2 px-3 py-2 rounded-lg border border-border-subtle bg-surface-container-lowest cursor-pointer hover:border-primary/40 transition-colors"
        >
          <Search size={15} className="text-on-surface-variant" />
          <input
            readOnly
            placeholder="Search or ask RAYGO Copilot..."
            className="w-full bg-transparent outline-none font-body-sm text-body-sm placeholder:text-on-surface-variant cursor-pointer"
          />
        </div>

        <div className="flex items-center gap-3 shrink-0">
          <RefreshRateIndicator />
          <button aria-label="Notifications" className="p-2 rounded-lg hover:bg-surface-container text-on-surface-variant">
            <Bell size={17} />
          </button>
          <button aria-label="Help" className="p-2 rounded-lg hover:bg-surface-container text-on-surface-variant">
            <HelpCircle size={17} />
          </button>
        </div>
      </header>
      <CopilotDrawer isOpen={copilotOpen} onClose={() => setCopilotOpen(false)} />
    </>
  );
}
