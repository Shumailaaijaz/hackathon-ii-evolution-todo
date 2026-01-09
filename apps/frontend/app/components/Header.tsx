/**
 * Header component with logo, login button, and dark mode toggle.
 *
 * Displays the application logo in the top-left corner
 * with navigation links, login button, and dark mode toggle.
 */

"use client";

import Image from "next/image";
import Link from "next/link";
import { useTheme } from "next-themes";
import { MoonIcon, SunIcon } from "@heroicons/react/24/outline";

export function Header() {
  const { theme, setTheme } = useTheme();

  const toggleTheme = () => {
    setTheme(theme === "dark" ? "light" : "dark");
  };

  return (
    <header className="bg-white dark:bg-gray-800 shadow-sm dark:shadow-gray-700">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-3 hover:opacity-80 transition-opacity">
            <Image
              src="/logoh2p2.jpeg"
              alt="Evolution of Todo Logo"
              width={60}
              height={60}
              className="rounded-lg border-2 border-transparent hover:border-blue-500 transition-all"
              priority
            />
            <div className="hidden sm:block">
              <h1 className="text-xl font-bold text-gray-900 dark:text-white">
                Evolution of Todo
              </h1>
              <p className="text-xs text-gray-600 dark:text-gray-300">Phase II - Full-Stack Web App</p>
            </div>
          </Link>

          {/* Navigation and Actions */}
          <div className="flex items-center gap-4">
            <nav className="hidden md:flex items-center gap-2">
              <Link
                href="/tasks"
                className="px-3 py-2 text-gray-700 dark:text-gray-200 hover:text-blue-600 dark:hover:text-blue-400 font-medium transition-colors rounded-md hover:bg-gray-100 dark:hover:bg-gray-700"
              >
                Tasks
              </Link>
              <Link
                href="/"
                className="px-3 py-2 text-gray-700 dark:text-gray-200 hover:text-blue-600 dark:hover:text-blue-400 font-medium transition-colors rounded-md hover:bg-gray-100 dark:hover:bg-gray-700"
              >
                Home
              </Link>
            </nav>

            {/* Dark Mode Toggle */}
            <button
              onClick={toggleTheme}
              className="p-2 rounded-full text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
              aria-label={theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
            >
              {theme === "dark" ? (
                <SunIcon className="h-5 w-5" />
              ) : (
                <MoonIcon className="h-5 w-5" />
              )}
            </button>

            {/* Login Button */}
            <Link
              href="/login"
              className="px-4 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800"
            >
              Login
            </Link>
          </div>
        </div>
      </div>
    </header>
  );
}
