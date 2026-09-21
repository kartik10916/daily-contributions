"""
Realistic GitHub Contribution Graph Generator
- Apr-May 2025: 2 commits/week (light green)
- Sep-Dec 2025: 2 commits/week (light green)
- Jan-Sep 2026: Realistic 2-3 active days per week (~18-20 zero days per month, natural gaps)
"""

import os
import random
import subprocess
from datetime import datetime, timedelta

AUTHOR_NAME = "kartik10916"
AUTHOR_EMAIL = "166645119+kartik10916@users.noreply.github.com"

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(WORK_DIR, "activity.md")

APR_MAY_2025_START = datetime(2025, 4, 1)
APR_MAY_2025_END = datetime(2025, 5, 31)

SEP_DEC_2025_START = datetime(2025, 9, 1)
SEP_DEC_2025_END = datetime(2025, 12, 31)

START_DATE_2026 = datetime(2026, 1, 1)
END_DATE_2026 = datetime(2026, 9, 21)

MESSAGES = [
    "Refactor core module and clean up syntax",
    "Update project documentation and guidelines",
    "Improve test coverage and assertions",
    "Optimize memory usage and algorithm efficiency",
    "Fix edge cases in data parsing logic",
    "Add logging and telemetry enhancements",
    "Update dependency configurations",
    "Restructure file organization and clean up imports",
    "Enhance error handling and validation",
    "Refine utility helpers and helper methods",
    "Improve styling and UI component layout",
    "Update build scripts and packaging settings",
    "Benchmark processing speed and reduce overhead",
    "Add new helper functions for utility pipeline",
    "Sync daily progress and review code changes"
]

