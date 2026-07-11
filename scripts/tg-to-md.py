#!/usr/bin/env python3
"""
Telegram JSON export (result.json) → per-day markdown files (Obsidian-flavored).

Usage:
    python tg-to-md.py result.json --slug turboplanner
    python tg-to-md.py result.json --slug turboplanner -o days/

Each message becomes a referenceable Obsidian block with id `^tg-{slug}-{id}`.
Reply references use wikilinks: [[YYYY-MM-DD#^tg-{slug}-{id}|Author]].

Idempotent: rerunning overwrites the same day files without touching others.
Service messages (join/leave/migrate/pin) are always dropped.

Handled:
    - text entities: plain, bold, italic, underline, strikethrough, code, pre,
                     link, text_link, mention, hashtag, phone, bot_command, email
    - photos (inline image), files (linked), polls (bullet list)
    - reply_to_message_id → wikilink block reference with author + preview
    - forwarded_from, edited timestamps
    - stickers, animations, voice/video messages (text description)
"""

import json
import os
import sys
import argparse
from collections import defaultdict


# ── helpers ──────────────────────────────────────────────────────────

def extract_plain(text):
    """Extract plain text from text field (str or list)."""
    if isinstance(text, str):
        return text
    if isinstance(text, list):
        parts = []
        for item in text:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                parts.append(item.get("text", ""))
        return "".join(parts)
    return str(text)


def render_text(text):
    """Render text field (str or list of str/dict) to markdown."""
    if isinstance(text, str):
        return text
    if not isinstance(text, list):
        return str(text)

    parts = []
    for item in text:
        if isinstance(item, str):
            parts.append(item)
            continue
        if not isinstance(item, dict):
            parts.append(str(item))
            continue

        t = item.get("text", "")
        etype = item.get("type", "plain")

        if etype == "plain":
            parts.append(t)
        elif etype == "bold":
            parts.append(f"**{t}**")
        elif etype == "italic":
            parts.append(f"*{t}*")
        elif etype == "underline":
            parts.append(f"<u>{t}</u>")
        elif etype == "strikethrough":
            parts.append(f"~~{t}~~")
        elif etype == "code":
            parts.append(f"`{t}`")
        elif etype == "pre":
            parts.append(f"```\n{t}\n```")
        elif etype == "link":
            parts.append(t)
        elif etype == "text_link":
            href = item.get("href", "#")
            parts.append(f"[{t}]({href})")
        else:
            # mention, hashtag, phone, bot_command, email → verbatim
            parts.append(t)

    return "".join(parts)


def render_poll(poll: dict) -> str:
    """Render poll structure as markdown."""
    lines = [f"📊 **Poll:** {poll.get('question', '')}"]
    if poll.get("closed"):
        lines[0] += " *(closed)*"
    for ans in poll.get("answers", []):
        voters = ans.get("voters", 0)
        chosen = " ✅" if ans.get("chosen") else ""
        lines.append(f"- {ans['text']} ({voters} votes{chosen})")
    return "\n".join(lines)


def block_id(slug: str, mid) -> str:
    """Obsidian block id for a message."""
    return f"tg-{slug}-{mid}"


# ── main conversion ──────────────────────────────────────────────────

