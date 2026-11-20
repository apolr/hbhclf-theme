# Elementor exit playbook

How we moved hbhclf.org off Elementor and Elementor Pro onto a custom WordPress block theme, with no downtime, no broken links and no paid plugins. Use it as a checklist for any similar WordPress site.

**Reference project:** Hamilton Black Health Community Leaders Forum (hbhclf.org), November 2026
**Result:** custom block theme (`hbhclf`, kept in GitHub), free plugins only (Fluent Forms, MailPoet, Cloudflare Turnstile), Elementor and Elementor Pro switched off.

---

## 0. Ground rules

- **Never edit the live look until switch-over day.** Build everything as drafts, on staging, or "behind" Elementor (see step 6).
- **Keep every web address the same.** Put the new design into the existing pages and posts. Don't create replacement pages with new addresses. This protects Google rankings and shared links.
- **The client approves each decision before it is implemented.** Show screenshots or staging links first.
- **Take a host backup right before the switch, and know the undo path.** The undo is: reactivate Elementor and Elementor Pro, then switch back to the old theme.

---

## 1. Audit the existing site (read only)

1. List every **published page and post**, noting which ones are built with Elementor (post meta `_elementor_edit_mode = builder`).
2. List the **Elementor Pro Theme Builder parts**: header, footer, single post, archive and 404 templates. These override any theme while Elementor Pro is active.
3. List every **form**:
   - Elementor forms and their stored submissions.
   - Other form plugins and which pages use them.
   - Where each form's notifications are sent.
4. List **newsletter tools** (lists, subscriber counts, sign-up forms and pop-ups).
5. Record **brand assets**: logo, colours (Elementor global colours live in the kit CSS, `post-<kit-id>.css`), fonts, pattern images and hero banners.
6. Note **page-specific design details** worth keeping: shape dividers (waves), header photos, gradient overlays and image shapes. Elementor stores these in `wp-content/uploads/elementor/css/post-<id>.css`.
7. Find **leftover template pages** from the theme or starter kit, such as "Welcome", "Clients" or "Alt Home". These are often still published.

## 2. Build the block theme

1. Start a theme with `style.css`, `theme.json` (v3), `functions.php`, `templates/`, `parts/` and `assets/`.
2. **Enqueue `style.css` yourself.** A block theme does not load it automatically. This was the biggest early bug: the theme looked unstyled until we added `wp_enqueue_style` with a `filemtime` version for cache busting.
3. Put brand colours, fonts and button styles into `theme.json`, and add brand CSS variables in `style.css`.
4. Header part:
   - Site logo.
   - Navigation block with explicit links, so it doesn't depend on old Elementor menus.
   - Donate button and social link.
   - Sticky header, with an offset for the admin bar.
   - Hamburger menu below about 1100px.
5. Footer part: logo, quick links, newsletter sign-up, copyright and a Privacy Policy link.
6. Templates:
   - `front-page.html`.
   - `page.html`: full width, with the title supplied by the content.
   - `single.html`: narrow reading column with the date.
   - `archive.html`, `index.html` and `404.html`.
7. Motion and finish, in `assets/js` and `assets/css`:
   - hero slider with dots and pause on hover
   - fade-up reveal on scroll
   - floating decorative shapes and image hover zoom
   - scrolling logo strip
   - wavy section dividers using a CSS mask, with each section tucked under the one above
   - organic photo shapes
   - styled mobile menu overlay
   - back-to-top button
   - photo lightbox for post galleries
   - always respect `prefers-reduced-motion`
8. SEO basics in `inc/seo.php`:
   - meta description (from the excerpt, else the first paragraph)
   - Open Graph and Twitter tags
   - JSON-LD for the organization, website and articles
   - noindex on search results
   - an `llms.txt` file
9. **Legacy template fix.** After Elementor is off, pages still carry `_wp_page_template = elementor_header_footer`. WordPress then refuses to save them with "Invalid page template". To fix this, add `templates/elementor_header_footer.html` (a copy of `page.html`) and register it in `theme.json` under `customTemplates`.
10. **MailPoet in a block template.** A Shortcode block runs `wpautop` over the form and breaks its built-in CSS with stray `<p>` and `<br>` tags. Add a `render_block` filter that returns `do_shortcode()` for `[mailpoet_form ...]` without `wpautop`.
11. Keep the theme in Git and ship numbered zip builds (0.1.0, 0.2.0 and so on). Each zip contains: `assets`, `functions.php`, `inc`, `parts`, `style.css`, `templates`, `theme.json`.

## 3. Rebuild the content as blocks

1. Generate block markup for each page from a script (we used Python helpers in `tools/`), so pages can be rebuilt consistently.
2. Convert each Elementor post's content into clean blocks:
   - a lead image
   - text with spans and empty links removed
   - a gallery with every image and its alt text
3. Write **search descriptions** (excerpts) for every page.
4. Load new pages as **drafts** first, such as "About (new design)", for review.
5. After every write, **check the database copy matches the local file** (MD5 of `post_content`).

## 4. Forms and newsletter (free tools)

1. **Fluent Forms (free)** replaces Elementor forms:
   - contact
   - newcomer questionnaire
   - volunteer registration with a file upload
   - event registrations
2. For each form:
   - Add an admin notification to the organization's inbox, with **Reply-To set to the sender's email field**.
   - Give the button clear text.
   - Turn on the honeypot.
