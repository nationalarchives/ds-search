const path = require("path");

module.exports = {
  entry: {
    main: "./src/scripts/main.js",
    analytics: "./src/scripts/analytics.js",
    "catalogue-results": "./src/scripts/catalogue-results.js",
  },
  mode: "production",
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ["@babel/preset-env"],
          },
        },
      },
    ],
  },
  output: {
    path: path.resolve(__dirname, "app/static"),
    filename: "[name].min.js",
  },
  devtool: "source-map",
};
