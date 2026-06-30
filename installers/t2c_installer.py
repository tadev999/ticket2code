#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def ensure_target_dir(path: Path) -> None:
    if not path.is_dir():
        raise SystemExit(f"ERROR: target directory does not exist: {path}")


def copy_tree(src: Path, dst: Path) -> None:
    shutil.copytree(src, dst, dirs_exist_ok=True)


def reset_workflow_dirs(target_dir: Path) -> None:
    for path in [
        target_dir / "ticket2code" / "code",
        target_dir / "ticket2code" / "review",
        target_dir / "ticket2code" / "integration-tests",
        target_dir / "ticket2code" / "screen-transition-tests",
    ]:
        if path.exists():
            shutil.rmtree(path)


def install(target_dir: Path) -> int:
    src_dir = repo_root()
    ensure_target_dir(target_dir)

    print(f"Installing ticket2code core into: {target_dir}")

    for rel_path in [
        ".github",
        "docs/report",
        "docs/test/integration",
        "docs/test/screen-transition",
        "ticket2code",
    ]:
        (target_dir / rel_path).mkdir(parents=True, exist_ok=True)

    copy_tree(src_dir / "core" / "prompts", target_dir / ".github" / "prompts")
    copy_tree(src_dir / "core" / "skills", target_dir / ".github" / "skills")
    copy_tree(src_dir / "core" / "hooks", target_dir / ".github" / "hooks")

    reset_workflow_dirs(target_dir)

    copy_tree(src_dir / "workflows" / "code", target_dir / "ticket2code" / "code")
    copy_tree(src_dir / "workflows" / "review", target_dir / "ticket2code" / "review")
    copy_tree(
        src_dir / "workflows" / "integration",
        target_dir / "ticket2code" / "integration-tests",
    )
    copy_tree(
        src_dir / "workflows" / "screen-transition",
        target_dir / "ticket2code" / "screen-transition-tests",
    )
    shutil.copy2(
        src_dir / "templates" / "project" / "SETUP.md",
        target_dir / "ticket2code" / "SETUP.md",
    )

    config_path = target_dir / "ticket2code.config.yaml"
    if not config_path.exists():
        shutil.copy2(
            src_dir / "templates" / "project" / "ticket2code.config.yaml",
            config_path,
        )

    env_path = target_dir / ".env.local"
    if not env_path.exists():
        shutil.copy2(
            src_dir / "templates" / "project" / "env.local.example",
            target_dir / ".env.local.example",
        )

    print("Done.")
    print("Next steps:")
    print(f"1) Edit {config_path}")
    print(f"2) Create {target_dir / '.env.local'} from .env.local.example")
    print(
        "3) Run: "
        f"{src_dir / 'installers' / 't2c_installer.py'} doctor --target-dir {target_dir}"
    )
    return 0


def uninstall(target_dir: Path) -> int:
    print(f"Removing ticket2code runtime assets from: {target_dir}")

    paths = [
        target_dir / "ticket2code",
        target_dir / ".github" / "prompts" / "t2c_code.prompt.md",
        target_dir / ".github" / "prompts" / "t2c_integration_tests.prompt.md",
        target_dir / ".github" / "prompts" / "t2c_screen_transition_tests.prompt.md",
        target_dir / ".github" / "prompts" / "t2c_review.prompt.md",
        target_dir / ".github" / "skills" / "jira-pbi-analysis",
        target_dir / ".github" / "skills" / "figma-design-analysis",
        target_dir / ".github" / "skills" / "figma-svg-export",
        target_dir / ".github" / "skills" / "ac-decomposition",
        target_dir / ".github" / "skills" / "dead-code-cleanup",
        target_dir / ".github" / "skills" / "git-diff-analysis",
        target_dir / ".github" / "skills" / "test-environment-designer",
        target_dir / ".github" / "skills" / "design-image-ocr-analysis",
        target_dir / ".github" / "hooks" / "safety-guard.json",
        target_dir / ".github" / "hooks" / "scripts" / "pre_tool_guard.py",
    ]

    for path in paths:
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists():
            path.unlink()

    print("Removed runtime assets. Project files remain unchanged.")
    return 0


def upgrade(target_dir: Path) -> int:
    src_dir = repo_root()
    ensure_target_dir(target_dir)

    print(f"Upgrading ticket2code runtime assets in: {target_dir}")

    (target_dir / ".github").mkdir(parents=True, exist_ok=True)
    (target_dir / "ticket2code").mkdir(parents=True, exist_ok=True)

    copy_tree(src_dir / "core" / "prompts", target_dir / ".github" / "prompts")
    copy_tree(src_dir / "core" / "skills", target_dir / ".github" / "skills")
    copy_tree(src_dir / "core" / "hooks", target_dir / ".github" / "hooks")

    reset_workflow_dirs(target_dir)

    copy_tree(src_dir / "workflows" / "code", target_dir / "ticket2code" / "code")
    copy_tree(src_dir / "workflows" / "review", target_dir / "ticket2code" / "review")
    copy_tree(
        src_dir / "workflows" / "integration",
        target_dir / "ticket2code" / "integration-tests",
    )
    copy_tree(
        src_dir / "workflows" / "screen-transition",
        target_dir / "ticket2code" / "screen-transition-tests",
    )
    shutil.copy2(
        src_dir / "templates" / "project" / "SETUP.md",
        target_dir / "ticket2code" / "SETUP.md",
    )

    print("Upgrade completed")
    return 0


def doctor(target_dir: Path) -> int:
    missing = False

    checks = [
        ".github/prompts/t2c_code.prompt.md",
        ".github/skills/jira-pbi-analysis/SKILL.md",
        ".github/hooks/safety-guard.json",
        "ticket2code/code/code-agent.md",
        "ticket2code/code/code-processor.prompt.md",
        "ticket2code/review/review-agent.md",
        "ticket2code/integration-tests/integration-tests-agent.md",
        "ticket2code/screen-transition-tests/screen-transition-tests-agent.md",
        "ticket2code/SETUP.md",
        "ticket2code.config.yaml",
        ".env.local",
    ]

    # Keep compatibility with old/new naming for the figma skill.
    figma_checks = [
        ".github/skills/figma-design-analysis/SKILL.md",
        ".github/skills/figma-svg-export/SKILL.md",
    ]

    for rel_path in checks:
        full_path = target_dir / rel_path
        if full_path.exists():
            print(f"OK   {rel_path}")
        else:
            print(f"MISS {rel_path}")
            missing = True

    if any((target_dir / rel_path).exists() for rel_path in figma_checks):
        print("OK   .github/skills/figma-*/SKILL.md")
    else:
        print("MISS .github/skills/figma-*/SKILL.md")
        missing = True

    if missing:
        print("Doctor check failed. Missing required files.")
        return 1

    print("Doctor check passed.")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Cross-platform installer for Ticket2Code runtime assets."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in ["install", "uninstall", "upgrade", "doctor"]:
        sub = subparsers.add_parser(command)
        sub.add_argument(
            "--target-dir",
            default=str(Path.cwd()),
            help="Target project directory (defaults to current directory).",
        )

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    target_dir = Path(args.target_dir).expanduser().resolve()

    if args.command == "install":
        return install(target_dir)
    if args.command == "uninstall":
        return uninstall(target_dir)
    if args.command == "upgrade":
        return upgrade(target_dir)
    if args.command == "doctor":
        return doctor(target_dir)

    raise SystemExit(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())