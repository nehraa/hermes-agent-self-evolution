#!/usr/bin/env python3
"""
Heuristic Dataset Generator — ZERO LLM calls.
Extracts task patterns from skill text and generates eval examples via keyword matching.
Produces 10 examples per skill: 7 train / 2 val / 1 holdout.
"""
import json
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from evolution.core.dataset_builder import EvalExample, EvalDataset

HERMES_SKILLS = Path.home() / '.hermes' / 'skills'

# Task templates per category (zero LLM)
TASK_TEMPLATES = {
    'coding': [
        ("Review this PR for bugs and security issues", "Provides specific, actionable findings with file:line references"),
        ("Implement the feature described in the SKILL.md", "Follows the exact procedure in the skill — numbered steps, code blocks, path references"),
        ("Debug why the tests are failing", "Identifies root cause, shows traceback analysis, proposes fix"),
        ("Refactor this code to be cleaner", "Follows the refactoring patterns in the skill"),
        ("Write tests for this module", "Tests cover happy path + edge cases, use the skill's testing conventions"),
    ],
    'research': [
        ("Find recent papers about {topic}", "Returns title, authors, year, arXiv ID, and 2-line summary"),
        ("Research {topic} and give me a briefing", "Structure: Overview → Key Findings → Gaps → Next Steps"),
        ("Compare {a} vs {b} for our use case", "Gives structured comparison table, states recommendation with rationale"),
        ("Find the best open-source implementation of {topic}", "Links to repos, stars, last commit, pros/cons"),
        ("What is the current state of {topic}?", "Gives concise technical overview with recent developments"),
    ],
    'ops': [
        ("Set up {service} on the server", "Follows the setup procedure in the skill — exact commands, correct paths"),
        ("Debug why {service} is down", "Diagnostic steps, log analysis, shows what was checked"),
        ("Monitor {service} and alert me if {condition}", "Checks at correct interval, alert contains actionable info"),
        ("Deploy {app} with zero downtime", "Follows deployment procedure — backup, migrate, verify, rollback"),
        ("Configure {service} for production", "Uses production-grade settings from the skill"),
    ],
    'messaging': [
        ("Send a personalized outreach message to {person}", "Message is specific to recipient, has clear CTA, matches the skill's tone"),
        ("Draft a follow-up to {situation}", "Follows the outreach template structure — hook, value prop, close"),
        ("Create a bulk message for {list}", "Personalized placeholders, correct format, no spam signals"),
        ("Reply to this customer complaint", "Empathetic, solution-oriented, specific resolution, right tone"),
        ("Send a meeting summary to {recipient}", "Key decisions, action items with owners, next steps"),
    ],
    'data': [
        ("Analyze this dataset and find patterns", "Structure: Overview → Patterns → Anomalies → Recommendations"),
        ("Build a visualization for {metric}", "Chart type matches data shape, clear labels, no chartjunk"),
        ("Clean this messy data and explain decisions", "Shows what was cleaned, why, preserves useful variance"),
        ("Generate a report from {source}", "Follows report structure, all sections populated, actionable"),
        ("Find outliers in {dataset}", "Lists outliers with context, distinguishes from noise"),
    ],
    'file': [
        ("Organize the files at {path} according to {rule}", "Correct categorization, consistent naming, preserves accessibility"),
        ("Find all files matching {pattern}", "Returns correct paths, correct file types, no false positives"),
        ("Convert {file} from {a} to {b} format", "Content preserved, formatting equivalent, no data loss"),
        ("Compress {file} to under {size}", "Output under size limit, content intact, appropriate algorithm"),
        ("Backup {path} to {destination}", "Incremental, verified, documented, restorable"),
    ],
}

