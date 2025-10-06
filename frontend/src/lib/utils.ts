import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * Yeh function conditional CSS classes ko aasani se combine karta hai.
 * Example: cn("base-class", { "active-class": isActive }, "another-class")
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
