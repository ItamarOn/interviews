# CityMap Exercise

## Overview

Start by reviewing the `City topology - Frame 1.jpg` to get a visual understanding of the city infrastructure.

Welcome to the CityMap modeling exercise! In this challenge, you'll work with a city infrastructure consisting of houses, neighborhoods, security gates, junctions, highways, and an airport. The goal is to build a Python class, `CityMap`, which can determine valid paths between entities in the map based on provided connections and rules.

## Key Concepts

- Find valid paths between entities (e.g., houses, neighborhoods, airport).
- Main requirement: find a path between two houses or between a house and the airport.
- Apply access rules (e.g., security gate restrictions).

## File Structure

- **`map.py`**: Implement the `CityMap` class.
- **`test_map.py`**: Unit tests to validate your implementation.
- **`map_entities.json`**: Describes map entities and relationships.
- **`map_expected_paths.json`**: Contains expected paths for test cases.
- **`City topology - Frame 1.jpg`**: Visual diagram of the topology.

## Getting Started

1. **Understand the Topology**: Review `City topology - Frame 1.jpg` and `map_entities.json` to understand the structure and relationships.

2. **Entity Details**:
   - **Houses**: Each house belongs to a neighborhood (e.g., `house-a` in `nbh-bavli`).
   - **Neighborhoods**: Associated with security gates (e.g., `nbh-bavli` has `sg-1`).
   - **Security Gates**: Each gate has entrance and exit rules (e.g., `sg-1` allows entrance for certain addresses).
   - **Junctions, Highways, City, Airport**: Connect neighborhoods and other entities.

   **Example from `map_entities.json`**:
   ```json
   {
     "houses": [
       {"house_address": "33", "entity_id": "house-a", "neighborhood_id": "nbh-bavli"},
       {"house_address": "152", "entity_id": "house-b", "neighborhood_id": "nbh-bavli"}
     ],
     "neighborhoods": [
       {
         "entity_id": "nbh-bavli",
         "sg_id": "sg-1",
         "exits": ["junction-rokach"]
       }
     ]
   }
   ```
   This example shows `house-a` and `house-b` in `nbh-bavli`, associated with `sg-1`.

3. **Implement the `CityMap` Class**: In `map.py`, complete `CityMap` by implementing `get_path(src_id, dst_id)`, which returns a valid path considering all rules.

4. **Run Tests**: Use `test_map.py` to validate paths. Each test case uses `map_expected_paths.json` to verify correctness.

   **Example from `map_expected_paths.json`**:
   ```json
   {
     "test1": [
       "house-a", "sg-1", "nbh-bavli", "junction-rokach", "city-tlv", "nbh-ramataviv", "sg-2", "house-d"
     ]
   }
   ```
   This example shows the expected path for `test1`, from `house-a` to `house-d`.

## Running the Tests

To run the tests, use:

```bash
python -m unittest test_map.py
```

## Expectations

Focus on quality work and explaining your approach. There is no single solution, and discussing your reasoning is important. Consider complexity and performance, aiming for an efficient implementation.

Good luck, and have fun implementing the CityMap!