TASK_KEYWORDS = {
    'coding': ['git', 'code', 'debug', 'pr', 'branch', 'commit', 'test', 'build', 'deploy', 'function', 'class', 'module', 'api', 'refactor', 'lint', 'type'],
    'research': ['paper', 'arxiv', 'research', 'find', 'compare', 'analyze', 'survey', 'review', 'study', 'academic'],
    'ops': ['server', 'deploy', 'docker', 'kubernetes', 'monitor', 'alert', 'config', 'setup', 'install', 'cron', 'nginx', 'ssl'],
    'messaging': ['message', 'send', 'email', 'outreach', 'whatsapp', 'telegram', 'dm', 'draft', 'template', 'bulk', 'personalize'],
    'data': ['data', 'csv', 'json', 'visualization', 'chart', 'plot', 'analyze', 'clean', 'dataset', 'pandas', 'sql'],
    'file': ['file', 'path', 'directory', 'folder', 'organize', 'compress', 'convert', 'backup', 'copy', 'move'],
}

FILL_VALUES = {
    '{topic}': ['transformers', 'attention mechanisms', 'RLHF', 'vector databases', 'federated learning', 'model compression'],
    '{a}': ['PostgreSQL', 'MongoDB', 'Redis', 'Cassandra'],
    '{b}': ['Neo4j', 'InfluxDB', 'TimescaleDB', 'DynamoDB'],
    '{service}': ['nginx', 'postgresql', 'redis', 'docker', 'kubernetes', 'nginx'],
    '{condition}': ['CPU > 80%', 'error rate > 1%', 'disk full', 'memory leak detected'],
    '{app}': ['API gateway', 'auth service', 'worker queue', 'notion-sync'],
    '{person}': ['Rajesh from Rohtak', 'Priya Sharma', 'the engineering team', 'a potential partner'],
    '{situation}': ['no response for 3 days', 'objection about pricing', 'asking for demo'],
    '{list}': ['rohtak_coaching_list.csv', 'leads_q1.csv', 'partnerProspects.json'],
    '{metric}': ['conversion rate', 'API latency', 'user growth', 'revenue per user'],
    '{dataset}': ['sales_data.csv', 'user_events.json', 'logs.parquet'],
    '{path}': ['/home/hermes/skills', '/var/log', '~/projects'],
    '{rule}': ['type then date', 'priority then alphabetically', 'project folder structure'],
    '{file}': ['data.csv', 'image.png', 'video.mp4'],
    '{size}': ['10MB', '50MB', '100MB'],
    '{destination}': ['/backup', 's3://bucket', '~/backups'],
    '{pattern}': ['*.py', '*.md', '*.json', '**/test_*.py'],
}

def get_category(skill_text):
    """Infer category from skill keywords."""
    text_lower = skill_text.lower()
    scores = {}
    for cat, keywords in TASK_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        scores[cat] = score
    best_cat = max(scores, key=scores.__getitem__)
    return best_cat if scores[best_cat] > 0 else random.choice(list(TASK_KEYWORDS.keys()))

def fill_template(template, skill_text):
    """Fill template with domain-relevant values from skill text."""
    result = template
    for placeholder, values in FILL_VALUES.items():
        if placeholder in result:
            # Pick a value that appears in the skill, else random
            domain_keywords = re.findall(r'\b\w{5,}\b', skill_text.lower())[:50]
            matched = [v for v in values if any(kw in v.lower() for kw in domain_keywords)]
            chosen = random.choice(matched if matched else values)
            result = result.replace(placeholder, chosen)
    return result

def extract_key_terms(skill_text, n=5):
    """Extract key technical terms from skill for expected_behavior generation."""
    # Find things that look like tool names, file paths, config keys
    tools = re.findall(r'`([^`]+)`', skill_text)
    tools += re.findall(r'\b(hermes|terminal|patch|read_file|skill_view|cronjob|delegate_task)\b', skill_text, re.I)
    paths = re.findall(r'`/(?:[^`]+)`', skill_text)[:3]
    commands = re.findall(r'\b(python|git|npm|curl|wget|grep|awk|sed)\b', skill_text)
    terms = (tools + paths + commands)[:n]
    return terms

