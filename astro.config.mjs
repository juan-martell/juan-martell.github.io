// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import starlightSidebarTopics from 'starlight-sidebar-topics';

// https://astro.build/config
export default defineConfig({
  site: 'http://juanmartell.online',
  base: '/juan-martell.github.io',
	integrations: [
		starlight({
      plugins: [        
            starlightSidebarTopics([
            {
              label: 'Curriculum',
              link: '/curriculum/contacto',
              icon: 'information',
              items: ['curriculum/contacto', 'curriculum/experiencia', 'curriculum/formacion', 'curriculum/skills'],
            },
            {
              label: 'Notas',
              link: '/notas/facultad/matplotlib',
              icon: 'pen',
              items: [
                {
                label: 'Facultad',
                autogenerate: { directory: 'notas/facultad'},
                },
                {
                label: 'Otros',
                autogenerate: { directory: 'notas/otros' }, 
                },
              ],
            },
      ]),
      ],
		  title: 'Juan B. Martell',	
      pagefind: false,
      customCss: [
        './src/styles/custom.css',
        ],
      logo: {
        light: './src/assets/logo.png',
        dark: './src/assets/logo-dark.png',
        replacesTitle: false,
      },
		}),
	],
});
