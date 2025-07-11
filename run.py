#!/usr/bin/env python
"""The run script."""
import logging
import os
from pathlib import Path
from typing import List, Tuple, Union

# import flywheel functions
from flywheel_gear_toolkit import GearToolkitContext
from app.main import superfield_process


# The gear is split up into 2 main components. The run.py file which is executed
# when the container runs. The run.py file then imports the rest of the gear as a
# module.
log = logging.getLogger(__name__)

def main(context: GearToolkitContext) -> None:
    """Parses config and runs."""

    log.info("Starting Super-Field processing gear")

    # Example: Get the Flywheel gear inputs
    input_folder = '/flywheel/v0/input'
    output_folder = '/flywheel/v0/work'
    spacing = tuple(context.config.get('spacing', [1.0, 1.0, 1.0]))
    intensity_upper = context.config.get('intensity_upper', 3000)
    sw_overlap = context.config.get('sw_overlap', 0.9)
    sw_batch_size = context.config.get('sw_batch_size', 8)

    # Call your imported function
    superfield_process(
        input_folder,
        output_folder,
        spacing,
        intensity_upper,
        sw_overlap,
        sw_batch_size
    )

    log.info("Gear complete!")


# Only execute if file is run as main, not when imported by another module
if __name__ == "__main__":  # pragma: no cover
    # Get access to gear config, inputs, and sdk client if enabled.
    with GearToolkitContext() as gear_context:

        # Initialize logging, set logging level based on `debug` configuration
        # key in gear config.
        gear_context.init_logging()

        # Pass the gear context into main function defined above.
        main(gear_context)