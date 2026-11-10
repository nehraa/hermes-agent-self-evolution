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

## Critical: How Messaging Works

**Your text reply IS the message sent to the group/user.**

The gateway automatically delivers your response text to the chat. There is no "send message" tool — simply reply normally and it will be sent.

**@Mentions are built-in.** Include `@nickname` in your reply text, and the gateway converts it into a real @mention that notifies the user. You have full @mention capability.

**Never:**
- Say you cannot send messages or @mention users
- Suggest the user do it manually
- Add disclaimers about permissions

Just reply with the text you want sent.

## Available Tools

### `yb_query_group_info`

Use when you need to find: group name, owner, member count.

### `yb_query_group_members`

Use when you need to:
- Find a specific user by name
- List all bots in the group
- List all members
- Get a user's exact nickname for @mention

### `yb_send_dm`

Use to send a private/direct message (DM/私信) to a user, with optional media files.

## @Mention Workflow

When asked to @mention (艾特) someone:

1. **Query the user** — Call `yb_query_group_members` with `action="find"`, `name="<target>"`, `mention=true`
2. **Extract the nickname** — Get the exact `nickname` from the response
3. **Reply with the mention** — Include `@nickname` in your reply text

### Example

User says: "帮我艾特元宝"

**Step 1 — Query the user:**
json
{
  "group_code": "328306697",
  "action": "find",
  "name": "元宝",
  "mention": true
}
**Step 2 — Reply with the @mention:**
@元宝 你好，有人找你！
The gateway handles the rest. Keep it short and natural.

### Rules

- **Always query first** — Never guess the nickname
- **Format:** `@nickname` with a space before the `@` sign
- **Your reply is the message** — it WILL be sent and the @mention WILL work
- **Be concise** — do NOT explain how @mentions work to the user

## Send DM (Private Message) Workflow

When asked to send a private message (私信/DM) to a user:

1. Call `yb_send_dm` with `group_code`, `name` (target user's name), and `message`
2. The tool automatically finds the user and sends the DM
3. Report the result

### Example

User says: "给 @用户aea3 私信发一个 hello"

json
{
  "group_code": "535168412",
  "name": "用户aea3",
  "message": "hello"
}
## Query Group Info

### Example

User says: "这个群有多少人？"

json
{
  "group_code": "328306697",
  "action": "get_group_info"
}
Response includes: group name, owner, member count.

## List Group Members

### Example

User says: "列出所有群成员"

json
{
  "group_code": "328306697",
  "action": "list_all"
}
## Quick Reference

| Task | Tool | Required Params |
|------|------|-----------------|
| @mention someone | `yb_query_group_members` | `group_code`, `action="find"`, `name`, `mention=true` |
| List all members | `yb_query_group_members` | `group_code`, `action="list_all"` |
| List bots | `yb_query_group_members` | `group_code`, `action="list_bots"` |
| Group info | `yb_query_group_info` | `group_code` |
| Send DM | `yb_send_dm` | `group_code`, `name`, `message` |