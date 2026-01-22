<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# add this to the note you did me for?

Yes. Here is the **updated note** content with the dark‑mode code-block section added; you can paste this over your existing spec note in Obsidian.

***

## Clinical Background Override

This snippet mathematically removes all room for theme-specific tints by forcing absolute RGB values.[^1]

```css
/* NUCLEAR NEUTRALIZER - Force Absolute Neutral White */
.theme-light {
  /* Force absolute white for the main canvas */
  --background-primary: #ffffff !important; 
  /* Force a clean, non-pink secondary panel (sidebar) */
  --background-secondary: #fdfdfd !important;
  --background-primary-alt: #f8f8f8 !important;
  --background-secondary-alt: #f5f5f5 !important;
  
  /* Force "Ink on Paper" text contrast */
  --text-normal: #000000 !important;
  --text-muted: #2a2a2a !important;
  --text-faint: #555555 !important;
}

/* Brighten File Explorer text and icons */
.theme-light .nav-folder-title,
.theme-light .nav-file-title {
  color: #000000 !important;
  font-weight: 500 !important;
  opacity: 1 !important;
}
```
## 🌓 Light vs Dark Compatibility

### 🌞 Light Mode

✔️ Your snippet applies **only** to the light theme.  
✔️ Backgrounds become stark white.  
✔️ Text gets strong high contrast black/charcoal.  
→ **Result:** Looks consistent and readable.

### 🌙 Dark Mode

❗ **Your snippet does _not_ affect dark mode at all.**

- Dark mode keeps Obsidian’s default dark backgrounds and text colors.
    
- If you want a similar “neutral” effect in dark mode, you’ll need a `.theme-dark { … }` block.

``` css
/* SUPER CLEAN LIGHT MODE */
.theme-light {
  --background-primary: #ffffff !important;
  --background-secondary: #ffffff !important;
  --background-primary-alt: #f9f9f9 !important;
  --background-secondary-alt: #f5f5f5 !important;

  --text-normal: #000000 !important;
  --text-muted: #1f1f1f !important;
  --text-faint: #444444 !important;

  --interactive-accent: #000000 !important;  /* buttons, links */
  --accent-strong: #000000 !important;
  --highlight-mixed-color: #dcdcdc !important;  /* selection bg */
}

/* File Explorer: Full visibility */
.theme-light .nav-folder-title,
.theme-light .nav-file-title {
  color: #000000 !important;
  font-weight: 600 !important;
  opacity: 1 !important;
}

/* Breadcrumbs, Tabs, Headers - keep them crisp */
.theme-light .workspace-tab-header-inner,
.theme-light .view-header-title,
.theme-light .breadcrumbs {
  color: #000000 !important;
  opacity: 1 !important;
  font-weight: 500 !important;
}

/* Code Blocks */
.theme-light .cm-s-obsidian pre.HyperMD-codeblock {
  background-color: #f5f5f5 !important;
  color: #111111 !important;
}

/* Tags, Buttons, Links */
.theme-light .tag,
.theme-light a {
  color: #000000 !important;
  background-color: #f0f0f0 !important;
  border: 1px solid #ddd !important;
}

/* Selection Highlight */
.theme-light ::selection {
  background-color: #cce7ff !important;
  color: #000000 !important;
}

```









## PLN / Rainbow Folder Text Only

Keeps rainbow colors on folder titles while removing the heavy background banners.[^2][^3]

```css
/* Remove rainbow banners but keep colored titles (PLN-style) */
.workspace-leaf-content[data-type="file-explorer"] .nav-folder-title,
.workspace-leaf-content[data-type="file-explorer"] .nav-file-title {
  background-color: transparent !important;
  border: none !important;
  box-shadow: none !important;
}

/* Example custom rainbow text colors */
.nav-folder:nth-of-type(10n+1) .nav-folder-title-content { color: #b31b1b !important; } /* Red */
.nav-folder:nth-of-type(10n+2) .nav-folder-title-content { color: #d35400 !important; } /* Orange */
.nav-folder:nth-of-type(10n+3) .nav-folder-title-content { color: #f1c40f !important; } /* Yellow */
.nav-folder:nth-of-type(10n+4) .nav-folder-title-content { color: #27ae60 !important; } /* Green */
.nav-folder:nth-of-type(10n+5) .nav-folder-title-content { color: #2980b9 !important; } /* Blue */
```


## Code Blocks – Light Mode (“Clinical White”)

Blends code into the bright page with a subtle border and classic IDE colors.[^4][^5]

```css
/* LIGHT MODE – Clinical White Code Blocks */
.theme-light .markdown-rendered pre,
.theme-light .markdown-source-view.mod-cm6 .cm-content pre {
  background-color: #fdfdfd !important;  /* Extremely light grey/white */
  border: 1px solid #e5e5e5 !important;
  border-radius: 4px;
}

/* High-contrast syntax highlighting */
.theme-light .token.keyword,
.theme-light .token.atrule,
.theme-light .token.attr-value {
  color: #af00db !important;  /* Sharp purple */
  font-weight: 600;
}

.theme-light .token.string,
.theme-light .token.attr-name {
  color: #a31515 !important;  /* Deep red */
}

.theme-light .token.comment,
.theme-light .token.prolog,
.theme-light .token.doctype,
.theme-light .token.cdata {
  color: #008000 !important;  /* Dark green */
  font-style: italic;
}

.theme-light .token.function,
.theme-light .token.class-name {
  color: #795e26 !important;  /* Dark gold/brown */
}

.theme-light .token.number,
.theme-light .token.boolean {
  color: #098658 !important;  /* Teal */
}
```


## Code Blocks – Dark Mode (“Slate Window”)

Gives dark themes like Glass Robo a clean, slate code window with orange accents.[^6][^7]

```css
/* DARK MODE – Slate Code Blocks */
.theme-dark .markdown-rendered pre,
.theme-dark .markdown-source-view.mod-cm6 .cm-content pre {
  background-color: #2d3436 !important;   /* Deep slate */
  border: 1px solid #3c4043 !important;
  border-radius: 6px;
  padding: 1em;
}

/* Orange keywords / headings */
.theme-dark .token.keyword,
.theme-dark .token.atrule,
.theme-dark .token.important {
  color: #ffb86c !important;              /* Warm orange */
  font-weight: 600;
}

/* Main code text */
.theme-dark code {
  color: #f8f8f2 !important;              /* Light text */
}

/* Softer comments */
.theme-dark .token.comment {
  color: #6272a4 !important;
  font-style: italic;
}
```

You can now keep this note as your **“CSS cookbook”**, and your snippet files (`light-tune.css`, `codeblocks-dark.css`, etc.) can just copy from here.[^8]
