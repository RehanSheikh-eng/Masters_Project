import React, { createContext, useContext, useState, ReactNode, useEffect } from 'react';
import { InferenceSession, Tensor } from 'onnxruntime-web';
import { handleImageScale } from '../components/helpers/scaleHelper';
import { modelScaleProps, modelInputProps } from '../components/helpers/Interfaces';
import { onnxMaskToImage } from '../components/helpers/maskUtils';
import { modelData } from '../components/helpers/onnxModelAPI';
const ort = require("onnxruntime-web");  
/* @ts-ignore */
import npyjs from "npyjs";

// Define paths as constants or import them from a configuration file
const MODEL_DIR = '/model/sam_onnx_quantized_example.onnx';
const IMAGE_PATH = '/assets/data/homerton.jpg';
const IMAGE_EMBEDDING = '/assets/data/homerton_embedding.npy';

// Define the context shape
interface ImageProcessingContextType {
  image: HTMLImageElement | null;
  setImage: (image: HTMLImageElement | null) => void;
  maskImg: HTMLImageElement | null;
  setMaskImg: (maskImg: HTMLImageElement | null) => void;
  clicks: modelInputProps[] | null;
  setClicks: (clicks: modelInputProps[]) => void;
  runOnnxModel: () => Promise<void>;
}

// Create context with an undefined default value, to be initialized within a provider
export const ImageProcessingContext = createContext<ImageProcessingContextType | undefined>(undefined);

// Context Provider Component
export const ImageProcessingProvider = ({ children }: { children: ReactNode }) => {
  const [image, setImage] = useState<HTMLImageElement | null>(null);
  const [maskImg, setMaskImg] = useState<HTMLImageElement | null>(null);
  const [model, setModel] = useState<InferenceSession | null>(null);
  const [tensor, setTensor] = useState<Tensor | null>(null);
  const [modelScale, setModelScale] = useState<modelScaleProps | null>(null);
  const [clicks, setClicks] = useState<Array<modelInputProps> | null>(null);

  // Load the model, image, and image embedding
  useEffect(() => {
    // Initialize model, load image and embedding logic here
    const initModel = async () => {
        try {
          if (MODEL_DIR === undefined) return;
          const URL: string = MODEL_DIR;
          const model = await InferenceSession.create(URL);
          setModel(model);
        } catch (e) {
          console.log(e);
        }
      };
      initModel();

    // Load the image
    const url = new URL(IMAGE_PATH, location.origin);
    loadImage(url);

    // Load the Segment Anything pre-computed embedding
    Promise.resolve(loadNpyTensor(IMAGE_EMBEDDING, "float32")).then(
      (embedding) => setTensor(embedding)
    );

  }, []);

  const runOnnxModel = async () => {
    try {
      if (
        model === null ||
        clicks === null ||
        tensor === null ||
        modelScale === null
      )
        return;
      else {
        // Preapre the model input in the correct format for SAM. 
        // The modelData function is from onnxModelAPI.tsx.
        const feeds = modelData({
          clicks,
          tensor,
          modelScale,
        });
        if (feeds === undefined) return;
        // Run the SAM ONNX model with the feeds returned from modelData()
        const results = await model.run(feeds);
        const output = results[model.outputNames[0]];
        // The predicted mask returned from the ONNX model is an array which is 
        // rendered as an HTML image using onnxMaskToImage() from maskUtils.tsx.
        setMaskImg(onnxMaskToImage(output.data, output.dims[2], output.dims[3]));
      }
    } catch (e) {
      console.log(e);
    }
  };

  useEffect(() => {
      runOnnxModel();
  }, [clicks]);
  
  /**
   * Loads an image from the given URL and sets the model scale based on the dimensions of the loaded image.
   *
   * @param {URL} url - The URL of the image to be loaded
   * @return {void} 
   */
  const loadImage = async (url: URL) => {
    try {
      const img = new Image();
      img.src = url.href;
      img.onload = () => {
        const { height, width, samScale } = handleImageScale(img);
        setModelScale({
          height: height,  // original image height
          width: width,  // original image width
          samScale: samScale, // scaling factor for image which has been resized to longest side 1024
        });
        img.width = width; 
        img.height = height; 
        setImage(img);
      };
    } catch (error) {
      console.log(error);
    }
  };
  
  /**
   * Loads a NPY tensor from the specified file and returns it as a Tensor object.
   *
   * @param {string} tensorFile - the file path of the NPY tensor
   * @param {string} dType - the data type of the tensor
   * @return {Tensor} the loaded NPY tensor as a Tensor object
   */
  const loadNpyTensor = async (tensorFile: string, dType: string) => {
    let npLoader = new npyjs();
    const npArray = await npLoader.load(tensorFile);
    const tensor = new ort.Tensor(dType, npArray.data, npArray.shape);
    return tensor;
  };

  // Provide state and helper functions through context
  const value = {
    image,
    setImage,
    maskImg,
    setMaskImg,
    clicks,
    setClicks,
    runOnnxModel,
  };

  return (
    <ImageProcessingContext.Provider value={value}>
      {children}
    </ImageProcessingContext.Provider>
  );
};

// Custom hook to use the context
export const useImageProcessing = () => {
  const context = useContext(ImageProcessingContext);
  if (context === undefined) {
    throw new Error('useImageProcessing must be used within an ImageProcessingProvider');
  }
  return context;
};
