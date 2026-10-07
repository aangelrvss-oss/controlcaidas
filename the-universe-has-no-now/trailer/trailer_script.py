"""Trailer: a 45-second standalone piece. Own narration lines, own cut, same scenes."""
def L(text, pause=0.5): return {"text": text, "pause": pause}
SHOTS = [
 dict(id="T01", act=1, scene="card", params=dict(text="Imagine two events happening\nat exactly the same time.", style="quote"), min_dur=3.6, lead=0, tail=0, lines=[], trans="dip:0.6"),
 dict(id="T02", act=1, scene="two_clocks", params=dict(mode="sync"), min_dur=3.2, lead=0.2, tail=0.2, lines=[L("Two clocks. One moment.", 0.3)], trans="cut", sfx={0.0: "tick_loop"}),
 dict(id="T03", act=1, scene="ship_flash", params=dict(frame="platform"), min_dur=3.6, lead=0.1, tail=0.1, lines=[L("The simplest idea in the world.", 0.3)], trans="cut", sfx={3.0: "flash"}),
 dict(id="T04", act=2, scene="minkowski", params=dict(phase="boost"), min_dur=3.4, lead=0.2, tail=0.1, lines=[L("It is not true.", 0.5)], trans="cut", sfx={0.5: "whoosh_soft"}),
 dict(id="T05", act=3, scene="scale", params=dict(stage="galaxy"), min_dur=3.4, lead=0.1, tail=0.1, lines=[L("Light sets the rules.", 0.4)], trans="cut", sfx={0.2: "pulse_hi"}),
 dict(id="T06", act=4, scene="lensing", params=dict(), min_dur=3.2, lead=0.1, tail=0.1, lines=[L("Gravity bends the stage.", 0.4)], trans="cut"),
 dict(id="T07", act=5, scene="blackhole", params=dict(phase="doppler"), min_dur=4.6, lead=0.4, tail=0.2, lines=[L("This black hole is computed, not painted.", 0.5)], trans="cut", sfx={0.0: "drone_in"}),
 dict(id="T08", act=6, scene="double_slit", params=dict(), min_dur=3.6, lead=0.1, tail=0.1, lines=[L("At the smallest scales, reality is made of probabilities.", 0.3)], trans="cut", sfx={0.0: "detector"}),
 dict(id="T09", act=7, scene="entangle", params=dict(phase="nosignal"), min_dur=3.4, lead=0.1, tail=0.1, lines=[L("Correlated across the solar system. No message sent.", 0.3)], trans="cut"),
 dict(id="T10", act=8, scene="split", params=dict(phase="clash"), min_dur=5.0, lead=0.2, tail=0.2, lines=[L("Two theories. Both confirmed beyond doubt.", 0.3), L("They do not fit together.", 0.6)], trans="dip:0.8", sfx={3.5: "sub_drop"}),
 dict(id="T11", act=10, scene="final_zoom", params=dict(), min_dur=4.5, lead=0.3, tail=0.2, lines=[L("The universe keeps no single time for anyone.", 0.4)], trans="dip:0.8", sfx={0.0: "whoosh_long"}),
 dict(id="T12", act=10, scene="card", params=dict(text="THE UNIVERSE HAS NO NOW", style="act", act_no="A SCIENCE FILM"), min_dur=4.5, lead=0, tail=0, lines=[], trans="cut"),
]