def convert(input_path: str, output_dir: str, slug: str):
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    chat_name = data.get("name", "Telegram Chat")
    msgs = data.get("messages", [])
    base_dir = os.path.dirname(os.path.abspath(input_path))

    print(f"Chat: {chat_name}")
    print(f"Slug: {slug}")
    print(f"Messages: {len(msgs)}")
    print(f"Output: {output_dir}")

    os.makedirs(output_dir, exist_ok=True)

    # ── pass 1: reply map (id → date_key, author, preview) ──
    reply_map = {}
    for m in msgs:
        if m.get("type") != "message":
            continue
        mid = m.get("id")
        if not mid:
            continue
        d = m.get("date", "")
        author = m.get("from") or m.get("actor") or "(unknown)"
        preview = extract_plain(m.get("text", ""))
        reply_map[mid] = {
            "date_key": d[:10],
            "author": author,
            "preview": preview[:80].replace("\n", " ").strip(),
        }

    # ── pass 2: group real messages by date ──
    days = defaultdict(list)
    skipped_service = 0
    for m in msgs:
        if m.get("type") != "message":
            if m.get("type") == "service":
                skipped_service += 1
            continue
        date_key = m.get("date", "")[:10]
        if date_key:
            days[date_key].append(m)

    if skipped_service:
        print(f"Skipped {skipped_service} service messages (join/leave/migrate/pin).")

    if not days:
        print("No messages to process.")
        return

    # ── pass 3: render each day ──
    for date_key in sorted(days.keys()):
        day_msgs = sorted(days[date_key], key=lambda x: x.get("date", ""))
        out_path = os.path.join(output_dir, f"{date_key}.md")

        lines = []
        # frontmatter
        lines.append("---")
        lines.append(f'title: "{chat_name} — {date_key}"')
        lines.append(f"chat: {chat_name}")
        lines.append(f"date: {date_key}")
        lines.append("type: chat-log")
        lines.append(f"messages: {len(day_msgs)}")
        rel_json = os.path.relpath(input_path, os.path.dirname(os.path.abspath(output_dir)))
        lines.append(f"source: {rel_json}")
        lines.append("---")
        lines.append("")

        for m in day_msgs:
            mid = m.get("id")
            ts = m.get("date", "")
            time_str = ts[11:16] if len(ts) >= 16 else ts
            author = m.get("from") or m.get("actor") or "(unknown)"
            bid = block_id(slug, mid)

            # collect message body lines
            body = []

            # Header (heading + metadata form one block when no blank line)
            body.append(f"### {time_str} — {author}")
            if m.get("edited"):
                body.append(f"*(edited)*")

            # Reply-to reference (wikilink to source block)
            reply_to = m.get("reply_to_message_id")
            if reply_to and reply_to in reply_map:
                ref = reply_map[reply_to]
                target = f"{ref['date_key']}#^{block_id(slug, reply_to)}"
                body.append(f"> ↪️ [[{target}|{ref['author']}]]: {ref['preview']}")

            # Forwarded from
            fwd = m.get("forwarded_from")
            if fwd:
                body.append(f"*(forwarded from {fwd})*")

            # Text body
            text_body = render_text(m.get("text", ""))
            if text_body.strip():
                body.append("")
                body.append(text_body)

            # Photo
            photo = m.get("photo")
            if photo:
                photo_path = os.path.relpath(
                    os.path.join(base_dir, photo),
                    os.path.abspath(output_dir),
                )
                body.append("")
                body.append(f"![]({photo_path})")

            # File attachment
            file_path = m.get("file", "")
            file_name = m.get("file_name", "")
            if file_path and not file_path.startswith("(File not included") and not file_path.startswith("(File exceeds"):
                file_rel = os.path.relpath(
                    os.path.join(base_dir, file_path),
                    os.path.abspath(output_dir),
                )
                mime = m.get("mime_type", "")
                icon = "📄"
                if mime and mime.startswith("image/"):
                    icon = "🖼️"
                elif mime and mime.startswith("video/"):
                    icon = "🎬"
                elif mime and "djvu" in mime:
                    icon = "📖"
                elif mime and "pdf" in mime:
                    icon = "📕"
                body.append("")
                body.append(f"{icon} [{file_name}]({file_rel})")

            # Sticker / media info
            media_type = m.get("media_type")
            if media_type:
                emoji = m.get("sticker_emoji", "")
                if media_type == "sticker":
                    body.append(f"*(sticker {emoji})*" if emoji else "*(sticker)*")
                elif media_type in ("animation", "gif"):
                    body.append("*(animation)*")
                elif media_type == "video_message":
                    dur = m.get("duration_seconds", "?")
                    body.append(f"*(video message, {dur}s)*")
                elif media_type == "voice_message":
                    dur = m.get("duration_seconds", "?")
                    body.append(f"*(voice message, {dur}s)*")
                elif media_type == "video_file":
                    body.append("*(video)*")
                else:
                    body.append(f"*({media_type})*")

            # Poll
            poll = m.get("poll")
            if poll:
                body.append("")
                body.append(render_poll(poll))

            # Block id: strip trailing blanks, append id on its own line
            # so it attaches to the last content block (no blank line before it).
            while body and body[-1].strip() == "":
                body.pop()
            body.append(f"^{bid}")

            lines.extend(body)
            lines.append("")
            lines.append("---")
            lines.append("")

        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"  ✓ {date_key} ({len(day_msgs)} msgs) → {out_path}")

    print(f"\nDone. {len(days)} day files in {output_dir}/")


# ── CLI ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Telegram JSON export → per-day Obsidian markdown files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s result.json --slug turboplanner\n"
            "  %(prog)s path/to/result.json --slug turboplanner -o days/\n"
        ),
    )
    parser.add_argument("input", help="Path to Telegram result.json")
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Output directory (default: 'days/' next to input file)",
    )
    parser.add_argument(
        "--slug",
        required=True,
        help="Chat slug used in block ids (e.g. 'turboplanner' → ^tg-turboplanner-1543)",
    )
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"Error: file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    output_dir = args.output
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(os.path.abspath(args.input)), "days")

    convert(args.input, output_dir, args.slug)


if __name__ == "__main__":
    main()
