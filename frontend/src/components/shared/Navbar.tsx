import React from 'react';
import Link from 'next/link';
import { Bot } from 'lucide-react';
import { Button } from '@/components/ui/Button';

const Navbar = () => {
  return (
    <header className="py-4 px-6 md:px-10 bg-gray-900/80 backdrop-blur-sm sticky top-0 z-50 border-b border-gray-800">
      <div className="container mx-auto flex justify-between items-center">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2">
          <Bot size={28} className="text-indigo-400" />
          <span className="text-xl font-bold text-white">AI Assistant</span>
        </Link>

        {/* Action Buttons */}
        <div className="flex items-center gap-4">
          <Link href="/login">
            <Button variant="ghost" className="text-gray-300 hover:text-white">
              Login
            </Button>
          </Link>
          <Link href="/signup">
            <Button>
              Sign Up
            </Button>
          </Link>
        </div>
      </div>
    </header>
  );
};

export default Navbar;
