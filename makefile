# Define default Python environment management commands
.PHONY: compile sync

# Compile requirements.txt from requirements.in
compile:
	uv pip compile requirements.in -o requirements.txt

# Sync the environment with requirements.txt
sync:
	uv pip sync requirements.txt
