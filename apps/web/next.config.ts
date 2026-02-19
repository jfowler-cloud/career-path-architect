import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  transpilePackages: ["@cloudscape-design/components", "@cloudscape-design/global-styles"],
};

export default nextConfig;