def run_cmd(cmd, env=None):
    result = subprocess.run(cmd, cwd=WORK_DIR, env=env, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running: {cmd}\n{result.stderr}")
    return result

def setup_repo():
    print("Setting up fresh branch for realistic commits...")
    run_cmd("git checkout --orphan realistic_main")
    run_cmd("git rm -rf .")

    run_cmd(f'git config user.name "{AUTHOR_NAME}"')
    run_cmd(f'git config user.email "{AUTHOR_EMAIL}"')

    readme_path = os.path.join(WORK_DIR, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("# Daily Activity Log\n\nContinuous development and daily coding practice log.\n")
    
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("# Activity History\n\n")

def add_weekly_commits(start_date, end_date, env, commit_tracker):
    curr_week_start = start_date
    while curr_week_start <= end_date:
        days_in_week = [curr_week_start + timedelta(days=i) for i in range(7) if curr_week_start + timedelta(days=i) <= end_date]
        if len(days_in_week) >= 2:
            chosen_days = sorted(random.sample(days_in_week, 2))
        else:
            chosen_days = days_in_week

        for day in chosen_days:
            hour = random.randint(11, 20)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            commit_time = day.replace(hour=hour, minute=minute, second=second)
            date_str = commit_time.strftime("%Y-%m-%dT%H:%M:%S+05:30")

            env["GIT_AUTHOR_DATE"] = date_str
            env["GIT_COMMITTER_DATE"] = date_str

            msg = random.choice(MESSAGES)
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(f"- `{date_str}`: {msg}\n")

            run_cmd("git add activity.md", env=env)
            run_cmd(f'git commit -m "{msg}"', env=env)
            commit_tracker[0] += 1

        curr_week_start += timedelta(days=7)

def generate_commits():
    env = os.environ.copy()
    env["GIT_AUTHOR_NAME"] = AUTHOR_NAME
    env["GIT_AUTHOR_EMAIL"] = AUTHOR_EMAIL
    env["GIT_COMMITTER_NAME"] = AUTHOR_NAME
    env["GIT_COMMITTER_EMAIL"] = AUTHOR_EMAIL

    commit_tracker = [0]

    # Initial commit April 1, 2025
    init_date_str = APR_MAY_2025_START.replace(hour=9, minute=30, second=0).strftime("%Y-%m-%dT%H:%M:%S+05:30")
    env["GIT_AUTHOR_DATE"] = init_date_str
    env["GIT_COMMITTER_DATE"] = init_date_str
    run_cmd("git add README.md activity.md", env=env)
    run_cmd('git commit -m "Initial commit: Daily development activity tracker"', env=env)
    commit_tracker[0] += 1

    # 1. April & May 2025 (2 commits per week)
    print("Generating April & May 2025 commits (2/week)...")
    add_weekly_commits(APR_MAY_2025_START, APR_MAY_2025_END, env, commit_tracker)

    # 2. Sep to Dec 2025 (2 commits per week)
    print("Generating Sep-Dec 2025 commits (2/week)...")
    add_weekly_commits(SEP_DEC_2025_START, SEP_DEC_2025_END, env, commit_tracker)

    # 3. 2026: Realistic 2-3 active days per week (~18-20 zero days per month)
    print("Generating realistic 2026 commits (2-3 days active per week, rest zero)...")
    curr_week_start = START_DATE_2026
    total_active_days_2026 = 0
    total_zero_days_2026 = 0

    # Let's seed random for consistent realistic distribution
    random.seed(42)

    while curr_week_start <= END_DATE_2026:
        # Get days in this week up to END_DATE_2026
        days_in_week = [curr_week_start + timedelta(days=i) for i in range(7) if curr_week_start + timedelta(days=i) <= END_DATE_2026]
        
        # Natural break: 5% chance to take an entire week off (e.g. exam week, vacation)
        is_break_week = random.random() < 0.06

        if is_break_week or len(days_in_week) == 0:
            total_zero_days_2026 += len(days_in_week)
            curr_week_start += timedelta(days=7)
            continue

        # Choose 2 or 3 active days this week (prefer weekdays: Mon, Tue, Wed, Thu, Fri; rarely weekend)
        num_active = random.choices([2, 3], weights=[60, 40])[0]
        num_active = min(num_active, len(days_in_week))

        # Weight weekdays higher than weekends
        weights = []
        for d in days_in_week:
            if d.weekday() in [1, 2, 3]:  # Tue, Wed, Thu
                weights.append(3.0)
            elif d.weekday() in [0, 4]:  # Mon, Fri
                weights.append(2.0)
            elif d.weekday() == 5:       # Sat
                weights.append(0.8)
            else:                        # Sun
                weights.append(0.3)

        # Pick active days
        active_days = []
        available = list(zip(days_in_week, weights))
        for _ in range(num_active):
            total_w = sum(w for _, w in available)
            r = random.uniform(0, total_w)
            cum = 0
            for idx, (day, w) in enumerate(available):
                cum += w
                if cum >= r:
                    active_days.append(day)
                    available.pop(idx)
                    break

        active_days.sort()
        total_active_days_2026 += len(active_days)
        total_zero_days_2026 += (len(days_in_week) - len(active_days))

        for day in active_days:
            # 1 to 2 commits on active days (mostly 1, sometimes 2, rare 3 for natural variation)
            num_commits = random.choices([1, 2, 3], weights=[65, 28, 7])[0]
            for _ in range(num_commits):
                commit_tracker[0] += 1
                hour = random.randint(10, 22)
                minute = random.randint(0, 59)
                second = random.randint(0, 59)
                commit_time = day.replace(hour=hour, minute=minute, second=second)
                date_str = commit_time.strftime("%Y-%m-%dT%H:%M:%S+05:30")

                env["GIT_AUTHOR_DATE"] = date_str
                env["GIT_COMMITTER_DATE"] = date_str

                msg = random.choice(MESSAGES)
                with open(LOG_FILE, "a", encoding="utf-8") as f:
                    f.write(f"- `{date_str}`: {msg}\n")

                run_cmd("git add activity.md", env=env)
                run_cmd(f'git commit -m "{msg}"', env=env)

        curr_week_start += timedelta(days=7)

    print(f"\n2026 Summary:")
    print(f"  Active days: {total_active_days_2026}")
    print(f"  Zero/grey days: {total_zero_days_2026} (~{total_zero_days_2026 // 8.7:.0f} zero days per month)")
    print(f"  Total commits: {commit_tracker[0]}")

    # Set as main
    run_cmd("git checkout -B main")
    run_cmd("git branch -D realistic_main")

if __name__ == "__main__":
    setup_repo()
    generate_commits()
