# Glitter Professional Salon Website

A production-ready, two-page static website for Glitter Professional Salon in
Don Galo, Parañaque. The site presents the salon, its complete service menu and
prices, client feedback, opening hours, location, and direct contact actions.

The project uses only HTML5, CSS3, and vanilla JavaScript. It has no framework,
package manager, build process, server, database, or external dependency.

## Folder structure

```text
glitter-professional/
├── index.html
├── services.html
├── css/
│   └── style.css
├── js/
│   └── script.js
├── scripts/
│   └── audit_site.py
├── images/
│   ├── salon-nail-colors.jpg
│   ├── service-nails.jpg
│   ├── service-hair.jpg
│   ├── service-spa.jpg
│   ├── service-lashes.jpg
│   ├── salon-treatment-room.jpg
│   ├── services-collage.jpg
│   ├── *-480.{avif,jpg,webp}
│   ├── *-768.{avif,jpg,webp}
│   ├── *-1080.{avif,jpg,webp}
│   ├── logo-glitter-salon.jpg
│   └── gallery-*.jpg
├── favicon.ico
└── README.md
```

## Open the website locally

1. Download or copy the full `glitter-professional` folder.
2. Keep the folder structure unchanged.
3. Double-click `index.html`, or right-click it and choose a web browser.
4. Use the Services links to open `services.html`.

No installation, compilation, terminal command, local server, or internet
connection is required. Telephone, email, social-media, and directions links
will use the appropriate app or browser when an internet-capable device is
available.

## Manage the salon images

The website includes the real Glitter Professional Salon logo, service photos,
client results, and social artwork supplied by the salon. Principal images use
descriptive filenames:

| Filename | Current image |
| --- | --- |
| `salon-nail-colors.jpg` | Glitter nail-color swatches |
| `service-nails.jpg` | Real matching manicure and pedicure |
| `service-hair.jpg` | Real smooth-hair result |
| `service-spa.jpg` | Real foot-spa treatment |
| `service-lashes.jpg` | Real lash application |
| `salon-treatment-room.jpg` | Real salon treatment graphic and room view |
| `services-collage.jpg` | Salon service collage |

Large images have 480, 768, and 1080 pixel AVIF, WebP, and JPEG derivatives.
The browser chooses the smallest suitable modern format through `<picture>` and
`srcset`; the unnumbered JPEG files preserve the supplied source images. The
small hair and lash photographs are intentionally displayed at restrained sizes
so their 206×206 sources are not visibly stretched.

To update a principal image later, replace its unnumbered JPEG and regenerate
all matching width variants. Then verify the intrinsic `width`, `height`,
`srcset`, `sizes`, and alternative text in the HTML.

For good results:

- Use JPG images in the sRGB color space.
- Aim for at least 1200 pixels on the longest side when a large original is
  available.
- Keep important subjects near the center so responsive cropping works well.
- Compress images before publishing; roughly 150–500 KB per image is a useful
  target for most web photos.
- Keep the filename family consistent across JPEG, WebP, and AVIF variants.
- Update the relevant `alt` text when a replacement image shows something
  materially different.

The HTML contains comments beside the principal salon images to make future
updates easy to find.

## Update contact and business information

Open both `index.html` and `services.html` in a text editor. Search for the old
value and replace every relevant occurrence.

- Phone display: `0917 830 1584`
- Phone link: `tel:09178301584`
- SMS link: `sms:+639178301584`
- Email: `glitterprofessional@gmail.com`
- Address: `994 Quirino Avenue, corner Balagtas Street, Don Galo, Parañaque,
  1700 Metro Manila, Philippines`
- Opening hours: `10:00 AM–9:00 PM`
- Last call: `8:30 PM`
- Messenger: `https://m.me/GlitterProfessional`
- Instagram DM: `https://ig.me/m/glitterprofessional`
- Facebook and Instagram profile URLs
- Google Maps directions URL

Business information also appears in the JSON-LD block inside the `<head>` of
each page. Update that block whenever the public business information changes.
Do not add ratings, awards, coordinates, or claims that cannot be verified.

The site intentionally omits canonical URLs and absolute social-sharing images
until a production domain exists. Never publish `example.com` or another false
canonical.

## Run the structural audit

Python 3 is only needed for the optional development audit; it is not required
to open or deploy the website.

```bash
python3 scripts/audit_site.py
```

The command fails if it finds duplicate IDs, broken local files or fragments,
invalid JSON-LD, images without an `alt` attribute, unsafe new-window links,
inconsistent business details, or a placeholder production domain.