3. **Cloudflare Turnstile (free, managed mode)**:
   - Create a widget for the live and staging domains.
   - Paste the site key and secret key into Fluent Forms global settings yourself. Never share the secret in chat.
   - Add the Turnstile field to every public form.
4. **MailPoet**:
   - Point the sign-up form at the real list.
   - Rename it and turn off any pop-up.
   - Replace any template wording such as "Dive in! ... fitness journey".
   - Remove the template background image.
5. **Export old Elementor submissions** (Elementor → Submissions → Export) **before** turning Elementor off. Store the file privately, because it contains personal data.

## 5. Staging review

1. Create a staging copy. On SiteGround: Site Tools → WordPress → Staging.
2. On staging only:
   1. Install and activate the theme.
   2. **Deactivate Elementor and Elementor Pro.** Otherwise Theme Builder keeps drawing the old header and footer, and staging "looks like the live site".
   3. Publish "Home (new design)" and set it as the homepage.
   4. Preview the other drafts.
3. Clear the host cache and hard refresh (Cmd+Shift+R) after every theme upload.
4. Iterate with the client: brand colours, banner, waves, spacing, inner pages, mobile menu and footer.
5. If staging needs fresh content, delete it and recreate it from live. Then repeat step 2 (theme, Elementor off, homepage).

## 6. Switch-over day

Pick a quiet time, and expect about 30 to 45 minutes.

1. **Backup:** take an on-demand host backup with a clear name, for example `ClientName-ElementorMigration`.
2. **Load the new content invisibly.**
   - Write the new block content and excerpts into the **existing** page IDs: Home, About, Programs, Contact and so on.
   - While Elementor is active, it keeps rendering its own saved design, so visitors see no change. Confirm this by loading a page and checking it still has `data-elementor-type="wp-page"`.
   - Check every page by MD5.
3. **Visible switch (client, back to back):**
   1. Appearance → Themes → upload the theme → Activate.
   2. Plugins → Deactivate **Elementor Pro**, then **Elementor**.
   3. Purge the host cache.
4. **Publish** any brand-new pages, such as a volunteer page under its parent.
5. **Verify on the live site:**
   - every page returns 200 and uses the new theme
   - forms are present with Turnstile
   - newsletter in the footer
   - no broken images
   - desktop and phone views
   - send one real test message through the contact form
6. Fix anything found straight away, by shipping a new theme zip or editing page content.

## 7. After the switch

1. **Trash practice drafts and duplicate "(new design)" drafts.** Use trash, not permanent delete, because it can be restored for 30 days.
2. **Deal with leftover Elementor-era pages** that are still published:
   - Starter-kit or template pages (often lorem ipsum, or raw Elementor CSS showing as text): unpublish or trash them.
   - Past event registration pages: set to private, or redirect to the event's news post.
3. **Publish a Privacy Policy** (forms plus newsletter means personal data). Link it in the footer and from the newsletter form.
4. Set the contact map to the real street address, and make it responsive (full content width, shorter on phones).
5. After 2 to 4 quiet weeks:
   - **Delete** the Elementor and Elementor Pro plugins.
   - Cancel or don't renew the Elementor Pro licence.
   - Optionally remove the `wp-content/uploads/elementor` folder and the Elementor library templates.
   - Keep the backup until then.
6. Optional later: put Cloudflare in front of the site for an extra security shield and easier DNS management. It isn't required, because the host's caching and CDN are enough for most small sites.

---

## Gotchas we hit (and the fix)

| Symptom | Cause | Fix |
|---|---|---|
| New theme installed but staging looks unchanged | Old theme still active, or Elementor Pro Theme Builder overriding | Activate the theme and deactivate Elementor and Elementor Pro on staging |
| Theme renders unstyled, no logo, messy menu | Block theme didn't enqueue `style.css` | `wp_enqueue_style( get_stylesheet_uri() )` with a `filemtime` version |
| Page edits fail: "Invalid page template" | Pages still set to `elementor_header_footer` | Add a matching template file and register it in `theme.json` `customTemplates` |
| Newsletter form shows a big gap and broken styling | `wpautop` from the Shortcode block mangles MailPoet's `<style>` and adds `<br>` | `render_block` filter that returns a clean `do_shortcode()` |
| White strips between coloured sections | Reveal animation moved whole sections | Animate only the content inside each section |
| Wave hides part of an event banner | Mask applied to a hero holding artwork | No wave on the hero; keep the banner's full aspect ratio |
| Map stuck to the left on wide screens | iframe is an inline element, so auto margins don't centre it | Wrap it in a block-level `.hb-map` container, full content width, with responsive height |
| Text like "/*! elementor ... */" showing on a page | Elementor-only page rendered without Elementor | Rebuild the page as blocks, or unpublish it |
| Photo file not found | Filename contains an invisible zero-width character | URL-encode it (`%E2%80%8B`) |

## Tools used

- **WordPress connection (MCP):** read-only SQL for audits and checks, plus create and update post for content.
- **Local test site:** WordPress with SQLite, served with `php -S`, and Playwright screenshots at desktop and phone sizes before every release.
- **Git and GitHub** for the theme source, and numbered zips for installs.
- **Host:** SiteGround (staging, backups, Speed Optimizer cache).
- **Free plugins:** Fluent Forms, MailPoet, Cloudflare Turnstile.
