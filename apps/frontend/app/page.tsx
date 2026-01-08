import Link from "next/link";

export default function Home() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
      <main className="text-center px-4">
        <h1 className="text-5xl font-bold text-gray-900 mb-4">
          Evolution of Todo
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Phase II - Full-Stack Web Application
        </p>
        <div className="flex gap-4 justify-center">
          <Link
            href="/tasks"
            className="px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors"
          >
            Go to Tasks
          </Link>
          <a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            className="px-6 py-3 bg-gray-100 text-gray-700 rounded-lg font-medium hover:bg-gray-200 transition-colors"
          >
            View on GitHub
          </a>
        </div>
      </main>
    </div>
  );
}
