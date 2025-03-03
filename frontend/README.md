## Getting Started

First, run the development server:

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Project Structure

```
├── public
│   ├── images
│   ├── javascripts
│   └── styles
├── app
│   ├── (auth)
│   │   └── sign-in
│   │       └── page.tsx
│   ├── (protected)
│   │   ├── chat
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── dashboard
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── knowledge
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   └── studio
│   │       ├── layout.tsx
│   │       └── page.tsx
│   ├── auth
│   │   ├── AuthContext.tsx
│   │   └── withRole.tsx
│   ├── layout.tsx
│   ├── page.tsx
│   ├── providers.tsx
│   └── styles
│       └── globals.css
├── components
│   ├── chat
│   │   ├── ChatWindow.tsx
│   │   └── Message.tsx
│   ├── common
│   │   ├── ExpandableCard.tsx
│   │   ├── Footer.tsx
│   │   ├── Header.tsx
│   │   ├── LanguageSwitcher.tsx
│   │   ├── Nav.tsx
│   │   └── Sidebar
│   │       ├── ChatSidebar.tsx
│   │       ├── DashboardSidebar.tsx
│   │       └── StudioSidebar.tsx
│   ├── dashboard
│   │   ├── SystemHealth.tsx
│   │   └── UserStats.tsx
│   ├── knowledge
│   │   └── ..
│   └── studio
│       ├── AgentManagement.tsx
│       └── KnowledgeBaseManagement.tsx
└── i18n
    ├── README.md
    ├── settings.ts     # i18n configuration file
    ├── index.ts        # i18n initialization file
    ├── en/             
    │   └── common.json # English translations
    ├── zh/             
    │   └── common.json # Chinese translations
    └── de/             
        └── common.json # German translations
```
