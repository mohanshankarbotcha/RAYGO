import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "RAYGO - Autonomous Revenue Intelligence",
  description: "AI revenue intelligence for modern commerce.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`light ${inter.variable}`}>
      <body className="font-body-base antialiased">{children}</body>
    </html>
  );
}
