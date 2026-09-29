# Zichuan Wang's homepage

An English academic homepage for https://zichuan517.github.io/.
Built with HTML and CSS. No installation or build step is required.

## Preview

Open `index.html` in a browser. The page also works from a static web server.

## Edit

- `index.html`: profile information, links, navigation, and section content.
- `styles.css`: typography, spacing, colors, and responsive layouts.
- `me.jpg`: the supplied profile image, preserved unchanged.

Course PDFs live in `uploads/` and are linked from the Courses section.
Add further content inside each section's `section-body` in `index.html`.
When adding a PDF, upload the file and link its exact, case-sensitive path.
The GitHub profile URL is based on the supplied homepage username.

## Publish on GitHub Pages

1. Create or open the repository `zichuan517.github.io` under the `zichuan517` account.
2. Upload `index.html`, `styles.css`, `me.jpg`, `.nojekyll`, and the complete `uploads/` folder to the root of the `main` branch.
3. In **Settings → Pages**, select **Deploy from a branch**, then **main** and **/ (root)**, and save.
4. Wait for deployment to complete, then visit https://zichuan517.github.io/.

If that repository already contains a website, review its files before
replacing them. Local changes are not automatically published.

Official instructions: https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site

The layout and section structure are inspired by https://wzyustc.github.io/;
the HTML and CSS here are independently implemented.
