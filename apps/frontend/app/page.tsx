import Link from "next/link";
import { Header } from "./components/Header";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <div className="relative flex min-h-[calc(100vh-80px)] items-center justify-center overflow-hidden flex-grow">
        {/* Hero Background Image */}
        <div className="absolute inset-0 z-0">
          <div
            className="absolute inset-0 bg-cover bg-center"
            style={{ backgroundImage: "url('/hero-image-h2p2.jpeg')" }}
          />
          {/* Overlay for better text readability */}
          <div className="absolute inset-0 bg-black/40" />
        </div>

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
    </div>
  );
}
