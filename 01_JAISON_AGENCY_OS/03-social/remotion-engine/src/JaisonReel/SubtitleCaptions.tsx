import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const SubtitleCaptions: React.FC<{
  captions: Array<{ word: string; startFrame: number; endFrame: number }>;
  primaryColor: string;
}> = ({ captions, primaryColor }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Find active word at current frame
  const activeCaption = captions.find(
    (c) => frame >= c.startFrame && frame <= c.endFrame
  );

  if (!activeCaption) return null;

  const wordProgress = frame - activeCaption.startFrame;

  const scale = spring({
    frame: wordProgress,
    fps,
    config: { damping: 12, stiffness: 200 },
  });

  const opacity = interpolate(wordProgress, [0, 4], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        top: "700px",
        left: "50%",
        transform: `translateX(-50%) scale(${scale})`,
        opacity,
        zIndex: 20,
        textAlign: "center",
        width: "90%",
      }}
    >
      <div
        style={{
          display: "inline-block",
          padding: "20px 36px",
          backgroundColor: "rgba(11, 15, 23, 0.92)",
          backdropFilter: "blur(12px)",
          borderRadius: "24px",
          border: `3px solid ${primaryColor}`,
          boxShadow: `0 0 40px ${primaryColor}88, 0 10px 30px rgba(0,0,0,0.8)`,
        }}
      >
        <span
          style={{
            color: "#FFFFFF",
            fontSize: "52px",
            fontWeight: 900,
            letterSpacing: "1px",
            textTransform: "uppercase",
            fontFamily: "system-ui, -apple-system, sans-serif",
            textShadow: `0 0 20px ${primaryColor}`,
          }}
        >
          {activeCaption.word}
        </span>
      </div>
    </div>
  );
};
