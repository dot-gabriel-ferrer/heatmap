# Examples

This directory contains example scripts demonstrating various features of the heatmap generator.

## Available Examples

### basic_example.py
Generate a simple heatmap from random point cloud data.

```bash
python examples/basic_example.py
```

### json_example.py
Create a heatmap from JSON coordinate data.

```bash
python examples/json_example.py
```

### animation_example.py
Create an animated heatmap showing temporal changes.

```bash
python examples/animation_example.py
```

## Sample Data

The `sample_data.json` file contains example coordinate data that can be used with the JSON example or CLI.

## Using the CLI

You can also use the command-line interface to run examples:

```bash
# Generate from JSON
python cli.py generate --input examples/sample_data.json --output examples/cli_output.png

# Create animation
python cli.py animate --frames 50 --output examples/cli_animation.gif
```
