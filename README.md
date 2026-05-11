# Global Protocol: Old World Order

[![Latest Release](https://img.shields.io/github/v/release/Dorlion-Interactive/Global-Protocol-Old-World-Order-Mod?label=download&style=for-the-badge&logo=github)](https://github.com/Dorlion-Interactive/Global-Protocol-Old-World-Order-Mod/releases/latest/download/old-world-order-latest.zip)
[![Total Downloads](https://img.shields.io/github/downloads/Dorlion-Interactive/Global-Protocol-Old-World-Order-Mod/total?style=for-the-badge)](https://github.com/Dorlion-Interactive/Global-Protocol-Old-World-Order-Mod/releases)
[![License](https://img.shields.io/github/license/Dorlion-Interactive/Global-Protocol-Old-World-Order-Mod?style=for-the-badge)](LICENSE)

![Global Protocol: Old World Order Logo](logo.png)

A historical total conversion mod for **[Global Protocol: New World Order](https://globalprotocolgame.com)** — play the world as it was in **1450 AD**.

~120 playable nations · Ottoman Empire · Ming Dynasty · Aztec Empire · Kingdom of France · and more.

---

## For Players

If you just want to play the mod:

1. Download **[old-world-order-latest.zip](https://github.com/Dorlion-Interactive/Global-Protocol-Old-World-Order-Mod/releases/latest/download/old-world-order-latest.zip)**
2. Extract it into:
   ```
   %LOCALAPPDATA%\NewWorldOrder\Mods\globalprotocol.old_world_order\
   ```
3. Start Global Protocol, open **Mods**, enable **Old World Order**, then launch the 1450 scenario.

No build step is needed.

---

## For Developers

If you want to clone this repo and build your own version of the mod:

1. Clone the repository.
2. Open the project in VS Code.
3. Run `install.bat /dotnet` to build the C# WASM version and install it into the correct game folder.
4. If you only want the AssemblyScript version, run `install.bat /as` instead.
5. Make your changes, then run the installer again to rebuild and redeploy.

For build details and reference material, see the **[Wiki](https://github.com/Dorlion-Interactive/Global-Protocol-Old-World-Order-Mod/wiki)**.

*Visit the official site: [globalprotocolgame.com](https://globalprotocolgame.com)*
