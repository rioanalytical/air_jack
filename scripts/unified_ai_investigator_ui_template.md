# UI Template Description: Morgan Stanley | Unified AI Investigator — Deep Research Interface

---

## OVERVIEW

A clean, professional enterprise AI chat interface with a two-panel layout: a narrow left sidebar for navigation and a wide main content area. The color scheme is **dark navy (#1a2744 or similar) for the header/sidebar accents**, with a **light gray (#f0f2f5) page background** and **white (#ffffff) card surfaces**.

---

## GLOBAL LAYOUT

```
┌──────────────────────────────────────────────────────────┐
│  HEADER (full width, dark navy, ~50px tall)              │
├────────┬─────────────────────────────────────────────────┤
│        │                                                  │
│ LEFT   │         MAIN CONTENT AREA                        │
│ SIDEBAR│         (centered card, max-width ~900px)        │
│ ~80px  │                                                  │
│        │                                                  │
├────────┴─────────────────────────────────────────────────┤
│  BOTTOM INPUT BAR (full width, light gray bg)            │
└──────────────────────────────────────────────────────────┘
```

---

## 1. HEADER BAR

- **Full-width**, fixed at top, dark navy background (`#0d1f3c`)
- **Left side:** Two text elements separated by a vertical pipe `|`
  - `Morgan Stanley` — white, bold, sans-serif (~16px)
  - `✦ Unified AI Investigator` — white, with a small diamond/sparkle icon prefix (~16px)
- **Right side:** A circular `?` help icon, white outlined, right-aligned with padding

**Streamlit CSS hint:** Use `st.markdown` with custom HTML or inject CSS via `st.markdown("<style>...</style>", unsafe_allow_html=True)` to style `[data-testid="stHeader"]`.

---

## 2. LEFT SIDEBAR

- **Narrow**, ~80px wide, light white/gray background with subtle right border
- **4 icon-buttons stacked vertically**, each with:
  - A centered icon (outline style)
  - A short label below the icon (~11px, gray)
  - No active/hover highlight in default state
- **Items (top to bottom):**
  1. `＋` circle icon → label: **"New Chat"**
  2. Clock/history icon → label: **"History"**
  3. Grid/checklist icon → label: **"Agents"**
  4. Bell icon → label: **"Alerts"**
- Items are spaced evenly with generous top padding (~20px between each)

**Streamlit hint:** Use `st.sidebar` with `st.button()` styled via CSS to appear icon-only with labels beneath.

---

## 3. MAIN CONTENT AREA

- **Background:** Light gray (`#f0f2f5`)
- **Content card:** White, centered, with padding (~40px), subtle box shadow, max-width ~860px, margin auto

### 3a. Card Header (Message/Step Header)

- **Icon:** Small diamond sparkle (`✦`) in dark navy, inline
- **Title:** `"Deep Research"` — dark navy, bold, ~16px
- **Timestamp:** `01:51 PM` — light gray, regular weight, ~13px, inline after title with space

---

### 3b. Step 1 Section

- **Label:** `"Step 1"` — dark navy, bold, ~14px, left-aligned, vertically centered with the buttons
- **Two toggle/pill buttons** inline to the right of the label:
  - `Paste text` — active/selected state: white background, border, slightly elevated shadow
  - `Upload file` — inactive state: no background, plain text
  - Both are small rounded pill buttons (~32px height), border-radius ~20px
- **Sub-label:** `"Enter your request"` — small, gray, ~12px, above the textarea
- **Textarea:**
  - Large, white background, 1px light gray border (`#d0d5dd`), border-radius ~6px
  - Placeholder text: `"Click here to ask a different question"` — light gray italic
  - Height: ~130px
  - Full width of the card content

---

### 3c. Step 2 Section

- **Label:** `"Step 2"` — dark navy, bold, ~14px, left-aligned
- **Sub-label:** `"Additional Context (optional)"` — small, gray, ~12px
- **Textarea:**
  - Same styling as Step 1 textarea
  - Placeholder text: `"please enter value"` — light gray italic
  - Height: ~130px
  - Has a **resize handle** (small triangle) at bottom-right corner
  - Full width of the card content

---

### 3d. Continue Button

- **Position:** Bottom-right of the card, right-aligned
- **Style:**
  - Solid fill, **teal/blue color** (`#1a73b8` or similar)
  - White text, bold, ~14px
  - Rounded pill shape, border-radius ~25px
  - Padding: ~10px 28px
  - Label: `"Continue"`
  - Subtle hover shadow effect

---

## 4. BOTTOM INPUT BAR

- **Full-width**, fixed at bottom, light gray background (`#e8eaed`), ~70px tall
- **Inner container:** Rounded rectangle input box, white background, border-radius ~12px, padding ~12px 16px
- **Left label (inline):**
  - Text: `"Asking"` — gray, ~13px
  - Followed by: `"Deep Research"` — **teal/blue colored**, bold, ~13px
  - Then a `∨` dropdown chevron in teal, indicating it's clickable/selectable
- **Right side tip text:** `"Tip: Hit Shift + Enter Key for next line."` — small, light gray, ~11px
- **Input field:** Full width, no visible border inside the box, placeholder: `"Type a message"` — gray
- **Right-side icons (3 icons, right-aligned, vertically centered):**
  1. 📎 Paperclip/attachment icon
  2. 🎤 Microphone icon
  3. ➤ Send/arrow icon — blue teal colored (active send button)

---

## 5. SPACING & TYPOGRAPHY SYSTEM

| Element                  | Font Size | Weight       | Color       |
|--------------------------|-----------|--------------|-------------|
| Header brand text        | 16px      | Bold         | `#ffffff`   |
| Section labels (Step 1/2)| 14px      | Bold         | `#0d1f3c`   |
| Field sub-labels         | 12px      | Regular      | `#6b7280`   |
| Textarea placeholder     | 13px      | Regular Italic | `#9ca3af` |
| Button text              | 13px      | SemiBold     | White/Navy  |
| Sidebar labels           | 11px      | Regular      | `#6b7280`   |
| Timestamp                | 12px      | Regular      | `#9ca3af`   |

---

## 6. COLOR PALETTE

| Token              | Hex       | Usage                              |
|--------------------|-----------|------------------------------------|
| Navy Dark          | `#0d1f3c` | Header bg, step labels, card title |
| Teal/Blue Accent   | `#1a73b8` | Continue button, active link text  |
| Page Background    | `#f0f2f5` | Main content area bg               |
| Card Surface       | `#ffffff` | Content card, textarea bg          |
| Border Light       | `#d0d5dd` | Textarea and input borders         |
| Text Muted         | `#6b7280` | Sub-labels, sidebar labels         |
| Placeholder Gray   | `#9ca3af` | Textarea placeholder text          |
| Bottom Bar BG      | `#e8eaed` | Fixed bottom input bar             |

---

## 7. STREAMLIT IMPLEMENTATION NOTES

```python
# Key CSS overrides needed:
# 1. Hide default Streamlit header → replace with custom HTML header
# 2. Style sidebar to be narrow icon-only nav
# 3. Style st.text_area to match the clean bordered inputs
# 4. Style st.button for both the pill toggles and the Continue CTA
# 5. Create fixed bottom bar using position:fixed CSS on a container
# 6. Use st.columns([1, 6]) or similar for Step label + content layout
# 7. Card effect: wrap content in a div with box-shadow via st.markdown HTML

# Recommended approach:
# - Use st.markdown(unsafe_allow_html=True) for the header and bottom bar
# - Use custom CSS injected via st.markdown("<style>...</style>")
# - Use st.session_state to toggle between "Paste text" / "Upload file"
# - Use st.session_state to track active sidebar nav item

# Example header injection:
header_html = """
<div style="background-color:#0d1f3c; padding:12px 24px; display:flex;
            justify-content:space-between; align-items:center;">
    <span style="color:white; font-weight:bold; font-size:16px;">
        Morgan Stanley &nbsp;|&nbsp; ✦ Unified AI Investigator
    </span>
    <span style="color:white; border:1px solid white; border-radius:50%;
                 width:24px; height:24px; display:inline-flex;
                 align-items:center; justify-content:center; font-size:13px;">?</span>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# Example card wrapper:
card_html_open = """
<div style="background:#ffffff; border-radius:8px; padding:36px 40px;
            max-width:860px; margin:32px auto;
            box-shadow:0 1px 4px rgba(0,0,0,0.08);">
"""
card_html_close = "</div>"
```

---

## 8. COMPONENT HIERARCHY (Pseudocode)

```
App
├── CustomHeader (HTML inject)
│   ├── BrandTitle: "Morgan Stanley | ✦ Unified AI Investigator"
│   └── HelpIcon: "?"
├── Sidebar (st.sidebar)
│   ├── NavItem: "New Chat"    [+ icon]
│   ├── NavItem: "History"     [clock icon]
│   ├── NavItem: "Agents"      [grid icon]
│   └── NavItem: "Alerts"      [bell icon]
├── MainContentArea
│   └── ContentCard
│       ├── CardHeader
│       │   ├── SparkleIcon ✦
│       │   ├── Title: "Deep Research"
│       │   └── Timestamp: "01:51 PM"
│       ├── Step1Row
│       │   ├── Label: "Step 1"
│       │   ├── PillToggle: ["Paste text" | "Upload file"]
│       │   ├── SubLabel: "Enter your request"
│       │   └── Textarea (placeholder: "Click here to ask a different question")
│       ├── Step2Row
│       │   ├── Label: "Step 2"
│       │   ├── SubLabel: "Additional Context (optional)"
│       │   └── Textarea (placeholder: "please enter value")
│       └── ContinueButton (right-aligned, teal pill)
└── BottomInputBar (HTML inject, position:fixed)
    ├── LeftLabel: "Asking  [Deep Research ∨]"
    ├── TipText: "Tip: Hit Shift + Enter Key for next line."
    ├── TextInput (placeholder: "Type a message")
    └── ActionIcons: [📎 Attachment | 🎤 Mic | ➤ Send]
```
