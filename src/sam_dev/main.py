from typing import Annotated

import dagger
from dagger import dag, function, object_type


@object_type
class SamDev:
    rootDir: Annotated[
        dagger.Directory,
        dagger.DefaultPath("."),
    ]

    @function(cache="never")
    async def verify_directory_file_caching(
        self,
        directory: Annotated[
            dagger.Directory,
            dagger.Ignore(
                [
                    ".env",
                    ".git",
                    "**/.venv",
                    "**__pycache__**",
                    ".dagger/sdk",
                    "**/.pytest_cache",
                    "**/.ruff_cache",
                    "**/node_modules",
                    "**/.evidence",
                ]
            ),
            dagger.DefaultPath("."),
        ],
    ) -> str:
        """Verifies that a file is cached"""
        return (
            await dag.container()
            .from_("alpine")
            .with_file("/file", directory.file("dagger.json"))
            .with_exec(["cat", "/file"])
            .stdout()
        )
