/** @type {import('next').NextConfig} */
const nextConfig = {
  webpack: (config, { isServer }) => {
    // PDF.js worker config
    config.resolve.alias.canvas = false;

    return config;
  },
};

module.exports = nextConfig; 