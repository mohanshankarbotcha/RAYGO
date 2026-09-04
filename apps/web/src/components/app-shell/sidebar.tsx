"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Target,
  FlaskConical,
  Sparkles,
  ShoppingCart,
  Package,
  CreditCard,
  Bot,
  ShieldCheck,
  FileSearch,
  MessageCircleMore,
} from "lucide-react";
import { sidebarNav } from "@/lib/routes";

const iconMap = {
  "layout-dashboard": LayoutDashboard,
  target: Target,
  "flask-conical": FlaskConical,
  sparkles: Sparkles,
  "shopping-cart": ShoppingCart,
  package: Package,
  "credit-card": CreditCard,
  bot: Bot,
  "shield-check": ShieldCheck,
  "file-search": FileSearch,
};

import { useState } from "react";
import { CopilotDrawer } from "@/components/shared/copilot-drawer";

export function Sidebar() {
  const pathname = usePathname();
  const [copilotOpen, setCopilotOpen] = useState(false);

  return (
    <>
      <aside className="hidden lg:flex lg:flex-col w-sidebar shrink-0 h-screen sticky top-0 border-r border-border-subtle bg-surface-container-lowest">
        <div className="flex items-center gap-2 px-5 h-16 border-b border-border-subtle">
          <Sparkles className="text-primary" size={22} />
          <span className="font-headline-md text-headline-md tracking-tight">RAYGO</span>
        </div>
        <nav className="flex-1 overflow-y-auto py-4 px-3 flex flex-col gap-1">
          {sidebarNav.map((item) => {
            const Icon = iconMap[item.icon];
            const active = pathname === item.href || pathname.startsWith(item.href + "/");
            return (
              <Link
                key={item.href}
                href={item.href}
                prefetch={true}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-lg font-body-sm text-body-sm transition-all active:scale-[0.98] ${
                  active
                    ? "bg-primary text-on-primary shadow-sm"
                    : "text-on-surface-variant hover:bg-surface-container hover:text-on-surface"
                }`}
              >
                <Icon size={17} />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>
        <div className="p-3 border-t border-border-subtle">
          <button 
            onClick={() => setCopilotOpen(true)}
            className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg font-label-bold text-label-bold bg-primary/10 hover:bg-primary/20 text-primary border border-primary/20 transition-all active:scale-[0.98]"
          >
            <MessageCircleMore size={17} />
            Ask RAYGO
          </button>
        </div>
      </aside>
      <CopilotDrawer isOpen={copilotOpen} onClose={() => setCopilotOpen(false)} />
    </>
  );
}
