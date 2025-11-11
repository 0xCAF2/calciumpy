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
          { text: 'API Reference', link: '/api' }
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/0xCAF2/calciumpy' }
    ]
  }
})
