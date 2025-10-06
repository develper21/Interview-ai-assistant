import React from 'react';
import Link from 'next/link';
import { LayoutDashboard, Mic, User, LogOut, Bot } from 'lucide-react';

// Yeh component sidebar aur main content area ka layout banayega.
// Har protected page is layout ke andar render hoga.
export default function AppLayout({ children }: { children: React.ReactNode }) {
  // TODO: Add `usePathname` hook to highlight the active link.

  return (
    <div className="flex min-h-screen bg-gray-900 text-white">
      {/* Sidebar Navigation */}
      <aside className="w-64 flex-shrink-0 bg-gray-800 p-6 flex flex-col justify-between">
        <div>
          {/* Logo/App Name */}
          <div className="flex items-center gap-3 mb-10">
            <Bot size={32} className="text-indigo-400" />
            <h1 className="text-2xl font-bold">AI Assistant</h1>
          </div>

          {/* Navigation Links */}
          <nav className="space-y-4">
            <Link href="/dashboard" className="flex items-center gap-3 p-3 rounded-lg text-gray-300 hover:bg-gray-700 hover:text-white transition-colors duration-200">
              <LayoutDashboard size={20} />
              <span>Dashboard</span>
            </Link>
            <Link href="/session" className="flex items-center gap-3 p-3 rounded-lg text-gray-300 hover:bg-gray-700 hover:text-white transition-colors duration-200">
              <Mic size={20} />
              <span>New Session</span>
            </Link>
            <Link href="/profile" className="flex items-center gap-3 p-3 rounded-lg text-gray-300 hover:bg-gray-700 hover:text-white transition-colors duration-200">
              <User size={20} />
              <span>Profile</span>
            </Link>
          </nav>
        </div>

        {/* Logout Button */}
        <div>
          <button className="w-full flex items-center gap-3 p-3 rounded-lg text-red-400 hover:bg-red-500 hover:text-white transition-colors duration-200">
            <LogOut size={20} />
            <span>Logout</span>
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 p-8 overflow-auto">
        {children}
      </main>
    </div>
  );
}
