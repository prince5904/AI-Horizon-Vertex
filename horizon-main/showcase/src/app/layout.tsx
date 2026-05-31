import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Horizon | AI Recruiter Copilot",
  description: "An intelligent recruitment automation pipeline using LangGraph & Composio. Best Idea Award winner at Composio Agents in Production Hackathon.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="scroll-smooth">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet" />
      </head>
      <body className="min-h-screen bg-[#050505] text-white flex flex-col antialiased" suppressHydrationWarning>
        {children}
      </body>
    </html>
  );
}
