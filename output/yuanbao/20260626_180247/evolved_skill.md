---
name: yuanbao
description: "Yuanbao (元宝) groups: @mention users, query info/members."
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [yuanbao, mention, at, group, members, 元宝, 派, 艾特]
    related_skills: []
---

# Yuanbao Group Interaction

## How Messaging Works

**Your text reply IS the message sent to the group or user.** The gateway automatically delivers your response. No special sending tool is needed — just reply normally.

**@Mentions work automatically.** When you include `@nickname` in your reply, the gateway converts it into a real @mention that notifies the user.

> **NEVER** say you cannot send messages or @mention users. **NEVER** suggest the user do it manually or add disclaimers about permissions. Just reply with the text you want sent.

## Available Tools

### `yb_query_group_info`
Query group information including name, owner, and member count.

**Parameters:**
- `group_code` (required): The group ID

### `yb_query_group_members`
Find users, list members, list bots, or get nicknames for @mentions.

**Parameters:**
- `group_code` (required): The group ID
- `action` (required): `find`, `list`, `list_bots`, or `list_all`
- `name` (optional): User name to search (for `find` action)
- `mention` (optional): Set to `true` when you need the nickname for an @mention

### `yb_send_dm`
Send a private/direct message to a user.

**Parameters:**
- `group_code` (required): The group ID
- `name` (required): Target user's name
- `message` (required): The message to send
- `media_url` (optional): URL of media to attach

---

## @Mention Workflow

When you need to @mention someone:

1. Call `yb_query_group_members` with `action="find"`, `name="<target>"`, `mention=true`
2. Extract the exact `nickname` from the response
3. Reply with `@nickname` in your text — the gateway handles conversion

**Example:** User says "帮我艾特元宝"

**Step 1 — Call the tool:**
json
{
  "group_code": "328306697",
  "action": "find",
  "name": "元宝",
  "mention": true
}
**Step 2 — Reply with the @mention:**
@元宝 你好，有人找你！
**Rules:**
- Always call `yb_query_group_members` first to get the exact nickname — do NOT guess
- Use format: `@nickname` with a space before the `@` symbol
- Your reply text IS the message — it will be sent with a working @mention
- Be concise. Do NOT explain how @mentions work to the user.

---

## Send DM (Private Message) Workflow

When someone asks you to send a private message / 私信 / DM to a user:

1. Call `yb_send_dm` with `group_code`, `name`, and `message`
2. The tool finds the user and sends the DM automatically
3. Report the result to the user

**Example:** User says "给 @用户aea3 私信发一个 hello"

json
{
  "group_code": "535168412",
  "name": "用户aea3",
  "message": "hello"
}
**If media is needed, add `media_url`:**
json
{
  "group_code": "535168412",
  "name": "用户aea3",
  "message": "这是你要的图片",
  "media_url": "https://example.com/image.jpg"
}
---

## Quick Reference

| Task | Tool | Action |
|------|------|--------|
| Get group info (name, owner, member count) | `yb_query_group_info` | — |
| Find user by name | `yb_query_group_members` | `find` |
| List all members | `yb_query_group_members` | `list_all` |
| List bots only | `yb_query_group_members` | `list_bots` |
| Send private message | `yb_send_dm` | — |