# Cooper's Dotfiles

Reproducible development environment using Nix flakes, home-manager, and nix-darwin.

## Overview

Two configurations:

| Config | Platform | Use Case | Command |
|--------|----------|----------|---------|
| `cooper@linux` | Linux x86_64 | VMs, servers (headless) | `home-manager switch --flake .#cooper@linux` |
| `coopers-macbook-pro` | macOS ARM | Workstation (full setup) | `darwin-rebuild switch --flake .#coopers-macbook-pro` |

## Quick Start

### Prerequisites

Install Nix with flakes:

```bash
curl --proto '=https' --tlsv1.2 -sSf -L https://install.determinate.systems/nix | sh -s -- install
```

### New Linux VM

```bash
git clone https://github.com/crcorbett/dotenv.git ~/dotenv
cd ~/dotenv

nix run home-manager -- switch --flake .#cooper@linux

./scripts/setup-tailscale.sh --ssh

cp .secrets.example ~/.secrets
# Edit ~/.secrets with your API keys
```

### New macOS Workstation

```bash
git clone https://github.com/crcorbett/dotenv.git ~/dotenv
cd ~/dotenv

nix run nix-darwin -- switch --flake .#coopers-macbook-pro

cp .secrets.example ~/.secrets
# Edit ~/.secrets with your API keys

# Install apps (see APPS.md)
```

### Updating

```bash
cd ~/dotenv
git pull

# Linux
home-manager switch --flake .#cooper@linux

# macOS
darwin-rebuild switch --flake .#coopers-macbook-pro
```

## Repository Structure

```
dotenv/
├── flake.nix                 # Main entry - defines configurations
├── flake.lock                # Pinned dependencies
│
├── home/
│   ├── core.nix              # Shared: CLI tools, dotfiles, mosh
│   ├── workstation.nix       # macOS: fonts, app configs (Ghostty/Zed/Cursor)
│   ├── p10k.zsh              # Powerlevel10k theme
│   └── dotfiles/
│       ├── zshrc             # Shell config
│       ├── p10k.zsh          # Powerlevel10k theme
│       ├── gitconfig         # Git config with 1Password signing
│       ├── gitconfig-macos   # macOS 1Password path
│       ├── gitconfig-linux   # Linux 1Password path
│       ├── ssh_config        # SSH config
│       └── ghostty.conf      # Terminal config
│
├── darwin/
│   └── system.nix            # macOS system preferences
│
├── nixos/
│   └── configuration.nix     # NixOS system config (if needed)
│
├── configs/                  # Workstation app configs (macOS)
│   ├── zed/
│   │   ├── settings.json
│   │   └── keymap.json
│   └── cursor/
│       └── settings.json
│
├── scripts/
│   ├── project-codex-skills.py # Validate/install/roll back shared Codex skills
│   ├── setup-tailscale.sh    # Tailscale install + auth
│   └── exit_node_setup.sh    # Configure VM as exit node
│
├── codex/
│   └── skills/               # Canonical shared engineering skills + manifest
│
├── APPS.md                   # Manual app installation list
├── SSH_SETUP.md              # 1Password SSH setup guide
├── .secrets.example          # Template for secrets file
└── README.md
```

## What's Included

### Shared Codex skills

`codex/skills/` is the version-controlled semantic source for the shared
engineering skills listed in its manifest. `~/.codex/skills` is an installed
projection, not an editing surface. The projection command validates source
digests, stages copies, preserves a last-known-good backup, replaces only the
manifest-named skills, and reads the result back:

```bash
python3 scripts/project-codex-skills.py --check
python3 scripts/project-codex-skills.py --install
```

Use the backup ID from an installation receipt to recover:

```bash
python3 scripts/project-codex-skills.py --rollback BACKUP_ID
```

Commit and review source changes before installation. The script never pushes,
publishes, or changes skills omitted from the manifest.

### Both Platforms (core.nix)

- **Shell**: zsh + oh-my-zsh + Powerlevel10k
- **Tools**: git, gh, ripgrep, fd, fzf, eza, zoxide, delta, lazygit, neovim, direnv
- **Network**: mosh (low-latency SSH for high-latency connections)
- **SSH**: 1Password integration (see [SSH_SETUP.md](SSH_SETUP.md))
- **Git**: 1Password SSH commit signing

### macOS Workstation (workstation.nix + darwin/system.nix)

- **Fonts**: Nerd Fonts (Meslo, JetBrains Mono)
- **App configs**: Ghostty, Zed, Cursor
- **System prefs**: Dock autohide, dark mode, text replacements
- **Services**: Tailscale, Touch ID for sudo

## Secrets

API keys and tokens are stored in `~/.secrets` (not in repo):

```bash
cp .secrets.example ~/.secrets
vim ~/.secrets
```

The zshrc automatically sources this file if it exists.

## Tailscale

### Linux VM (Client)

```bash
./scripts/setup-tailscale.sh --ssh
```

Opens a URL - authenticate with Google.

### Linux VM (Exit Node)

