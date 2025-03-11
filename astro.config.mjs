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
              link: '/curriculum/',
              icon: 'information',
              items: ['curriculum/contacto', 'curriculum/experiencia', 'curriculum/formacion', 'curriculum/skills'],
            },
            {
              label: 'Notas',
              link: '/guides/',
              icon: 'pen',
              items: [
                {
                label: 'Facultad',
                items: ['guides/matplotlib', 'guides/panda'],
                },
                {
                label: 'Random',
                items: ['guides/links', "guides/blind_sqli", "guides/sql_injection"],
                },
              ]
            },
      ]),
      ],
		  title: 'Juan B. Martell',	      
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