def make_expected_behavior(skill_text, category):
    """Generate expected_behavior from skill content without LLM."""
    terms = extract_key_terms(skill_text)
    term_str = ', '.join(terms[:3]) if terms else ''

    templates = {
        'coding': f"Follows the skill's procedure exactly — correct paths ({term_str or 'relevant files'}), step-by-step, no skipped steps. Output is actionable.",
        'research': f"Returns structured findings with specific references (titles, IDs, links). Mentions {term_str or 'key concepts'} correctly.",
        'ops': f"Uses the correct commands and configuration. Mentions {term_str or 'service names'} accurately. Follows the skill's troubleshooting sequence.",
        'messaging': f"Message matches the skill's template structure, personalized for recipient, clear CTA, correct format.",
        'data': f"Analysis is grounded in the actual data. Produces correct code/output. Uses {term_str or 'appropriate methods'} from the skill.",
        'file': f"Correct paths, proper commands, files organized as specified. No data loss, correct permissions.",
    }
    return templates.get(category, f"Follows skill procedure, produces correct output, mentions {term_str or 'key elements'} accurately.")

def generate_examples_for_skill(skill_name, skill_text):
    """Generate 10 heuristic examples for a skill — ZERO LLM calls."""
    category = get_category(skill_text)
    base_templates = TASK_TEMPLATES.get(category, TASK_TEMPLATES['coding'])

    # Generate 10 by cycling through templates with variations
    examples = []
    for i in range(10):
        template_set = base_templates[i % len(base_templates)]
        template, behavior_suffix = template_set
        task_input = fill_template(template, skill_text)
        expected_behavior = make_expected_behavior(skill_text, category)

        # Add some per-example variation
        if i >= 5:
            task_input = f"URGENT: {task_input}"

        difficulty = ['easy', 'medium', 'hard'][i % 3]
        examples.append(EvalExample(
            task_input=task_input,
            expected_behavior=expected_behavior,
            difficulty=difficulty,
            category=category,
            source='heuristic',
        ))

    # Split: 7 train, 2 val, 1 holdout
    random.shuffle(examples)
    return EvalDataset(
        train=examples[:7],
        val=examples[7:9],
        holdout=examples[9:],
    )

def scan_hermes_skills():
    """Find all skill directories."""
    if not HERMES_SKILLS.exists():
        print(f"Skills directory not found: {HERMES_SKILLS}")
        return []

    skills = []
    for skill_md in HERMES_SKILLS.rglob("SKILL.md"):
        name = skill_md.parent.name
        if name in ('SOUL.md', 'MEMORY.md', 'USER.md', 'AGENTS.md', 'CONSTITUTION.md'):
            continue
        skills.append((name, skill_md))
    return skills

def main():
    random.seed(42)
    output_base = Path(__file__).parent / 'datasets' / 'skills'
    output_base.mkdir(parents=True, exist_ok=True)

    skills = scan_hermes_skills()
    print(f"Found {len(skills)} skills to process")
    print()

    results = {'ok': 0, 'error': 0, 'skipped': 0}

    for name, skill_md in sorted(skills, key=lambda x: x[0]):
        out_dir = output_base / name

        # Check if already has valid dataset
        if (out_dir / 'train.jsonl').exists():
            # Verify it's valid JSON
            try:
                with open(out_dir / 'train.jsonl') as f:
                    for line in f:
                        json.loads(line)
                print(f"[SKIP] {name} — already has valid dataset")
                results['skipped'] += 1
                continue
            except:
                pass  # Corrupt, regenerate

        try:
            skill_text = skill_md.read_text()
            dataset = generate_examples_for_skill(name, skill_text)
            dataset.save(out_dir)

            total = len(dataset.all_examples)
            print(f"[OK] {name} — {total} examples ({len(dataset.train)}/{len(dataset.val)}/{len(dataset.holdout)})")
            results['ok'] += 1
        except Exception as e:
            print(f"[ERROR] {name}: {e}")
            results['error'] += 1

    print()
    print(f"Done: {results['ok']} generated, {results['skipped']} skipped, {results['error']} errors")

if __name__ == '__main__':
    main()