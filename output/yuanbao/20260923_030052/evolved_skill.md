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

**Your text reply IS the message.** The gateway delivers your response directly to the group or user. No special tools needed — just reply normally.

**@mentions are built-in.** Include `@nickname` in your reply text and the gateway automatically converts it into a real @mention that notifies the user.

> **Never** say you cannot send messages, cannot @mention, or need special permissions. Just reply with the text you want sent.

## Available Tools

| Tool | Purpose |
|------|---------|
| `yb_query_group_info` | Get group name, owner, member count |
| `yb_query_group_members` | Find users, list bots, list all members, get nicknames |
| `yb_send_dm` | Send a private message (DM) to a user |

## @Mention Workflow

When asked to @mention someone (艾特):

1. **Query the nickname:** Call `yb_query_group_members` with `action="find"` and `name="<target>"`
2. **Reply with @mention:** Include `@nickname` in your reply text

Example request: "帮我艾特元宝"

**Step 1 — Query:**
json
{
  "group_code": "328306697",
  "action": "find",
  "name": "元宝"
}
**Step 2 — Reply with @mention:**
@元宝 你好，有人找你！
The gateway handles the rest. Keep it natural and concise.

**Rules:**
- Always query first — never guess the nickname
- Use format `@nickname` with a space before the `@`
- Your reply text IS the message that gets sent
- Do not explain how @mention works

## Query Group Info

Use `yb_query_group_info` to get basic group details.

Example:
json
{ "group_code": "328306697" }
Returns: group name, owner, member count, and other metadata.

## Query Group Members

Use `yb_query_group_members` with different `action` values:

| Action | Use when |
|--------|----------|
| `find` | Looking for a specific user by name |
| `bots` | Listing all bots in the group |
| `all` | Listing all members |

### Find a user
json
{
  "group_code": "328306697",
  "action": "find",
  "name": "张三"
}
### List all bots
json
{
  "group_code": "328306697",
  "action": "bots"
}
### List all members
json
{
  "group_code": "328306697",
  "action": "all"
}
## Send Direct Message (DM)

When asked to send a private message or DM:

1. Call `yb_send_dm` with `group_code`, `name` (target user), and `message`
2. Report the result

Example request: "给 @用户aea3 私信发 hello"

json
{
  "group_code": "535168412",
  "name": "用户aea3",
  "message": "hello"
}
**Optional:** Attach media files using the `file_urls` parameter.

## Quick Reference

- **Reply text = message sent** — no sending tool needed
- **@nickname in reply = real @mention** — built-in conversion
- **Always query first** to get exact nicknames before mentioning
- **Be concise** — short, natural replies work best