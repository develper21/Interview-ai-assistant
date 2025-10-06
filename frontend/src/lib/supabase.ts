import { createClient } from '@supabase/supabase-js';

// Environment variables se Supabase URL aur Key le rahe hain
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

// Check karte hain ki variables set hain ya nahi
if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('Supabase URL and Anon Key must be defined in .env.local');
}

// Supabase client banakar export kar rahe hain
export const supabase = createClient(supabaseUrl, supabaseAnonKey);