To configure a VM as a Tailscale exit node (VPN endpoint):

```bash
./scripts/setup-tailscale.sh --exit-node
./scripts/exit_node_setup.sh
```

Then approve the exit node in [Tailscale admin console](https://login.tailscale.com/admin/machines).

The exit node script configures:
- IP forwarding (IPv4 + IPv6)
- UDP GRO optimization for better throughput
- Persistence across reboots

### macOS

Tailscale is enabled via nix-darwin. After first run:

```bash
tailscale up --ssh
```

### Using an Exit Node

From any Tailscale device:

```bash
tailscale up --exit-node=<exit-node-ip>
```

## Mosh (Mobile Shell)

For high-latency connections (e.g., UK → Australia), use mosh instead of SSH:

```bash
mosh user@hostname
```

Mosh provides local echo and handles connection interruptions gracefully.

## Shell Aliases

| Alias | Command |
|-------|---------|
| `ll` | `ls -la` |
| `gs` | `git status` |
| `gp` | `git push` |
| `gl` | `git pull` |
| `lg` | `lazygit` |
| `vim`, `v` | `nvim` |
| `signin` | Sign in to 1Password CLI (personal + work) |

## Text Replacements (macOS)

| Type | Expands To |
|------|------------|
| `@@` | coopercorbett@gmail.com |
| `@&` | cooper.corbett@tilt.legal |
| `omw` | On my way! |

## Updating Nix Packages

```bash
cd ~/dotenv
nix flake update
darwin-rebuild switch --flake .#coopers-macbook-pro  # or home-manager for Linux
```

## Adding Packages

Edit the appropriate file:

- **All platforms**: `home/core.nix` → `home.packages`
- **macOS only**: `home/workstation.nix` → `home.packages`
- **macOS system**: `darwin/system.nix` → `environment.systemPackages`

## SSH & Git Authentication

For detailed SSH setup instructions (including 1Password SSH agent, SSH bookmarks, and troubleshooting), see **[SSH_SETUP.md](SSH_SETUP.md)**.

## Git Commit Signing

All commits are automatically signed using SSH keys stored in 1Password. No special commands needed — `git commit` just works.

### Architecture

```
gitconfig (base)
├── commit.gpgsign = true             # Auto-sign all commits
├── user.signingkey = ssh-ed25519...  # Public key
├── gpg.format = ssh
│
├── [includeIf "gitdir:/Users/"]      # macOS
│   └── gitconfig-macos
│       └── program = /Applications/1Password.app/.../op-ssh-sign
│
└── [includeIf "gitdir:/home/"]       # Linux
    └── gitconfig-linux
        └── program = ~/.local/bin/op-ssh-sign-headless
```

### macOS (Desktop)

Uses 1Password desktop app's built-in `op-ssh-sign` binary. Requires:
- 1Password desktop app installed
- SSH agent enabled in 1Password settings
- SSH key added to 1Password

### Linux Headless VMs

Uses a local SSH key stored at `~/.ssh/id_ed25519_signing`. Simpler than the 1Password CLI approach and doesn't require re-authentication.

**First-time setup** — extract the signing key from 1Password:

```bash
# Sign in to 1Password CLI
eval $(op signin --account my)

# Extract the signing key
op item get "Github commit signing" --vault Development --fields "private key" --reveal > ~/.ssh/id_ed25519_signing
chmod 600 ~/.ssh/id_ed25519_signing

op item get "Github commit signing" --vault Development --fields "public key" > ~/.ssh/id_ed25519_signing.pub
chmod 644 ~/.ssh/id_ed25519_signing.pub
```

**Verify it works:**

```bash
git commit --allow-empty -m "test signing"
git log --show-signature -1
```

The gitconfig-linux overrides the signing key path to use the local file.

> **Note**: For SSH authentication setup (not commit signing), see [SSH_SETUP.md](SSH_SETUP.md).

### GitHub Setup

For commits to show as "Verified" on GitHub:

1. Go to [GitHub SSH Keys](https://github.com/settings/keys)
2. Click **New SSH key**
3. Set **Key type: Signing Key** (not Authentication)
4. Paste your public key
5. Ensure your commit email matches a verified email on your GitHub account

### Troubleshooting

| Issue | Solution |
|-------|----------|
| "Unverified" on GitHub | Add key as **Signing Key** (not just Authentication) in GitHub settings |
| "Permission denied" on gitconfig | Edit source in `~/dotfiles/home/dotfiles/`, rebuild with `home-manager switch` |
| Signing fails on Linux | Ensure `~/.ssh/id_ed25519_signing` exists (see extraction steps above) |
| "Too many authentication failures" | Set up SSH Bookmarks — see [SSH_SETUP.md](SSH_SETUP.md#ssh-bookmarks-solving-the-6-key-limit) |
| Shell not found on Linux VM | Run `home-manager switch` to fix nix PATH — see [SSH_SETUP.md](SSH_SETUP.md#troubleshooting) |

## License

Personal configuration - feel free to fork and adapt.
