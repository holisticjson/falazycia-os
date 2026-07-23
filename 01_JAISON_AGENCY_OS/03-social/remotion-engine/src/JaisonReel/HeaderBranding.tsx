import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

export const HeaderBranding: React.FC<{
  authorName: string;
  authorHandle: string;
  motto: string;
  primaryColor: string;
}> = ({ authorName, authorHandle, motto, primaryColor }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const slideDown = spring({
    frame,
    fps,
    config: { damping: 12 },
  });

  const opacity = spring({
    frame,
    fps,
    config: { damping: 20 },
  });

  return (
    <div
      style={{
        position: "absolute",
        top: "60px",
        left: "50%",
        transform: `translateX(-50%) translateY(${(-1 + slideDown) * 40}px)`,
        opacity,
        width: "90%",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "16px 24px",
        backgroundColor: "rgba(17, 24, 39, 0.75)",
        backdropFilter: "blur(16px)",
        WebkitBackdropFilter: "blur(16px)",
        border: "1px solid rgba(255, 255, 255, 0.12)",
        borderRadius: "20px",
        boxShadow: `0 8px 32px 0 rgba(0, 0, 0, 0.37), 0 0 15px ${primaryColor}33`,
        zIndex: 10,
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: "14px" }}>
        {/* Animated Cyber Icon Badge */}
        <div
          style={{
            width: "48px",
            height: "48px",
            borderRadius: "14px",
            background: `linear-gradient(135deg, ${primaryColor}, #3B82F6)`,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "#FFFFFF",
            fontWeight: "bold",
            fontSize: "24px",
            boxShadow: `0 0 12px ${primaryColor}`,
          }}
        >
          J
        </div>
        <div>
          <div
            style={{
              color: "#F8FAFC",
              fontSize: "20px",
              fontWeight: 700,
              letterSpacing: "0.5px",
              fontFamily: "system-ui, -apple-system, sans-serif",
            }}
          >
            {authorName}
          </div>
          <div
            style={{
              color: primaryColor,
              fontSize: "15px",
              fontWeight: 600,
              fontFamily: "monospace",
            }}
          >
            {authorHandle}
          </div>
        </div>
      </div>

      <div
        style={{
          color: "#94A3B8",
          fontSize: "13px",
          fontWeight: 500,
          textAlign: "right",
          maxWidth: "220px",
          fontStyle: "italic",
          lineHeight: "1.2",
          fontFamily: "system-ui, -apple-system, sans-serif",
        }}
      >
        "{motto}"
      </div>
    </div>
  );
};
