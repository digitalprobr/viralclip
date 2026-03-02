#!/usr/bin/env python3
import argparse
import subprocess
import sys
import os
from pathlib import Path

# Color constants for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

def check_docker():
    """Verify if Docker daemon is running."""
    try:
        subprocess.run(["docker", "info"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def discover_projects():
    """Find all directories in the parent folder that contain a docker-compose.yml file."""
    base_dir = Path(__file__).parent.parent
    projects = {}
    for item in base_dir.iterdir():
        if item.is_dir() and (item / "docker-compose.yml").exists():
            projects[item.name] = item
    return projects

def run_compose_command(args_list, description, cwd=None):
    """Run a docker compose command safely (no shell=True)."""
    print(f"🚀 {BLUE}{description}{RESET}...")
    try:
        subprocess.run(args_list, check=True, cwd=cwd)
        print(f"✅ {GREEN}{description} success !{RESET}")
    except subprocess.CalledProcessError as e:
        print(f"❌ {RED}Error during {description}: {e}{RESET}")
        return False
    return True

def manage_project(action, project_name, project_path, run_args=None, extra_args=None):
    """Execute docker-compose commands for a specific project."""
    if action == "start":
        run_compose_command(["docker", "compose", "up", "-d", "--build"], f"Starting {project_name}", cwd=project_path)
    elif action == "stop":
        run_compose_command(["docker", "compose", "down"], f"Stopping {project_name}", cwd=project_path)
    elif action == "restart":
        run_compose_command(["docker", "compose", "restart"], f"Restarting {project_name}", cwd=project_path)
    elif action == "status":
        run_compose_command(["docker", "compose", "ps"], f"Status of {project_name}", cwd=project_path)
    elif action == "run" and run_args:
        # Safe: each argument is passed separately, no shell interpolation
        cmd = ["docker", "compose", "exec", "clipping-env", "python", "main.py", run_args]
        if extra_args and extra_args.clips:
            cmd.extend(["--clips", str(extra_args.clips)])
        run_compose_command(cmd, f"Running pipeline in {project_name}", cwd=project_path)

def main():
    if not check_docker():
        print(f"❌ {RED}Error: Docker daemon is not running. Please start Docker Desktop and try again.{RESET}")
        sys.exit(1)

    projects = discover_projects()
    
    parser = argparse.ArgumentParser(description="Multi-Project Manager")
    parser.add_argument("command", choices=["start", "stop", "restart", "status", "list", "run"], help="Action to perform")
    parser.add_argument("project", nargs="?", help="Project name (e.g., 08_clipping). Use 'all' for all projects.")
    parser.add_argument("--url", help="URL for the 'run' command")
    parser.add_argument("--clips", "-c", type=int, help="Number of clips to generate (overrides settings.yaml)")

    args = parser.parse_args()

    if args.command == "list":
        print(f"{BLUE}Available projects:{RESET}")
        for p in sorted(projects.keys()):
            print(f" - {p}")
        return

    if not args.project:
        print(f"❌ {RED}Error: Please specify a project name or 'all'.{RESET}")
        parser.print_help()
        sys.exit(1)

    target_projects = []
    if args.project == "all":
        target_projects = sorted(projects.keys())
    elif args.project in projects:
        target_projects = [args.project]
    else:
        print(f"❌ {RED}Error: Project '{args.project}' not found.{RESET}")
        sys.exit(1)

    for p_name in target_projects:
        manage_project(args.command, p_name, projects[p_name], args.url, extra_args=args)

if __name__ == "__main__":
    main()
