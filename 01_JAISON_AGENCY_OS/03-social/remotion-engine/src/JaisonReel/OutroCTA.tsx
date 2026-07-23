import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const OutroCTA: React.FC<{
  primaryColor: string;
}> = ({ primaryColor }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Outro starts 120 frames before video ends (last 4 seconds)
  const outroStartFrame = durationInFrames - 120;

  if (frame < outroStartFrame) return null;

  const localFrame = frame - outroStartFrame;

  const opacity = interpolate(localFrame, [0, 15], [0, 1], {
    extrapolateRight: "clamp",
  });

  const scale = spring({
    frame: localFrame,
    fps,
    config: { damping: 12, stiffness: 120 },
  });

  return (
    <div
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        backgroundColor: "rgba(11, 15, 23, 0.95)",
        backdropFilter: "blur(25px)",
        opacity,
        zIndex: 30,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "40px",
        textAlign: "center",
        gap: "24px",
      }}
    >
      <div
        style={{
          transform: `scale(${scale})`,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: "24px",
        }}
      >
        {/* Animated Cyber Badge */}
        <div
          style={{
            width: "100px",
            height: "100px",
            borderRadius: "30px",
            background: `linear-gradient(135deg, ${primaryColor}, #3B82F6)`,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "#FFFFFF",
            fontWeight: 900,
            fontSize: "48px",
            boxShadow: `0 0 40px ${primaryColor}`,
          }}
        >
          J
        </div>

        <h2
          style={{
            color: "#FFFFFF",
            fontSize: "48px",
            fontWeight: 900,
            lineHeight: "1.2",
            margin: 0,
            fontFamily: "system-ui, -apple-system, sans-serif",
          }}
        >
          Pobierz poradnik <br />
          <span style={{ color: primaryColor }}>"Zewnętrzny Mózg"</span>
        </h2>

        <p
          style={{
            color: "#94A3B8",
            fontSize: "24px",
            fontWeight: 500,
            margin: 0,
            maxWidth: "80%",
            fontFamily: "system-ui, -apple-system, sans-serif",
          }}
        >
          Skomentuj słowem <strong style={{ color: "#FFFFFF" }}>"MÓZG"</strong> pod postem lub wejdź na:
        </p>

        {/* Website Button CTA */}
        <div
          style={{
            backgroundColor: primaryColor,
            color: "#090D16",
            padding: "20px 40px",
            borderRadius: "40px",
            fontWeight: 900,
            fontSize: "28px",
            letterSpacing: "1px",
            boxShadow: `0 0 30px ${primaryColor}`,
            fontFamily: "monospace",
          }}
        >
          go.jaison.pl
        </div>
      </div>
    </div>
  );
};
