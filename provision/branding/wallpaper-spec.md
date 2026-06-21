# Stars & Pines — Wallpaper & Branding Specification

## Desktop Wallpaper
- **Resolution:** 1920x1080 (primary), 1366x768 (secondary), 2560x1440 (wide)
- **Style:** Minimal luxury hospitality, modern Himalayan lodge
- **Mood:** Mountain retreat, boutique hospitality, warm and grounding

## Visual Elements
- **Background:** Dark forest green (#1D2C1B) or deep night (#0B0D0B)
- **Mountain silhouette:** Subtle Himalayan range in lower half
- **Stars:** Scattered gold/white stars in upper portion
- **Wordmark:** "Stars & Pines · Crank's Ridge" — bottom center, subtle gold (#D6B26E)
- **NO corporate clip art, NO bright neon colors, NO busy patterns**

## Color Palette
| Color | Hex | Usage |
|---|---|---|
| Forest Green | `#1D2C1B` | Backgrounds, dark areas |
| Night | `#0B0D0B` | Deep dark backgrounds |
| Warm Beige | `#F8F5F0` | Light text, cards |
| Off White | `#FCFAF6` | Text on dark |
| Gold Accent | `#D6B26E` | Stars, highlights, wordmark |
| Charcoal | `#161411` | Body text |

## Suggested Wallpaper Sources
- Unsplash: search "himalayan mountains night stars", "pine forest fog", "mountain lodge dark"
- Pexels: "mountain silhouette", "night sky stars"
- Place downloaded images in: `~/StarsAndPines/Media/wallpapers/`

## Login Screen (LightDM Greeter)
- Use same visual as desktop wallpaper
- Add subtle "Stars & Pines" wordmark overlay
- Config: `/etc/lightdm/lightdm-gtk-greeter.conf`
  ```ini
  background=/path/to/starsandpines-wallpaper.png
  ```

## GTK Theme
- MX Linux uses Adwaita by default — keep dark variant
- Icon theme: Adwaita (or Numix for custom)
- Accent color: Forest Green

## Firefox Theme
- Dark mode enabled
- Custom CSS for `userChrome.css`:
  - Hide tab bar (use app tabs)
  - Custom toolbar with ops links
  - Forest green accent color

## Desktop Icons (Optional)
- Custom SVG icons in `~/.local/share/icons/`
- Stars & Pines icon set: gold star + pine tree silhouette
- Colors: `#D6B26E` on dark green `#1D2C1B`

## Wallpaper Download Links (Free/CC0)
```bash
# Night mountain wallpaper
wget -O ~/StarsAndPines/Media/wallpapers/desktop.png \
  "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=80"

# Pine forest
wget -O ~/StarsAndPines/Media/wallpapers/forest.png \
  "https://images.unsplash.com/photo-1448375240586-882707db888b?w=1920&q=80"
```