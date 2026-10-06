# THE UNIVERSE HAS NO NOW — reproducible build
PY=python3
export LD_LIBRARY_PATH=/root/lib
.PHONY: all narration timeline audio preview film mux captions trailer shorts thumbnail docs test clean

all: narration timeline audio film captions thumbnail trailer shorts docs test

narration:            ## synthesize every narration line (Kokoro, local)
	$(PY) source/audio/tts.py --speed 0.9
timeline: narration   ## absolute times for every shot and line
	$(PY) source/render/nonow/timeline.py > build/timeline.txt
audio: timeline       ## score, sound design, mix (-14 LUFS)
	cd source/audio && $(PY) music.py && $(PY) sfx_track.py && $(PY) mix.py
captions: timeline
	cd source/audio && $(PY) captions.py
preview: timeline     ## quarter-resolution, 6 fps check render
	cd source/render && $(PY) -m nonow.render film --out ../../build/preview_q.mp4 --scale 0.25 --fps 6 --workers 4 --crf 28
film: timeline        ## full 1080p24 picture + mux
	cd source/render && $(PY) -m nonow.render film --out ../../build/film_video.mp4 --workers 4 --crf 18
	$(PY) source/mux.py
mux:
	$(PY) source/mux.py
trailer:
	$(PY) trailer/build_trailer.py prep
	cd source/render && $(PY) -m nonow.render film --timeline ../../build/trailer_timeline.json --out ../../build/trailer_video.mp4 --workers 4 --crf 18
	$(PY) trailer/build_trailer.py mux
shorts:
	$(PY) source/shorts.py
thumbnail:
	$(PY) source/thumbnail.py
docs:
	$(PY) source/docs_gen.py
test:
	$(PY) -m pytest -q tests
clean:
	rm -rf build/segs build/prev build/*.mp4
