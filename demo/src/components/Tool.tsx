import React, { useContext, useEffect, useState } from "react";
import { ImageProcessingContext } from "../context/ImageProcessingContext"; // Updated import
import { ToolProps } from "./helpers/Interfaces";
import * as _ from "underscore";

const Tool = ({ handleMouseMove }: ToolProps) => {
  const { image, maskImg, setMaskImg } = useContext(ImageProcessingContext)!; // Updated to use ImageProcessingContext

  const [shouldFitToWidth, setShouldFitToWidth] = useState(true);
  const bodyEl = document.body;

  const fitToPage = () => {
    if (!image) return;
    const imageAspectRatio = image.width / image.height;
    const screenAspectRatio = window.innerWidth / window.innerHeight;
    setShouldFitToWidth(imageAspectRatio > screenAspectRatio);
  };

  const resizeObserver = new ResizeObserver((entries) => {
    for (const entry of entries) {
      if (entry.target === bodyEl) {
        fitToPage();
      }
    }
  });

  useEffect(() => {
    fitToPage();
    resizeObserver.observe(bodyEl);
    return () => resizeObserver.unobserve(bodyEl);
  }, [image]);

  const imageClasses = "max-w-full max-h-full"; // Adjusted classes for responsiveness
  const maskImageClasses = "absolute opacity-40 pointer-events-none top-0 left-0"; // Ensure mask aligns properly over the image

  return (
    <>
      {image && (
        <img
          onMouseMove={handleMouseMove}
          onMouseOut={() => _.defer(() => setMaskImg(null))}
          onTouchStart={handleMouseMove}
          src={image.src}
          alt="Interactive Area" // Added alt for accessibility
          className={`${shouldFitToWidth ? "w-full" : "h-full"} ${imageClasses}`}
        />
      )}
      {maskImg && (
        <img
          src={maskImg.src}
          alt="Mask Overlay" // Added alt for accessibility
          className={`${shouldFitToWidth ? "w-full" : "h-full"} ${maskImageClasses}`}
        />
      )}
    </>
  );
};

export default Tool;
