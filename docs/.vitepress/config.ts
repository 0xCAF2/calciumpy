import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "calciumpy | Interpreter in Python",
  description: "A Python library to consume JSON and run.",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Guides', link: '/guides' },
      { text: 'API Reference', link: '/api' }
    ],

    sidebar: [
      {
        text: 'Contents',
        items: [
          { text: 'Get Started', link: '/guides' },
          { text: 'About Commands', link: '/commands' },
          { text: 'Expressions', link: '/expressions' },
          { text: 'API Reference', link: '/api' }
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/0xCAF2/calciumpy' }
    ],

    externalLinkIcon: true,
  },
  locales: {
    root: {
      label: "English",
      lang: "en",
    },
    ja: {
      label: "日本語",
      lang: "ja",
      title: "calciumpy | インタプリタ",
      description:
        "JSONを解釈して「実行」するための Python ライブラリです。",
      themeConfig: {
        nav: [
          { text: 'ホーム', link: '/ja/' },
          { text: 'ガイド', link: '/ja/guides' },
          { text: 'API リファレンス', link: '/ja/api' }
        ],

        sidebar: [
          {
            text: '目次',
            items: [
              { text: 'はじめに', link: '/ja/guides' },
              { text: 'コマンドについて', link: '/ja/commands' },
              { text: '式の表現', link: '/ja/expressions' },
              { text: 'API リファレンス', link: '/ja/api' }
            ]
          }
        ],
      },
    },
  },
  base: "/calciumpy/",
})
