# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Static HTML/CSS (plus minimal vanilla JS for progressive enhancement), multi-page, no build step, deployed from the repository with GitHub Pages. Confirmed by the user for this concept repo.

The eventual production site is a WordPress block (FSE) theme with an IDX plugin, hosted on Cloudways. Anything this concept defines (tokens, components, data shapes) must translate cleanly into `theme.json`, block patterns and a provider-agnostic IDX adapter.

## Users

- **Buyers** searching for a home anywhere in Massachusetts, often on a phone, comparing listings, towns and terms.
- **Sellers** deciding whom to trust with pricing, preparation and the legal side of a sale.
- **Investors** evaluating rental, multi-family and value-add property who need numbers, zoning context and straight answers.

The three audiences carry equal priority. A secondary audience is agents and teams considering affiliation with the brokerage, and affiliated teams (The Oberdorfer Group) who must be represented without being absorbed.

## Product Purpose

The website is REWAP Brokerage LLC's primary public presence: it establishes the firm as a serious, trustworthy advisory brokerage, routes buyers, sellers and investors to the right next step, and (in production) carries MLS/IDX listing search. Success is a visitor concluding "this is a serious brokerage," not "this is a nice real-estate template," and then making contact or saving a search.

This repository is **Concept 1** — an independent creative direction to be compared side by side with Concept 2 ("The Massachusetts Atlas", https://cptnope.github.io/REWAP-Brokerage-Concept-2/). It must not reuse Concept 2's concept, typefaces or palette.

## Positioning

A brokerage founded and led by a real estate lawyer. Hong Tran is both founder and practicing real estate attorney, so the firm can credibly offer legal-level precision on contracts, title and closing alongside brokerage service. Neighboring brokerages can claim local knowledge and responsiveness; they cannot truthfully claim an attorney-founder at the center of the transaction.

## Operating Context

- Headquarters: 652 Park Ave, Worcester, MA 01603. Phone 508-509-7759. Email hongtran@lehonglaw.com.
- Coverage: all of Massachusetts, with every region presented with equal weight (user decision, 2026-10-06). Worcester is the home office, not the boundary.
- Affiliation hierarchy the product must support: Brokerage → brokers → agents → teams/groups → listings → communities. Confirmed affiliated team: The Oberdorfer Group (Brandon Oberdorfer, broker; Kait Oberdorfer), which keeps its own identity under REWAP.
- Listings will come from a legitimate MLS/IDX feed through a vendor that may change; no vendor is chosen.
- Massachusetts compliance surfaces: brokerage/agency disclosures, Fair Housing, MLS attribution and data-currency notices, privacy policy, WCAG 2.2 AA.

## Capabilities and Constraints

- Phase 1 (this round): brand book and logo system only. Website page concepts follow in a later round.
- The existing REWAP logo is binding (see Brand Commitments).
- Future platform intent is internal only: brand, content, brokerage, agent, team, property, IDX adapter, lead routing, CRM adapter, analytics and compliance layers stay separable so the system can later serve other brokerages. Visitors never see this.
- Undecided: IDX vendor, CRM, final domain structure for team microsites, photography budget/commissioning.

## Brand Commitments

- **Name:** REWAP Brokerage LLC. The meaning of "REWAP" is not publicly documented; do not invent an origin story or expand it as an acronym as fact.
- **Logo:** the existing mark (bronze ring and key-shaped frame, "REWAP" with a navy "W" and a small house glyph in the "A", a skyline running along the key shaft, "BROKERAGE" set inside the shaft ending in a key-tip chevron). It is an input, not a suggestion: it may be vectorised, cleaned and given reduced-complexity variants for small or one-color use, but not replaced or redrawn into a different identity. Exploratory marks must be labelled as such.
- **Required qualities:** quiet authority, legal-level precision, local knowledge, calm confidence, intelligent guidance, long-term trust. Feels like an established advisory firm that is exceptional at real estate.
- **Concept 1 direction (user decision, 2026-10-06):** the category standard for a top-tier brokerage, executed at full craft rather than reinvented. Peer bar: Christie's International Real Estate (gallery-like composition, auction-house authority). Match that level of finish; never copy its marks, typefaces or layouts. The brief's bans still apply (no black + metallic gold + serif cliché, no glassmorphism, no fake metrics).
- **Public positioning to preserve:** buyers, sellers, investors; local market knowledge; honest guidance; responsive service; clarity and confidence; long-term client value.

## Evidence on Hand

- Logo raster (512 × 171 px, RGBA): `assets/logo/source/rewap-logo-original.png`.
- Founder name and title, office address, phone and email (above).
- No testimonials, reviews, transaction counts, sales volume, awards, years-in-business or market statistics have been supplied. Do not fabricate any; show labelled placeholders where a live data source will supply them.
- No photography supplied; art direction must specify what to commission and mark any placeholder imagery as such.

## Product Principles

1. **Counsel before commerce.** Every surface should read as advice from a firm that understands the transaction, not as a pitch.
2. **Precision is the luxury.** Exact language, exact data, sourced numbers; no inflated claims.
3. **Every region, equal standing.** No part of Massachusetts is presented as an afterthought.
4. **Affiliates keep their names.** REWAP frames its teams; it never swallows them.
5. **Built to outlast the vendor.** Listing data, CRM and IDX are swappable layers behind a stable brand.

## Accessibility & Inclusion

WCAG 2.2 AA across all surfaces, including property search, filters, maps, dialogs and forms. Respect `prefers-reduced-motion`. Fair Housing–compliant language: describe places and properties, never the people who live there.
