import type { Config } from 'webpack-dev-server';

const config: Config = {
  root: import.meta.dir,
  plugins: [],
  server: {
    middlewareMode: true,
    hmr: true,
  },
};

export default config;
