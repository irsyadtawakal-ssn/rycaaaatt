// Same composition as lib/video/hf.py, in React. Both read timeline.json and
// share captions.css + komposisi.css, so the two renders should match frame
// for frame. Times in the timeline are seconds; frame = round(seconds * fps).
import React, { useEffect, useState } from "react";
import {
  Audio, Img, OffthreadVideo, Sequence, cancelRender, continueRender, delayRender,
  staticFile, useCurrentFrame,
} from "remotion";
import "../captions.css";
import "../komposisi.css";

type Part = { t: string; kw: boolean };
type Span = { mulai: number; selesai: number };
export type Timeline = {
  fps: number; lebar: number; tinggi: number; durasi: number; video: string; handle: string;
  input_bar: (Span & { kosong: boolean; ketik: boolean; kata: Part[] })[];
  caption: (Span & { kata: Part[] })[];
  kartu_angka: (Span & { angka: string; label: string; sumber: string })[];
  contekan: (Span & { judul: string; poin: string[] }) | null;
  zoom: (Span & { skala: number })[];
  objek: (Span & { gambar: string })[];
  sfx: { src: string; mulai: number; durasi: number; volume: number }[];
};

const FONTS = ['700 66px "Figtree"', '500 34px "Figtree"', '800 100px "Bricolage Grotesque"', 'italic 64px "Instrument Serif"'];

// tail (the caret) is glued to the last word so it never drops to its own line.
const Words: React.FC<{ parts: Part[]; chars?: number; tail?: React.ReactNode }> = ({ parts, chars, tail }) => {
  let left = chars ?? Infinity;
  if (!parts.length) return <>{tail}</>;
  return (
    <>
      {parts.map((p, i) => {
        const shown = p.t.slice(0, Math.max(0, left));
        left -= p.t.length;
        const hidden = p.t.slice(shown.length);
        const text = (
          <>
            {shown}
            {hidden && <span style={{ visibility: "hidden" }}>{hidden}</span>}
          </>
        );
        const word = p.kw ? <span className="kw">{text}</span> : text;
        return (
          <React.Fragment key={i}>
            {i > 0 && " "}
            {tail && i === parts.length - 1 ? <span style={{ whiteSpace: "nowrap" }}>{word}{tail}</span> : word}
          </React.Fragment>
        );
      })}
    </>
  );
};

export const Video: React.FC<Timeline> = (tl) => {
  const frame = useCurrentFrame();
  const t = frame / tl.fps;
  // Same frame boundaries as HyperFrames: a clip is visible from its start
  // frame up to (not including) its end frame.
  const on = (s: Span) => frame >= Math.round(s.mulai * tl.fps) && frame < Math.round(s.selesai * tl.fps);

  const [handle] = useState(() => delayRender("fonts"));
  useEffect(() => {
    Promise.all(FONTS.map((f) => document.fonts.load(f)))
      .then(() => continueRender(handle))
      .catch((e) => cancelRender(e));
  }, [handle]);

  const zoom = tl.zoom.find(on);

  return (
    <div className="frame">
      <div className="video-wrap" style={{ transform: `scale(${zoom ? zoom.skala : 1})` }}>
        <OffthreadVideo src={staticFile(tl.video)} />
      </div>

      <div className="zone-atas">
        {tl.objek.filter(on).map((o, i) => (
          <div className="objek" key={i}>
            <Img src={staticFile(o.gambar)} />
          </div>
        ))}
      </div>

      {tl.input_bar.filter(on).map((b, i) => {
        const since = t - b.mulai;
        const caretOn = since < 0.5 || Math.floor((since - 0.5) / 0.5) % 2 === 1;
        const total = b.kata.reduce((n, p) => n + p.t.length, 0);
        const chars = b.ketik ? Math.floor((since / 1.5) * total) + 1 : undefined;
        return (
          <div className={b.kosong ? "input-bar is-empty" : "input-bar"} key={i}>
            <Words parts={b.kata} chars={chars} tail={<span className="caret" style={{ opacity: caretOn ? 1 : 0 }} />} />
          </div>
        );
      })}

      {tl.caption.filter(on).map((c, i) => (
        <div className="cap" key={i}>
          <Words parts={c.kata} />
        </div>
      ))}

      {tl.kartu_angka.filter(on).map((k, i) => (
        <div className="card-angka" key={i}>
          <div className="angka">{k.angka}</div>
          <div className="label">{k.label}</div>
          {k.sumber && <div className="sumber">{k.sumber}</div>}
        </div>
      ))}

      {tl.contekan && on(tl.contekan) && (
        <div className="contekan">
          <div className="judul">{tl.contekan.judul}</div>
          <ol>
            {tl.contekan.poin.map((p, i) => <li key={i}>{p}</li>)}
          </ol>
        </div>
      )}

      {tl.sfx.map((s, i) => (
        <Sequence key={i} from={Math.round(s.mulai * tl.fps)} durationInFrames={Math.max(1, Math.round(s.durasi * tl.fps))}>
          <Audio src={staticFile(s.src)} volume={s.volume} />
        </Sequence>
      ))}

      <div className="handle">{tl.handle}</div>
    </div>
  );
};
