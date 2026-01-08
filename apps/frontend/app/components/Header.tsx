/**
 * Header component with logo.
 *
 * Displays the application logo in the top-left corner
 * with navigation links.
 */

"use client";

import Image from "next/image";
import Link from "next/link";

export function Header() {
  return (
    <header className="bg-white shadow-sm">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-3 hover:opacity-80 transition-opacity">
            <Image
              src="/logoh2p2.jpeg"
              alt="Evolution of Todo Logo"
              width={50}
              height={50}
              className="rounded-lg"
              priority
            />
            <div className="hidden sm:block">
              <h1 className="text-xl font-bold text-gray-900">
                Evolution of Todo
              </h1>
              <p className="text-xs text-gray-600">Phase II - Full-Stack Web App</p>
            </div>
          </Link>

          {/* Navigation */}
          <nav className="flex items-center gap-4">
            <Link
              href="/tasks"
              className="px-4 py-2 text-gray-700 hover:text-blue-600 font-medium transition-colors"
            >
              Tasks
            </Link>
            <Link
              href="/"
              className="px-4 py-2 text-gray-700 hover:text-blue-600 font-medium transition-colors"
            >
              Home
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
}
