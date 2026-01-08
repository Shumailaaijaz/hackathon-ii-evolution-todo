import Image from "next/image";
import Link from "next/link";

export default function Home() {
  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden">
      {/* Hero Background Image */}
      <div className="absolute inset-0 z-0">
        <Image
          src="/hero-image-h2p2.jpeg"
          alt="Hero Background"
          fill
          className="object-cover"
          priority
          quality={100}
        />
        {/* Overlay for better text readability */}
        <div className="absolute inset-0 bg-black/40" />
      </div>

      {/* Logo in top-left corner */}
      <Link
        href="/"
        className="absolute top-6 left-6 z-20 hover:opacity-80 transition-opacity"
      >
        <Image
          src="/logoh2p2.jpeg"
          alt="Evolution of Todo Logo"
          width={80}
          height={80}
          className="rounded-lg shadow-lg"
          priority
        />
      </Link>

      {/* Main Content */}
      <main className="relative z-10 text-center px-4 max-w-4xl">
        <h1 className="text-6xl font-bold text-white mb-6 drop-shadow-lg">
          Evolution of Todo
        </h1>
        <p className="text-2xl text-white/90 mb-12 drop-shadow-md">
          Phase II - Full-Stack Web Application
        </p>
        <div className="flex gap-4 justify-center flex-wrap">
          <Link
            href="/tasks"
            className="px-8 py-4 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-all transform hover:scale-105 shadow-lg"
          >
            Go to Tasks
          </Link>
          <a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            className="px-8 py-4 bg-white/90 text-gray-800 rounded-lg font-medium hover:bg-white transition-all transform hover:scale-105 shadow-lg"
          >
            View on GitHub
          </a>
        </div>
      </main>
    </div>
  );
}
