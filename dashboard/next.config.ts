import type { NextConfig } from "next";

const API_BASE =
  process.env.NEXT_PUBLIC_API_URL || "https://bharatwatch-api.onrender.com";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${API_BASE}/api/:path*`,
      },
    ];
  },
};

export default nextConfig;
