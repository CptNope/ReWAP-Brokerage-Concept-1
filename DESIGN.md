---
name: REWAP Brokerage — Concept 1
description: The category standard for a top-tier brokerage, at gallery-and-catalogue craft. Real estate, with clarity.
colors:
  night: "#0C1827"
  navy: "#17283F"
  navy-700: "#273A54"
  navy-500: "#4D5F77"
  navy-200: "#C9D2DD"
  navy-100: "#E5EAF0"
  bronze-700: "#7C532E"
  bronze: "#AD7E50"
  bronze-300: "#D8B38A"
  bronze-100: "#F4E8D8"
  gallery: "#FAFAF9"
  plaster: "#F4F2EF"
  limestone: "#E5E3DE"
  hairline: "#D9D7D3"
  granite: "#7C8187"
  slate: "#545C66"
  ink: "#192331"
  success: "#2C6C47"
  warning: "#875814"
  warning-fill: "#F0D49B"
  error: "#B1322D"
typography:
  display:
    fontFamily: "Libre Caslon Display, Georgia, serif"
    fontSize: "clamp(3rem, 1.9rem + 4.2vw, 6rem)"
    fontWeight: 400
    lineHeight: 1.02
    letterSpacing: "-0.012em"
  h1:
    fontFamily: "Libre Caslon Display, Georgia, serif"
    fontSize: "clamp(2.5rem, 1.75rem + 2.8vw, 4.25rem)"
    fontWeight: 400
    lineHeight: 1.12
    letterSpacing: "-0.012em"
  h2:
    fontFamily: "Libre Caslon Display, Georgia, serif"
    fontSize: "clamp(1.875rem, 1.45rem + 1.5vw, 2.75rem)"
    fontWeight: 400
    lineHeight: 1.12
    letterSpacing: "-0.006em"
  h3:
    fontFamily: "Libre Caslon Text, Georgia, serif"
    fontSize: "clamp(1.375rem, 1.22rem + .55vw, 1.75rem)"
    fontWeight: 600
    lineHeight: 1.25
  lead:
    fontFamily: "Libre Caslon Text, Georgia, serif"
    fontSize: "clamp(1.1875rem, 1.08rem + .4vw, 1.4375rem)"
    fontWeight: 400
    lineHeight: 1.5
  body:
    fontFamily: "Libre Caslon Text, Georgia, serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.6
  ui:
    fontFamily: "Public Sans, system-ui, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.45
  label:
    fontFamily: "Public Sans, system-ui, sans-serif"
    fontSize: "0.75rem"
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: "0.14em"
  caption-title:
    fontFamily: "Libre Caslon Text, Georgia, serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.35
  price:
    fontFamily: "Libre Caslon Display, Georgia, serif"
    fontSize: "1.75rem"
    fontWeight: 400
    lineHeight: 1.1
rounded:
  none: "0"
spacing:
  s-1: "4px"
  s-2: "8px"
  s-3: "12px"
  s-4: "16px"
  s-5: "24px"
  s-6: "32px"
  s-7: "48px"
  s-8: "64px"
  s-9: "96px"
  s-10: "128px"
  section: "clamp(64px, 48px + 5vw, 144px)"
components:
  button-primary:
    backgroundColor: "{colors.navy}"
    textColor: "{colors.gallery}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0 24px"
    height: "48px"
  button-primary-hover:
    backgroundColor: "{colors.navy-700}"
  button-primary-active:
    backgroundColor: "{colors.night}"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.night}"
    rounded: "{rounded.none}"
    height: "48px"
  button-on-navy:
    backgroundColor: "{colors.gallery}"
    textColor: "{colors.night}"
    rounded: "{rounded.none}"
    height: "48px"
  input:
    backgroundColor: "#FFFFFF"
    textColor: "{colors.ink}"
    typography: "{typography.ui}"
    rounded: "{rounded.none}"
    padding: "12px 16px"
    height: "48px"
  chip:
    backgroundColor: "#FFFFFF"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "0 12px 0 16px"
    height: "36px"
  chip-selected:
    backgroundColor: "{colors.navy-100}"
  property-status:
    backgroundColor: "{colors.gallery}"
    textColor: "{colors.night}"
    rounded: "{rounded.none}"
    padding: "6px 12px"
---

# Design System: REWAP Brokerage — Concept 1

## Overview

**Creative North Star: "The Gallery and the Catalogue"**

REWAP is presented the way a great auction house presents a collection: generous white walls, few works per room, and an exact caption beside each one. The peer bar is Christie's International Real Estate's level of finish; the material is REWAP's own. Authority comes from composition, precise language and sourced facts rather than ornament. The binding logo (bronze ring and key, navy W with a house) supplies the only two brand colors, and the system holds them with restraint: Registry Navy does the work black usually does, bronze is a signature reserved for the mark and hairlines.

Pages alternate rooms: Gallery (white), Plaster (alternate), one Registry Navy statement room per page, and full-width Ledger data. Photography is commissioned and observational; until it exists, an authored fine-line elevation drawing set stands in honestly.

**Key Characteristics:**
- Near-neutral gallery white ground, never cream; navy-tinted ink, never pure black.
- Caslon for the voice (display, headings, prose), Public Sans for facts (labels, data, interface) with tabular figures.
- Every image and listing carries a museum wall-label caption: italic title, then facts.
- Square corners, 1 px rules, a single soft lift reserved for menus.
- An index margin of three columns for section codes and labels; reading starts at column four.

## Colors

The palette is defined in OKLCH (source: tools/palette.py) with sRGB hex as the fallback recorded above.

### Primary
- **Registry Navy** (navy): the field color of statement rooms, primary buttons and links. Drawn from the logo's W.
- **Night** (night): darkest navy for headings, footer and pressed states. **Navy 700** for hover, **Harbor** for informational UI, **Fog** and **Mist** for tints and selected states.

