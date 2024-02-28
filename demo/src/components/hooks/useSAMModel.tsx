import { useContext, useCallback } from 'react';
import { ImageProcessingContext } from '../../context/ImageProcessingContext';
import * as _ from 'underscore';

export const useSAMModel = () => {
  const { setClicks, image } = useContext(ImageProcessingContext)!;

  // Converts screen coordinates to image coordinates and updates clicks
  const handleMouseMove = useCallback(_.throttle((event: MouseEvent) => {
    if (!image) return;

    const target = event.target as HTMLElement;
    const rect = target.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    const imageScale = image.width / target.offsetWidth;

    const scaledX = x * imageScale;
    const scaledY = y * imageScale;

    const newClick = { x: scaledX, y: scaledY, clickType: 1 };

    if (newClick) setClicks([newClick]);
  }, 15), [image, setClicks]);

  return { handleMouseMove };
};
