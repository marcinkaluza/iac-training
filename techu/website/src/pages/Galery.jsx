import { useState, useEffect, useRef } from "react";

import "./Galery.css";
import images from "../data/images.json";
import Comments from "../components/Comments";

function Galery() {
  const [image, setImage] = useState();

  useEffect(() => {
    setImage(images[0]);
  }, []);

  const nextImage = (image) => {
    let imageIndex = images.indexOf(image);

    if (imageIndex === images.length - 1) {
      imageIndex = 0;
    } else {
      imageIndex++;
    }

    setImage(images[imageIndex]);
  };

  const previousImage = (image) => {
    let imageIndex = images.indexOf(image);

    if (imageIndex === 0) {
      imageIndex = images.length - 1;
    } else {
      imageIndex--;
    }

    setImage(images[imageIndex]);
  };

  return (
    <div className="galery container">
      <h1>{image?.title}</h1>
      <h3>&copy;{image?.author}</h3>
      <div className="image-box">
        <img className="image" src={image?.url}></img>
        <div className="button-bar">
          <button onClick={() => previousImage(image)}>&lt;</button>
          <button onClick={() => nextImage(image)}>&gt;</button>
        </div>
      </div>
      <Comments imageId={image?.id} />
    </div>
  );
}

export default Galery;
