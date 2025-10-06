'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { User, AtSign, Lock } from 'lucide-react';

// Sign Up Page ka component
const SignUpPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');

  // Form submit hone par yeh function chalega
  const handleSignUp = (e: React.FormEvent) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setError('Passwords match nahi kar rahe.');
      return;
    }
    setError('');
    // Yahan Supabase ya backend logic aayega
    console.log('Signing up with:', { email, password });
    // TODO: Supabase signup logic implement karein
  };

  return (
    <main className="flex items-center justify-center min-h-screen bg-gray-900 text-white">
      <div className="w-full max-w-md p-8 space-y-8 bg-gray-800 rounded-2xl shadow-lg">
        <div className="text-center">
          <h1 className="text-3xl font-bold tracking-tight">Naya Account Banayein</h1>
          <p className="mt-2 text-gray-400">Interview ki taiyari shuru karein.</p>
        </div>

        {/* Sign Up Form */}
        <form onSubmit={handleSignUp} className="space-y-6">
          {/* Email Input Field */}
          <div className="relative">
            <AtSign className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
            <input
              type="email"
              placeholder="Email Address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full pl-10 pr-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all duration-300"
            />
          </div>

          {/* Password Input Field */}
          <div className="relative">
            <Lock className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full pl-10 pr-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all duration-300"
            />
          </div>

          {/* Confirm Password Input Field */}
          <div className="relative">
            <Lock className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
            <input
              type="password"
              placeholder="Confirm Password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              className="w-full pl-10 pr-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all duration-300"
            />
          </div>

          {/* Error Message */}
          {error && <p className="text-sm text-red-400 text-center">{error}</p>}

          {/* Sign Up Button */}
          <button
            type="submit"
            className="w-full group flex items-center justify-center gap-2 py-3 px-4 text-lg font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-indigo-500 transition-transform duration-300 transform hover:scale-105"
          >
            Create Account
            <User className="transition-transform duration-300 group-hover:scale-110" size={24} />
          </button>
        </form>

        {/* Login Link */}
        <p className="text-center text-gray-400">
          Pehle se account hai?{' '}
          <Link href="/login" className="font-medium text-indigo-400 hover:text-indigo-300">
            Login karein
          </Link>
        </p>
      </div>
    </main>
  );
};

export default SignUpPage;
