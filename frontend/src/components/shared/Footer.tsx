import React from 'react';
import Link from 'next/link';
import { Bot } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-gray-900 border-t border-gray-800 mt-auto">
      <div className="container mx-auto py-6 px-6 text-center text-gray-400">
        <div className="flex justify-center items-center gap-2 mb-2">
          <Bot size={20} className="text-gray-500" />
          <p className="font-semibold text-gray-300">AI Interview Assistant</p>
        </div>
        <p className="text-sm">
          © {new Date().getFullYear()} All Rights Reserved.
        </p>
        <div className="mt-3 text-xs space-x-4">
          <Link href="/privacy" className="hover:text-white transition-colors">Privacy Policy</Link>
          <span>•</span>
          <Link href="/terms" className="hover:text-white transition-colors">Terms of Service</Link>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
