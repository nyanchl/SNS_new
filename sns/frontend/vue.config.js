const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  publicPath: "/",
  outputDir: "../dist",
  assetsDir: "static",
  // indexPath: "../templates/index.html",
  transpileDependencies: true,
  pages: {
    index: {
      entry: "./src/main.js",
      template: "../templates/index.html",
      filename: "../templates/index.html",
    },
    vuelogin: {
      entry: "./src/main.js",
      template: "../templates/vuelogin.html",
      filename: "../templates/vuelogin.html",
    }
  },
  devServer: {
    host: "localhost",
    hot: "only",
    proxy: {
      "^/api": {
        target: "http://localhost:8080",
        changeOrigin: true,
      },
    },
  },
  chainWebpack: config => {
  config.module
    .rule('vue')
    .use('vue-loader')
    .loader('vue-loader')
    .tap(options => {
      options.compilerOptions = {
        whitespace: 'condense',
        delimiters: ['[[', ']]']
      };
      return options;
    });
  }
})