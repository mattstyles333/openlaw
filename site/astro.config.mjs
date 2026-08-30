import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://mattstyles333.github.io',
  base: '/canon/',
  integrations: [
    starlight({
      title: 'Canon',
      description:
        'Always-on law for AI agents. Git markdown. Never retrieved.',
      favicon: '/canon-mark.png',
      customCss: ['./src/styles/canon.css'],
      social: [
        {
          icon: 'github',
          label: 'GitHub',
          href: 'https://github.com/mattstyles333/canon',
        },
      ],
      sidebar: [
        {
          label: 'Docs',
          items: [
            { label: 'Overview', slug: 'docs' },
            { label: 'Why', slug: 'docs/why' },
            { label: 'Onboarding', slug: 'docs/onboarding' },
            { label: 'Harness attach', slug: 'docs/harness' },
            { label: 'Security', slug: 'docs/security' },
            { label: 'MCP / Portainer', slug: 'docs/mcp' },
            { label: 'Status', slug: 'docs/status' },
          ],
        },
      ],
      head: [
        {
          tag: 'meta',
          attrs: {
            property: 'og:image',
            content: 'https://mattstyles333.github.io/canon/canon-og.png',
          },
        },
        {
          tag: 'link',
          attrs: {
            rel: 'icon',
            href: '/canon/canon-mark.png',
            type: 'image/png',
          },
        },
      ],
    }),
  ],
});
