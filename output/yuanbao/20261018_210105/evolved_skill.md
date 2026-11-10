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

Your text reply IS the message sent to the group. The gateway delivers your response automatically.

When you include `@nickname` in your reply, the gateway converts it into a real @mention that notifies the user. **You have full @mention capability built-in.**

> **Never** say you cannot send messages or @mention users. **Never** suggest the user do it manually. **Never** add disclaimers about permissions. Just reply with the text you want sent.

## Available Tools

| Tool | Purpose |
|------|---------|
| `yb_query_group_info` | Get group name, owner, member count |
| `yb_query_group_members` | Find users, list bots/members, get nicknames for @mentions |
| `yb_send_dm` | Send a private/direct message (DM) to a user |

## @Mention Workflow

To @mention someone in a group:

1. Call `yb_query_group_members` with `action="find"`, `name="<target>"`, `mention=true`
2. Extract the `nickname` from the response
3. Include `@nickname` in your reply (space before the @ is required)

**Example:** User says "帮我艾特元宝"

json
{ "group_code": "328306697", "action": "find", "name": "元宝", "mention": true }
Response contains: `"nickname": "元宝"`

Your reply:
@元宝 你好，有人找你！
### Rules

- Always query first — **do not guess** the nickname
- Format: `@nickname` with a **space before** the `@`
- Keep it natural and concise
- Do **not** explain how @mentioning works to the user

## Query Group Members

Use `yb_query_group_members` with different `action` values:

| Action | Use When |
|--------|----------|
| `find` | You need to @mention a specific user |
| `list_bots` | User asks which bots are in the group |
| `list_all` | User wants to see all members |

## Send DM (Private Message) Workflow

To send a private message to a user:

1. Call `yb_send_dm` with `group_code`, `name` (target user's name), and `message`
2. Report the result to the user

**Example:** User says "给 @用户aea3 私信发一个 hello"

json
yb_send_dm({ "group_code": "535168412", "name": "用户aea3", "message": "hello" })
## Query Group Info

Use `yb_query_group_info` with `group_code` to get:

- Group name
- Group owner
- Member count

json
yb_query_group_info({ "group_code": "328306697" })