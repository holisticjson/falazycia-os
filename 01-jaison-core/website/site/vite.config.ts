import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  base: './',
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        blogSeo: resolve(__dirname, 'blog-seo.html'),
        blogAutomatyzacja: resolve(__dirname, 'blog-automatyzacja.html'),
        blogMake: resolve(__dirname, 'blog-make.html'),
        politykaPrywatnosci: resolve(__dirname, 'polityka-prywatnosci.html'),
        caseStudies: resolve(__dirname, 'case-studies.html'),
        opinia: resolve(__dirname, 'opinia.html'),
        oranzada: resolve(__dirname, 'oferty/oranzada/index.html'),
      }
    }
  }
});
