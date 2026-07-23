import React from "react";
import { DynamicHookCard } from "./DynamicHookCard";
import { HeaderBranding } from "./HeaderBranding";
import { NeonBackground } from "./NeonBackground";
import { OutroCTA } from "./OutroCTA";
import { SubtitleCaptions } from "./SubtitleCaptions";
import { JaisonReelProps } from "./types";

export const JaisonReel: React.FC<JaisonReelProps> = ({
  title,
  subtitle,
  hookText,
  authorName,
  authorHandle,
  primaryColor,
  secondaryColor,
  motto,
  captions,
}) => {
  return (
    <div
      style={{
        flex: 1,
        position: "relative",
        width: "1080px",
        height: "1920px",
        backgroundColor: "#0B0F17",
        overflow: "hidden",
      }}
    >
      {/* 1. Animated Neon Background */}
      <NeonBackground primaryColor={primaryColor} secondaryColor={secondaryColor} />

      {/* 2. Glassmorphic Top Branding Header */}
      <HeaderBranding
        authorName={authorName}
        authorHandle={authorHandle}
        motto={motto}
        primaryColor={primaryColor}
      />

      {/* 3. Main Hook Scroll-Stopper Card */}
      <DynamicHookCard
        title={title}
        subtitle={subtitle}
        hookText={hookText}
        primaryColor={primaryColor}
      />

      {/* 4. Word-by-Word Voiceover Captions */}
      <SubtitleCaptions captions={captions} primaryColor={primaryColor} />

      {/* 5. End Outro CTA Screen */}
      <OutroCTA primaryColor={primaryColor} />
    </div>
  );
};