## Update services and prices

Open `services.html` and find the relevant category:

- `id="nails"`
- `id="hair"`
- `id="spa"`
- `id="lashes-brows"`

Each service uses a description-list row:

```html
<div><dt>Service name</dt><dd>₱500</dd></div>
```

Edit the text inside `<dt>` for the service name and `<dd>` for the price. Keep
the Philippine peso symbol (`₱`) and preserve the surrounding HTML. The visible
price notice should remain on the page.

## Deploy to GitHub Pages

1. Create a new GitHub repository.
2. Upload the contents of the `glitter-professional` folder to the repository
   root. `index.html` should be at the top level of the repository.
3. In the repository, open **Settings → Pages**.
4. Under **Build and deployment**, choose **Deploy from a branch**.
5. Select the `main` branch and the `/ (root)` folder, then save.
6. Wait for GitHub to publish the site and open the URL shown in Pages settings.
7. Complete the production-domain checklist below, then upload those edits.

If the repository URL is
`https://username.github.io/glitter-professional/`, the relative file paths
used in this project will continue to work.

## Deploy to Netlify

### Drag-and-drop

1. Sign in to Netlify.
2. Open the Sites area and choose the manual deployment or drag-and-drop option.
3. Drag the complete `glitter-professional` folder into the upload area.
4. Netlify will publish it without a build command.
5. Complete the production-domain checklist below and upload the updated folder.

### Connect a Git repository

1. Push the project to a Git repository.
2. In Netlify, choose **Add new site → Import an existing project**.
3. Select the repository.
4. Leave the build command empty.
5. Set the publish directory to the repository root (`.`).
6. Deploy the site.

## Production-domain checklist

After the final HTTPS domain is selected:

1. Add an absolute canonical URL to each page.
2. Add absolute `og:url` and `og:image` values, plus matching Twitter image
   metadata. Use a properly cropped social preview rather than inventing a
   placeholder URL.
3. Add the homepage URL and representative image to each `BeautySalon` JSON-LD
   block.
4. Create `sitemap.xml`, reference it from `robots.txt`, and submit it through
   the relevant search-console account.
5. Configure the host's HTTPS redirect, preferred hostname, custom 404 page,
   cache rules, and security headers.
6. Test all metadata with social-preview and structured-data tools.
7. Run `python3 scripts/audit_site.py` and a final Lighthouse/axe review.

## Test on mobile and different screen sizes

Test at a minimum:

- 320 px wide phone
- 375–430 px modern phone
- 768 px tablet
- 1024 px small laptop
- 1440 px desktop

In a desktop browser, open its developer tools and enable device emulation.
Check that:

- The mobile navigation opens, closes, and closes with the Escape key.
- The fixed Message, Services, and Directions bar does not cover page content.
- Buttons are easy to tap.
- The page itself has no horizontal scrolling; category-filter rows may scroll
  within their own container on narrow screens.
- Long email and address text wrap cleanly.
- Filters update the URL without jumping, browser Back restores the previous
  category, and every category returns when **All services** is chosen.
- Both pages still show all essential content when JavaScript is disabled.
- The services page prints cleanly, including all categories.

Also test on at least one real phone when possible. Confirm that Messenger,
Instagram DM, SMS, telephone, email, social-profile, and Google Maps links open
the expected app or page. If direct Messenger is not enabled for the page,
replace that CTA with the verified Facebook Page URL.

## Basic accessibility testing

1. Navigate both pages using only the Tab, Shift+Tab, Enter, Space, and Escape
   keys.
2. Confirm that the skip link appears on focus and moves to the main content.
3. Confirm that every interactive element has a visible focus indicator.
4. Open and close the mobile menu with the keyboard.
5. Use the service filters with the keyboard and confirm their selected state is
   announced.
6. Zoom the browser to 200% and confirm that text is readable and the layout does
   not require horizontal scrolling.
7. Enable the operating system's reduced-motion preference and confirm that the
   page remains clear without reveal motion.
8. Run an automated check with Lighthouse, axe DevTools, or WAVE, then review
   any findings manually.
9. Test with a screen reader such as VoiceOver, NVDA, or TalkBack. Check heading
   order, landmarks, link wording, image alternatives, and price reading order.

## Editing notes

- Shared styles are in `css/style.css`.
- Shared interactions are in `js/script.js`.
- JavaScript is an enhancement only; core content and links work without it.
- The dynamic footer year updates automatically when JavaScript is enabled.
- Do not add a booking form unless a real, supported booking service is
  intentionally integrated.
