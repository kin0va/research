from __future__ import annotations



from pathlib import Path
import json
from typing import Any

from structs.room_params import RoomParams

PathLike = str | Path


def single_room_json(path: PathLike) -> tuple[str, RoomParams]:
    """Load room metadata from a JSON file.

    This helper reads a JSON file containing room and location metadata,
    validates the expected top-level keys, and returns a tuple with the
    `LocationID` and a constructed `RoomParams` object so callers can
    associate geometry with the source location.
    """
    # Read and parse a JSON file, then delegate to the payload parser.
    json_path = Path(path)

    # Ensure the file exists before attempting to read it.
    if not json_path.exists():
        raise FileNotFoundError(f"JSON file not found: {json_path}")

    raw_text = json_path.read_text(encoding="utf-8")
    if not raw_text.strip():
        raise ValueError(f"JSON file is empty: {json_path}")

    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Failed to parse JSON file {json_path}: {exc.msg}"
        ) from exc

    # Delegate to the shared payload parsing/validation helper so logic is
    # identical for single-file and multi-file loaders.
    return _parse_room_payload(payload)


def _parse_room_payload(payload: dict[str, Any]) -> tuple[str, RoomParams]:
    """Validate a parsed JSON payload and construct RoomParams.

    This function centralizes validation rules and mapping from JSON keys
    to the `RoomParams` constructor. It returns (LocationID, RoomParams).
    """

    # Validate required top-level keys
    required_keys = ["LocationID", "Room", "AverageMaxOccupancy"]
    missing_keys = [key for key in required_keys if key not in payload]
    if missing_keys:
        raise ValueError(
            "Missing required room metadata keys: "
            f"{', '.join(missing_keys)}"
        )

    room_payload = payload["Room"]
    if not isinstance(room_payload, dict):
        raise ValueError("Expected 'Room' to be an object in JSON metadata.")

    # Validate geometry keys inside the Room object. Note: Volume can be
    # omitted by some authors; we tolerate that by using get() below.
    required_room_keys = ["Height_m", "Width_m", "Length_m"]
    missing_room_keys = [key for key in required_room_keys if key not in room_payload]
    if missing_room_keys:
        raise ValueError(
            "Missing required room geometry keys: "
            f"{', '.join(missing_room_keys)}"
        )

    # Extract values and construct RoomParams
    location_id = payload["LocationID"]
    height = room_payload["Height_m"]
    width = room_payload["Width_m"]
    length = room_payload["Length_m"]
    volume = room_payload.get("Volume_m3")
    max_occupancy = payload["AverageMaxOccupancy"]

    room_params = RoomParams(
        height=height,
        width=width,
        length=length,
        max_occupancy=max_occupancy,
        volume=volume,
    )

    return (location_id, room_params)

def multi_room_json(path: PathLike) -> dict[str, RoomParams]:
    """Load multiple room metadata entries from a JSON file.

    This helper reads a JSON file containing an array of room and location
    metadata objects, validates each entry, and returns a dictionary mapping
    `LocationID` to constructed `RoomParams` objects.
    """
    json_path = Path(path)
    if not json_path.exists():
        raise FileNotFoundError(f"JSON file not found: {json_path}")

    raw_text = json_path.read_text(encoding="utf-8")
    if not raw_text.strip():
        raise ValueError(f"JSON file is empty: {json_path}")

    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Failed to parse JSON file {json_path}: {exc.msg}"
        ) from exc

    if not isinstance(payload, list):
        raise ValueError("Expected top-level JSON structure to be an array.")

    result: dict[str, RoomParams] = {}
    for entry in payload:
        if not isinstance(entry, dict):
            raise ValueError("Each entry in the array must be an object.")
        # Parse the in-memory JSON object using the shared helper
        location_id, room_params = _parse_room_payload(entry)
        result[location_id] = room_params

    return result