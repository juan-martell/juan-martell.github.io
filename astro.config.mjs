// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
  site: 'http://juanmartell.online',
  base: '/juan-martell.github.io',
	integrations: [
		starlight({
            plugins: [],
			title: 'Juan B. Martell',	      
      customCss: [
        './src/styles/custom.css',
        ],
      logo: {
        light: './src/assets/logo.png',
        dark: './src/assets/logo-dark.png',
        replacesTitle: false,
      },
			sidebar: [
				{
					label: 'Yo',
					items: [
						{ label: 'About me', slug: 'curriculum/contacto' },
						{ label: 'Experiencia', slug: 'curriculum/experiencia' },
						{ label: 'Formacion', slug: 'curriculum/formacion' },
						{ label: 'skills', slug: 'curriculum/skills' }
					],
				},
				{
					label: 'random',
					autogenerate: { directory: 'guides/' },
				},
			],
		}),
	],
});