### Secondary
- **Bronze** (bronze): the mark's flat color. Rules, underlines, chapter numerals at display size and the mark only.
- **Bronze Deep** (bronze-700): the only bronze allowed as small text on light grounds (6.4:1); also the focus outline.
- **Bronze Light** (bronze-300): accents and text on navy (7.6:1). **Bronze Tint** for quiet grounds.

### Neutral
- **Gallery** page ground, **Plaster** alternate surface, **Limestone** and **Hairline** rules, **Granite** control borders (3.76:1, meets non-text contrast), **Slate** secondary text, **Ink** body text.

### Named Rules
**The Five Percent Rule.** Bronze covers under five percent of any view. When a layout seems to need more bronze, it needs a photograph instead.

**The No Gold Rule.** Bronze is never pushed toward yellow gold, never metallic outside the logo itself, and never fills a button.

**The Status-Only Rule.** Success, Warning and Error appear only for status, never as decoration.

## Typography

**Display Font:** Libre Caslon Display (Georgia fallback)
**Body Font:** Libre Caslon Text (Georgia fallback)
**Label/Mono Font:** Public Sans (system-ui fallback)

**Character:** Caslon is the face of the American founding documents and of law books; Public Sans was drawn for United States government web standards. Together: permanence, law and civic clarity. All three files are self-hosted, Latin-subset WOFF2, with the historical long-s "st" ligature removed from the Caslon fonts.

### Hierarchy
- **Display** (400, 48→96 px, 1.02): cover titles and single statements.
- **Headline h1–h2** (400, 40→68 / 30→44 px): chapter and section titles, sentence case.
- **Title h3** (Caslon Text 600, 22→28 px).
- **Lead** (19→23 px, 1.5) max 38 characters per line; **Body** (17 px, 1.6) max 66ch.
- **UI** (Public Sans 16 px), **Small** (14 px), **Label** (12 px, 600, +0.14em, all caps, four words maximum).
- **Price** in Caslon Display; every other number in Public Sans with tabular lining figures.

### Named Rules
**The Two Voices Rule.** Caslon speaks; Public Sans states facts. A price is the one number set in Caslon.

**The Four Word Label Rule.** Caps-tracked labels never exceed four words, and never sit above a heading as an eyebrow.

## Layout

Twelve columns inside a 1440 px page (`--page-max: 90rem`), fluid gutters 20→64 px, column gap 16→32 px. Columns 1–3 form the index margin (section codes, terms, captions); content starts at column 4, body measure 66ch. Sections are separated by fluid 64→144 px padding with more space above a heading than below it. Compositions: Index (3/7), Plate (8/4), Statement (full navy, once per page), Catalogue (3–4 across), Ledger (full-width data), Split search (list and map, full bleed). Below 768 px the index margin collapses above content, tables scroll inside their frame and touch targets stay at 44 px.

## Elevation & Depth

The system is flat. Depth comes from ground changes (Gallery, Plaster, Navy) and 1 px rules, not shadows.

### Shadow Vocabulary
- **lift** (`0 1px 2px rgb(12 24 39 / .06), 0 10px 20px -12px rgb(12 24 39 / .2)`): menus and popovers only.

### Named Rules
**The One Lift Rule.** Only floating UI (menus, popovers, sheets) casts a shadow. Cards and plates never do.

## Shapes

Square corners everywhere (`rounded.none`). Circles appear only in the logo's rings, radio controls and map pins. Rules are 1 px; the current item and error states change weight or full border, never a thick side stripe.

## Components

### Buttons
Square, 48 px tall, Public Sans 600 caps at 0.08em. Primary: Registry Navy fill, hover Navy 700, pressed Night. Secondary: Night outline, fills Night on hover. Quiet: text with a 1 px Bronze underline. On navy: Gallery fill, hover Bronze Light. One primary per view.

### Chips
Square 36 px filter chips on white with a Limestone border; selected chips take a Mist fill and Harbor border; removable chips carry an × icon.

### Cards / Containers
Property cards are catalogue entries: 4:3 image (elevation drawing with "Photo pending" when media is missing), one MLS status label, a 1 px Night rule, price in Caslon Display, italic address, Public Sans facts separated by hairlines, and listing-office attribution. The whole card links through the address; Save is a separate labelled toggle. No nested cards.

### Inputs / Fields
White field, Granite 1 px border, 48 px tall, label above, hint before error; focus adds a Night ring plus a soft bronze halo; errors use a full Error border and a message naming the fix.

### Navigation
Logo top left (200–240 px; derived wordmark at 120 px on phones), six links in Public Sans 500 — Buy, Sell, Invest, Communities, Market, The Firm — current page marked by a 1 px bronze rule, one filled action: Search homes.

### Wall-label caption
The signature component: a 1 px rule, an italic Caslon title, then a Public Sans meta line of facts, credit and date. Used under every image, plate, logo figure and listing.

## Do's and Don'ts

### Do:
- **Do** use the logo exactly as supplied, from the vector masters, with one roof height of clear space.
- **Do** caption every image like a wall label.
- **Do** set numbers in tabular Public Sans and cite the source and date of every market figure.
- **Do** present every Massachusetts region with equal standing.
- **Do** label sample data and placeholders as such.

### Don't:
- **Don't** use black with metallic gold, gradient text, glassmorphism or rounded oversized cards.
- **Don't** place eyebrows or kickers above headings.
- **Don't** use stock imagery of keys, handshakes, families on sofas or aerial subdivisions, or AI-generated homes or people.
- **Don't** invent metrics, testimonials or awards.
- **Don't** recolor an affiliated team's mark in REWAP colors or merge team and brokerage names.
