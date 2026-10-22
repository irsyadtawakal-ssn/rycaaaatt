import React from "react";
import { Composition } from "remotion";
import { Video, Timeline } from "./Video";

const empty: Timeline = {
  fps: 30, lebar: 1080, tinggi: 1920, durasi: 1, video: "potong.mp4", handle: "@irsyadtawakal",
  input_bar: [], caption: [], kartu_angka: [], contekan: null, zoom: [], objek: [], sfx: [],
};

export const Root: React.FC = () => (
  <Composition
    id="Video"
    component={Video}
    fps={30}
    width={1080}
    height={1920}
    durationInFrames={30}
    defaultProps={empty}
    calculateMetadata={({ props }) => ({
      fps: props.fps,
      width: props.lebar,
      height: props.tinggi,
      durationInFrames: Math.max(1, Math.round(props.durasi * props.fps)),
    })}
  />
);
