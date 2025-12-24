import importlib.util
import logging
import pathlib
from discord import app_commands

logger = logging.getLogger("cypher_bot")

async def commands_load(tree: app_commands.CommandTree) -> int:
    # Prefer a project-level Commands/ directory (../Commands relative to this file),
    # but keep compatibility with events/Commands if you create it later.
    candidates = [
        pathlib.Path(__file__).resolve().parent.parent / "Commands",
        pathlib.Path(__file__).resolve().parent / "Commands",
    ]

    commands_path = next((p for p in candidates if p.exists()), candidates[0])

    if not commands_path.exists():
        logger.warning("Commands directory not found: %s", commands_path)
        return 0

    logger.debug("Scanning commands directory: %s", commands_path)

    count = 0

    for file_path in sorted(commands_path.glob("*.py")):
        module_name = file_path.stem
        logger.debug("Loading module: %s", module_name)

        try:
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec is None or spec.loader is None:
                logger.error("Failed to create import spec for %s", module_name)
                continue

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, "command"):
                tree.add_command(module.command)
                count += 1
                logger.info("Loaded command: /%s", module.command.name)
            else:
                logger.warning("Module %s.py has no 'command'", module_name)

        except Exception:
            logger.exception("Failed to load module %s", module_name)

    try:
        synced = await tree.sync()
        logger.info("Successfully synced %d global application commands", len(synced))
    except Exception:
        logger.exception("Failed to sync commands")

    return count
