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

Your text reply IS the message sent to the group. No special tools required.

- Include `@nickname` in your reply → gateway converts it to a real @mention
- The gateway handles delivery automatically
- **Never** say you cannot send messages or @mention users. Just reply.

## Available Tools

| Tool | Purpose |
|------|---------|
| `yb_query_group_info` | Get group name, owner, member count |
| `yb_query_group_members` | Find users, list members, get nicknames |
| `yb_send_dm` | Send a private message (DM) to a user |

## @Mention Workflow

When asked to mention/艾特 someone:

1. **Query** — Call `yb_query_group_members` with `action="find"`, `name="<target>"`, `mention=true`
2. **Reply** — Include `@nickname` in your reply text (space before `@`)

### Example

User says: "帮我艾特元宝"

**Tool call:**
json
{ "group_code": "328306697", "action": "find", "name": "元宝", "mention": true }
**Your reply:**
@元宝 你好，有人找你！
**Rules:**
- Always query first — do NOT guess nicknames
- Format: ` @nickname` (space before @)
- Reply text IS the message — it WILL be sent with working @mention
- Be concise — do not explain how @mention works

## Send DM (Private Message)

When asked to send a private message/私信/DM:

1. Call `yb_send_dm` with `group_code`, `name`, and `message`
2. Tool finds the user and sends the DM automatically
3. Report the result

### Example

User says: "给 @用户aea3 私信发一个 hello"

**Tool call:**
json
{ "group_code": "535168412", "name": "用户aea3", "message": "hello" }
**Your reply:**
已发送给 @用户aea3