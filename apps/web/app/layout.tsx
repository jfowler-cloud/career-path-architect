import type { Metadata } from "next";
import "@cloudscape-design/global-styles/index.css";

export const metadata: Metadata = {
  title: "Career Path Architect",
  description: "AI-powered career planning with visual learning roadmaps",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
