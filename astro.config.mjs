// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import starlightThemeBlack from 'starlight-theme-black'

// https://astro.build/config
export default defineConfig({
  site: 'http://juanmartell.online',
  base: '/juan-martell.github.io',
	integrations: [
		starlight({
            plugins: [
        starlightThemeBlack({})
      ],
			title: 'Juan B. Martell',	
			sidebar: [
				{
					label: 'sobre mi',
					items: [
						{ label: 'Experiencia', slug: 'curriculum/experiencia' },
						{ label: 'Formacion', slug: 'curriculum/formacion' },
						{ label: 'contactame', slug: 'curriculum/contacto' },
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
