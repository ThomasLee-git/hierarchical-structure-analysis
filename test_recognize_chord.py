from pathlib import Path
import sys
import numpy as np

sys.path.append(
    "/home/thomas/git/github/hierarchical-structure-analysis/preprocessing/exported_midi_chord_recognition"
)
from preprocessing.exported_midi_chord_recognition.main import (
    ChordRecognition,
    ChordClass,
    DataEntry,
    MidiBeatExtractor,
    ChordLabIO,
    io,
    # process_chord,
    midi_to_thickness_and_bass_weights,
)
import music21


def filter_tab(midi_path: Path):
    valid_num_parts = 2
    valid_time_signature = (4, 4)
    num_time_signatures_per_part = 1
    score = music21.converter.parse(midi_path)
    num_parts = len(score.parts)
    assert (
        num_parts == valid_num_parts
    ), f"invalid {num_parts=}, expected {valid_num_parts}"
    for part_idx in range(num_parts):
        curr_part = score.parts[part_idx]
        part_ts_list = curr_part.getTimeSignatures()
        assert (
            len(part_ts_list) == num_time_signatures_per_part
        ), f"got {len(part_ts_list)} time signatures, expected {num_time_signatures_per_part}"
        part_ts = (part_ts_list[0].beatCount, part_ts_list[0].denominator)
        assert (
            part_ts == valid_time_signature
        ), f"invalid time signature {part_ts}, expected {valid_time_signature}"
    return score


def get_chords(
    midi_entry,
):
    rec = ChordRecognition(midi_entry, ChordClass())
    # weights = midi_to_thickness_and_bass_weights(midi_entry.midi)
    # reset weights to [0, 1]
    weights = np.array([0, 1.0])
    rec.process_feature(weights)
    chord = rec.decode()
    return chord


def insert_chords_into_score(score, chord_list):
    def insert_virt_note(bar_list, chord_name, bar_idx, beat_idx):
        if bar_idx >= len(bar_list):
            print(f"out of range, skip")
            return
        tmp_n = music21.note.Note()
        tmp_n.addLyric(chord_name)
        bar_list[bar_idx].insert(beat_idx, tmp_n)

    def get_duration(start, end):
        num_beats_per_bar = 4
        s_bar_idx, s_beat_idx = start
        e_bar_idx, e_beat_idx = end
        duration = (
            (e_bar_idx - s_bar_idx) * num_beats_per_bar + e_beat_idx - s_beat_idx + 1
        )
        return duration

    # get num_bars
    part0 = score.parts[0]
    bar_list = part0.getElementsByClass(music21.stream.Measure)
    num_bars = len(bar_list)
    # insert into new part
    part = music21.stream.Part(id="chord")
    # insert Chord
    for idx, chord_tuple in enumerate(chord_list):
        start, end, chord = chord_tuple
        s_bar_idx, s_beat_idx = start
        if s_bar_idx >= num_bars:
            print(f"{s_bar_idx=} out of range {num_bars=}, skip")
            continue
        beat_duration = get_duration(start, end)
        tmp_note = music21.note.Note()
        tmp_note.duration.quarterLength = beat_duration
        tmp_note.addLyric(chord)
        part.append(tmp_note)
    # add part
    score.append(part)
    return score


def process(midi_path: Path, output_path: Path):
    try:
        score = filter_tab(midi_path)
    except Exception as e:
        print(f"failed validating {midi_path.as_posix()}: {str(e)}")
        return
    entry = DataEntry()
    entry.append_file(midi_path.as_posix(), io.MidiIO, "midi")
    entry.append_extractor(MidiBeatExtractor, "beat")
    chord_list = get_chords(entry)
    score = insert_chords_into_score(score, chord_list)
    score.write(fmt="musicxml", fp=output_path)


def test():
    midi_root = Path("/tmp/thomas_ramdisk/everyone_piano_20221027/everyone_piano")
    musicxml_root = Path("/tmp/thomas_ramdisk/everyone_piano_musicxml")
    for f in midi_root.iterdir():
        if f.is_file() and f.suffix == ".mid":
            output_path = musicxml_root.joinpath(f.stem)
            try:
                process(f, output_path)
            except Exception as e:
                print(f"exception: {f.stem} {str(e)}")


if __name__ == "__main__":
    test()
