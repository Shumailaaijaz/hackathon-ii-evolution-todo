import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Disable SWC and use Babel (WSL2 compatibility)
  swcMinify: false,

  // Disable image optimization (WSL2 compatibility)
  images: {
    unoptimized: true,
  },

  // Use webpack instead of Turbopack
  experimental: {
    turbo: undefined,
  },
};

export default nextConfig;
