import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Speed up dev/HMR by avoiding loading entire icon libraries
  experimental: {
    optimizePackageImports: ["@heroicons/react"],
  },
  modularizeImports: {
    "@heroicons/react/24/outline": {
      transform: "@heroicons/react/24/outline/{{member}}",
    },
  },
};

export default nextConfig;
