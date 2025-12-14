# Frontend - Cyber-SOP Assistant

React + TypeScript frontend with Perplexity-style UI for the Cyber-SOP Assistant.

## Features

- **Fixed Layout**: No page scroll, only chat scrolls
- **Dark Theme**: Modern, clean interface
- **Real-time Chat**: Instant responses with source citations
- **Sidebar Navigation**:
  - Recent Chats
  - Resources Hub (NCRP, CEIR, TAFCOP, etc.)
  - Police Locator
  - API Documentation
- **Responsive**: Optimized for desktop

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create .env file:
```bash
copy .env.example .env
```

3. Start dev server:
```bash
npm run dev
```

4. Open browser:
```
http://localhost:5173
```

## Project Structure

```
src/
├── components/
│   ├── layout/
│   │   ├── Sidebar.tsx           # Left sidebar
│   │   └── SidebarSection.tsx    # Sidebar sections
│   ├── chat/
│   │   ├── ChatWindow.tsx        # Main chat interface
│   │   ├── MessageBubble.tsx     # Message display
│   │   └── Composer.tsx          # Input composer
│   ├── resources/
│   │   └── ResourceList.tsx      # Resources display
│   └── police/
│       └── NearbyPolice.tsx      # Police locator
├── hooks/
│   └── useChat.ts                # Chat state management
├── api/
│   └── client.ts                 # API client
├── App.tsx                        # Main app component
└── index.css                      # Global styles
```

## Customization

### Styling

Edit `src/index.css` to customize:
- Colors (CSS variables at top)
- Layout dimensions
- Component styles

### API Endpoint

Edit `.env`:
```env
VITE_API_URL=http://localhost:8000/api
```

## Tech Stack

- React 18.3.1
- TypeScript 5.3.3
- Vite 5.0.5
- Axios (HTTP client)
- Lucide React (Icons)

## Build for Production

```bash
npm run build
```

Output in `dist/` directory.
