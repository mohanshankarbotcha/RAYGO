"use client";

import Link from "next/link";
import { Sparkles, ArrowLeft } from "lucide-react";
import { routes } from "@/lib/routes";

export default function NotFound() {
  return (
    <div className="min-h-screen bg-surface text-on-surface flex flex-col items-center justify-center p-6 text-center">
      <div className="flex items-center gap-2 mb-4">
        <Sparkles className="text-primary w-8 h-8" />
        <span className="font-headline-lg text-headline-lg font-bold">RAYGO</span>
      </div>
      <h1 className="text-6xl font-bold text-primary mb-2">404</h1>
      <h2 className="text-xl font-semibold mb-4">Page Not Found</h2>
      <p className="text-on-surface-variant max-w-md mb-8">
        The page you are looking for does not exist or has been moved.
      </p>
      <Link
        href={routes.overview}
        className="inline-flex items-center gap-2 px-6 py-3 rounded-lg bg-primary text-on-primary font-medium hover:opacity-90 transition-opacity"
      >
        <ArrowLeft className="w-4 h-4" />
        Return to Overview
      </Link>
    </div>
  );
}
