import { useState, useEffect, useRef } from "react";
import Comment from "../components/Comment";
import "./Galery.css";
import images from "../data/images.json";

function Galery() {
  const [image, setImage] = useState();
  const comment = useRef();
  const [comments, setComments] = useState([
    {
      id: 1,
      author: "bob@amazon.com",
      text: "This is awesome",
    },
    {
      id: 2,
      author: "alice@amazon.com",
      text: "This is better than awesome",
    },
  ]);

  useEffect(() => {
    setImage(images[0]);
  }, []);

  useEffect(() => {
    console.log("Loading comments");
  }, [image]);

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

  function addComment(e) {
    e.preventDefault();
    setComments((current) => {
      const newComments = [
        {
          id: 1,
          author: "me",
          text: comment.current.value,
        },
        ...current,
      ];
      console.log(newComments);
      return newComments;
    });
  }

  return (
    <div className="galery">
      <h1>{image?.title}</h1>
      <h3>&copy;{image?.author}</h3>
      <div className="image-box">
        <button onClick={() => previousImage(image)}>&lt;</button>
        <img className="image" src={image?.url}></img>
        <button onClick={() => nextImage(image)}>&gt;</button>
      </div>

      <form action="" className="comment-form">
        <strong>Your comment:</strong>
        <textarea rows="4" ref={comment}></textarea>
        <button onClick={addComment}>Submit</button>
      </form>

      <div className="comments">
        <h3>Comments:</h3>
        {comments.map((c) => (
          <Comment key={c.id} comment={c} />
        ))}
      </div>
    </div>
  );
}

export default Galery;
