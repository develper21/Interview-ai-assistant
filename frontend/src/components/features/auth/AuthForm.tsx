'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { AtSign, Lock } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/Card';

// Component ko batane ke liye ki yeh 'login' mode mein hai ya 'signup' mein
type AuthMode = 'login' | 'signup';

interface AuthFormProps {
  mode: AuthMode;
}

const AuthForm: React.FC<AuthFormProps> = ({ mode }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const isLoginMode = mode === 'login';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    if (!isLoginMode && password !== confirmPassword) {
      setError('Passwords match nahi kar rahe.');
      setIsLoading(false);
      return;
    }

    // Yahan Supabase logic aayega
    try {
      console.log(`Attempting to ${mode} with:`, { email, password });
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      // if (isLoginMode) {
      //   const { error } = await supabase.auth.signInWithPassword({ email, password });
      //   if (error) throw error;
      // } else {
      //   const { error } = await supabase.auth.signUp({ email, password });
      //   if (error) throw error;
      // }
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : `An error occurred during ${mode}.`;
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-md bg-gray-800 border-gray-700">
      <CardHeader>
        <CardTitle className="text-3xl font-bold text-center">
          {isLoginMode ? 'Welcome Back' : 'Create an Account'}
        </CardTitle>
        <CardDescription className="text-center">
          {isLoginMode ? 'Apne AI assistant se milne ke liye login karein.' : 'Apna free account banayein.'}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-400">Email</label>
            <div className="relative">
              <AtSign className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
              <Input
                id="email"
                type="email"
                placeholder="you@example.com"
                className="pl-10"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-400">Password</label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                className="pl-10"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
          </div>
          {!isLoginMode && (
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-400">Confirm Password</label>
              <div className="relative">
                 <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
                 <Input
                  id="confirmPassword"
                  type="password"
                  placeholder="••••••••"
                  className="pl-10"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                />
              </div>
            </div>
          )}
          {error && <p className="text-sm text-red-500">{error}</p>}
          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? 'Processing...' : (isLoginMode ? 'Login' : 'Create Account')}
          </Button>
        </form>
      </CardContent>
      <CardFooter>
        <p className="w-full text-center text-sm text-gray-400">
          {isLoginMode ? "Account nahi hai? " : "Pehle se account hai? "}
          <Link href={isLoginMode ? '/signup' : '/login'} className="font-semibold text-indigo-400 hover:underline">
            {isLoginMode ? 'Sign Up' : 'Login'}
          </Link>
        </p>
      </CardFooter>
    </Card>
  );
};

export default AuthForm;
