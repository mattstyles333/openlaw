import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://mattstyles333.github.io',
  base: '/openlaw/',
  vite: {
    plugins: [tailwindcss()],
  },
  integrations: [
    starlight({
      title: 'Openlaw',
      description:
        'Always-on law for AI agents. Git markdown. Never retrieved.',
      favicon: '/openlaw-mark.png',
      customCss: ['./src/styles/openlaw.css'],
      social: [
        {
          icon: 'github',
          label: 'GitHub',
          href: 'https://github.com/mattstyles333/openlaw',
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
        {
          label: 'Ops',
          items: [{ label: 'Dashboard', link: '/ops/' }],
        },
      ],
      head: [
        {
          tag: 'meta',
          attrs: {
            property: 'og:image',
            content: 'https://mattstyles333.github.io/openlaw/openlaw-og.png',
          },
        },
        {
          tag: 'link',
          attrs: {
            rel: 'icon',
            href: '/openlaw/openlaw-mark.png',
            type: 'image/png',
          },
        },
      ],
    }),
  ],
});
