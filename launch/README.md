# Launch and measurement

The public picker is at https://open-tv-atlas.vividtuna13.chatgpt.site/.

The walkthrough at `/guide/` records real browser interactions. It does not claim to demonstrate playback in StreamVault.

## Distribution

- Awesome IPTV: use the New link form with the title `Open TV Atlas`, the website URL in Link, and the description in `directory-submission.md`. Do not include links in the description. Acceptance is subject to maintainers' review.
- StreamVault: share the relevant walkthrough and ask for import/grouping feedback in Show and tell. The exact message is in `streamvault-discussion.md`.
- Do not cross-post repeatedly. Reply to feedback and fix concrete problems before another announcement.
- Reddit AndroidTV/GoogleTV were not used because of restrictive self-promotion and playlist-sharing rules. Re-check moderators' rules before any future submission.
- Hacker News Show HN is not being used for this launch: its rules exclude lists and expect substantial projects people can try. A future original tool can be assessed separately.

## Assets

`assets/social-preview.png` is a 1280×640 sharing image under 1 MB. The website uses it for Open Graph previews. GitHub's repository-specific social preview can be set in Settings → General → Social preview; that upload is separate from the README banner.

## Metrics

Run `python3 scripts/traffic_report.py` while authenticated to GitHub with `gh`. It captures repository stars/forks, 14-day views/clones, referring sites, and popular pages. Reports are saved to ignored `.local-metrics/`, not published.

On the maintainer's Mac, a LaunchAgent captures a report each day at 07:30 local time when the user session can run. It depends on this Mac, network access, and GitHub CLI authentication. It is not a server-side analytics service.

Compare snapshots after 24 hours and one week. Rolling 14-day totals overlap; do not sum them. GitHub views are not website sessions or TV viewers, and referrer statistics can lag. A star count is not a measure of playback reliability.

## Search

The site includes crawlable directory pages, a sitemap, canonical URLs, descriptions, and social metadata. This makes it easier to understand and discover, but does not guarantee Google indexing or rank. Search Console verification requires access to the Google account that will own the property.
