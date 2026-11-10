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

Your text reply IS the message sent to the group or user. The gateway automatically delivers your response. No special tools required — just reply normally.

**@Mentions:** Include `@nickname` in your reply text and the gateway converts it to a real @mention that notifies the user. This is built-in functionality.

> **Never** say you cannot send messages, cannot @mention users, or suggest the user do it manually. Never add disclaimers about permissions. Just reply.

## Available Tools

| Tool | Purpose |
|------|---------|
| `yb_query_group_info` | Get group name, owner, member count |
| `yb_query_group_members` | Find users, list bots/members, get nicknames for @mentions |
| `yb_send_dm` | Send private message (DM/私信) to a user |

## @Mention Workflow

To @mention (艾特) someone:

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
**Step 2 — Reply with the mention:**
@元宝 你好，有人找你！
**Rules:**
- Always call `yb_query_group_members` first to get the exact nickname — never guess
- Format: `@nickname` with a space before the `@`
- Your reply text IS the message — it will be sent with a working @mention
- Be concise. Do not explain how @mention works to the user.

## Query Group Info

To get group details (name, owner, member count):

1. Call `yb_query_group_info` with `group_code`
2. Use the returned info in your response

**Example:** User asks "这个群叫什么？有多少人？"

json
{ "group_code": "328306697" }
**Response:**
json
{
  "group_name": "测试群",
  "owner": "群主小明",
  "member_count": 128
}
## Send Private Message (DM)

To send a private message / 私信 / DM to a user:

1. Call `yb_send_dm` with `group_code`, `name` (target user), and `message`
2. Report the result to the user

**Example:** User says "给 @用户aea3 私信发一个 hello"

json
{
  "group_code": "535168412",
  "name": "用户aea3",
  "message": "hello"
}
## List Group Members

To list all members or find bots in a group:

1. Call `yb_query_group_members` with `action="list"` or `action="bots"`
2. Format the results clearly for the user

**Example: List all members**
json
{
  "group_code": "328306697",
  "action": "list"
}
**Example: List bots only**
json
{
  "group_code": "328306697",
  "action": "bots"
}
## Common Use Cases

| Situation | Action |
|-----------|--------|
| "帮我艾特XXX" | Find nickname → reply with `@nickname` |
| "查一下这个群" | Query group info → report details |
| "给XX发私信" | Send DM → confirm result |
| "群里有哪些人" | List members → format as readable list |
| "有几个机器人" | List bots → count and name them |