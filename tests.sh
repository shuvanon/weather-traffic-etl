#!/bin/bash

# Run the fast, network-free unit tests.
# The live integration tests are deselected here; run them with: pytest -m integration
pytest -m "not integration"
