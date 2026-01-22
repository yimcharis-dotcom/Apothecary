---
title: "Branches · VoloBuilds/create-volo-app"
source: "<https://github.com/VoloBuilds/create-volo-app>"
author:
- "[[VoloBuilds]]"
created: 2026-01-22
tags:
- "clippings"
---


## create-volo-app

== AI-ready Full‑Stack Starter Kit for Vibe Coding, Rapid Prototyping & Production Scaling ==

Create full-stack apps with React, Firebase Auth, and Postgres all set up for you. Start with a full local stack in under 30 seconds and use `connect` when ready - or use the `--full` flag to immediately start with production services hooked up.

[![Demo](https://github.com/VoloBuilds/create-volo-app/raw/main/assets/demo.gif)](https://github.com/VoloBuilds/create-volo-app/blob/main/assets/demo.gif)

## ==Quick Start==

```
# Local development (default) - working app in 30 seconds!
npx create-volo-app my-app

# Full production setup
npx create-volo-app my-app --full
```

**==Full Stack:==**

- ==⚛️ React + TypeScript + Vite==
- ==🎨 Tailwind CSS + ShadCN components==
- ==🔐 Firebase Authentication (Google Sign-In + optional anonymous access)==
- ==🔥 Hono API backend (NodeJS)==
- ==🗄️ Postgres database with Drizzle ORM==

**==Local ==Development== (Default):==**

- ==⚡ Runs UI + Server + DB + Auth on your computer==
- ==🏠 Embedded PostgreSQL database==
- ==🔧 Firebase Auth emulator==
- ==✅ Zero sign-ins or accounts needed==

**==Production (Optional):==**

- ==🌐 Cloudflare Pages + Workers deployment ready==
- ==🗄️ Neon, Supabase, or custom PostgreSQL==
- ==🔐 Production Firebase Auth==

## ==Development Modes==

==Perfect for learning, prototyping, and development:==

```
npx create-volo-app my-app
cd my-app
pnpm run dev
```

- **==Zero authentication required==**
- **==Working app in 30 seconds==**
- ==All services running locally==
- ==Full authentication and database functionality==

==For production-ready apps:==

```
# All production services
npx create-volo-app my-app --full

# Modular: mix local and production services
npx create-volo-app my-app --auth          # Production Firebase + local database
npx create-volo-app my-app --database neon # Production database + local auth
npx create-volo-app my-app --deploy        # Deployment setup + local services
```

==Start local, connect production services later:==

```
# Start with local development
npx create-volo-app my-app
cd my-app

# Connect production services when ready
pnpm connect:auth           # Production Firebase Auth
pnpm connect:database       # Choose database provider
pnpm connect:deploy         # Cloudflare deployment
pnpm connection:status      # Check current setup
```

When setting up Firebase Auth, you'll be asked if you want to allow **anonymous users** to access your app:

- **Enabled**: Users can explore your app immediately, then sign in later to keep their data
- **Disabled**: Users must sign in before accessing any features

==Defaults: Enabled in local/fast mode, disabled in interactive production setup.==

## ==Requirements==

- ==Node.js 20+==
- pnpm

==The CLI will check and guide all other installation as needed.==

## ==Usage Examples==

```
# Local development - instant setup
npx create-volo-app my-app

# Create project in current folder
npx create-volo-app .

# Production with specific database
npx create-volo-app my-app --database neon
npx create-volo-app my-app --database supabase

# Production Firebase Auth only
npx create-volo-app my-app --auth

# Full production setup
npx create-volo-app my-app --full

# Fast mode (minimal prompts)
npx create-volo-app my-app --full --fast

# Connect to existing project
npx create-volo-app --connect --database --path ./my-app
npx create-volo-app --status --path ./my-app
```

## ==Local Services==

==Your local development environment includes:==

- **Database**: Embedded PostgreSQL at `./data/postgres`
- **Auth**: Firebase emulator with demo users
- **Frontend**: `http://localhost:5173`
- **API**: `http://localhost:8787`

All data persists locally between development sessions in the `data` folder within your project

## ==Production Deployment==

```
cd server
pnpm run deploy
```

**Set production environment variables** (use `wrangler` for easier management):

**==Manual Setup:==**

1. Go to [Cloudflare Pages](https://dash.cloudflare.com/pages) → "Create a project"
2. ==Connect your Git repository==
3. Configure build settings:

- **Build command**: `pnpm run build`
- **Output directory**: `ui/dist`

1. ==Deploy automatically on Git push==

**==Add your Pages domain to Firebase:==**

- ==Go to Firebase Console → Authentication → Settings → Authorized domains==
- Add your `*.pages.dev` domain

### ==Automated Deployment==

==For CI/CD, use GitHub Actions or similar with Cloudflare API tokens:==

- **Workers**: Use `wrangler deploy` in your pipeline
- **Pages**: Automatic on Git push (or use Cloudflare API)

## Development

```
git clone https://github.com/VoloBuilds/create-volo-app.git
cd create-volo-app
pnpm install
pnpm run build
node bin/cli.js test-app
```

## ==Roadmap==

- ==Make Auth provider modular; support Supabase and Clerk auth==
- ==Make deployment target more modular (support Docker, different backend TS runtimes like Bun)==
- ==Create UI on top of the CLI for more intuitive project config==
- ==Build optional "commit to git" support to push created volo-app to Git==
- ==Build optional auto-deploy process (git actions + any platform-specific configs)==
- ==Add payment integration for Lemon Squeezy==
- ==Create templates for common usecases==

## ==Testing==

See [`/test`](https://github.com/VoloBuilds/create-volo-app/blob/main/test) for testing tools and instructions.

## ==Support==

- 📖 [Documentation](https://github.com/VoloBuilds/volo-app)
- 🐛 [Issues](https://github.com/VoloBuilds/create-volo-app/issues)
- 💬 [Discussions](https://github.com/VoloBuilds/create-volo-app/discussions)

## License

MIT

## Releases

No releases published

## Packages

No packages published  

## Languages

- [TypeScript 94.7%](https://github.com/VoloBuilds/create-volo-app/search?l=typescript)
- [JavaScript 4.2%](https://github.com/VoloBuilds/create-volo-app/search?l=javascript)
- [Dockerfile 1.1%](https://github.com/VoloBuilds/create-volo-app/search?l=dockerfile)
