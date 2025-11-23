import {NextConfig} from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "images.unsplash.com",
      },
      {
        protocol: "https",
        hostname: "unsplash.com",
      },
      {
        protocol: "https",
        hostname: "rawpixel.com",
      },
      {
        protocol: "https",
        hostname: "pxhere.com",
      },
        {
        protocol: "https",
        hostname: "skylum.com",
      },
    ],
  },
};

export default nextConfig;
