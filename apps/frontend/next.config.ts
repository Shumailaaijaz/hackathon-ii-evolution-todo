import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Disable image optimization (WSL2 compatibility)
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
