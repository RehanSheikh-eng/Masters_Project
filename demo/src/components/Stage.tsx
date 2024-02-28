import React from "react";
import Tool from "./Tool";
import { useSAMModel } from "./hooks/useSAMModel";

const Stage = () => {
  const { handleMouseMove } = useSAMModel();

  const flexCenterClasses = "flex items-center justify-center";

  return (
    <div className={`${flexCenterClasses} w-full h-full`}>
      <div className={`${flexCenterClasses} relative w-[90%] h-[90%]`}>
        <Tool handleMouseMove={handleMouseMove}/>
      </div>
    </div>
  );
};

export default Stage;
