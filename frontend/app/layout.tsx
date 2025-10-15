import type { Metadata } from "next";
import "./globals.css";

import { ThemeProvider } from "./components/theme-provider";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/app-sidebar"

export const metadata: Metadata = {
  title: "QA Patentes",
  description: "Sistema de QA para Patentes.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-br">
      <body className="h-screen overflow-hidden">
        <ThemeProvider
              attribute="class"
              defaultTheme="system"
              enableSystem
              disableTransitionOnChange
            >
          <SidebarProvider>
          <AppSidebar />
            <main className="flex flex-col h-screen w-full">
              <SidebarTrigger className="p-4 cursor-pointer"/>
              <div className="flex-1 flex overflow-y-auto">
                {children}
              </div>
            </main>
          </SidebarProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
