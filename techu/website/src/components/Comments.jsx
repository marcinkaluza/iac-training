import { useState, useEffect, useRef } from "react";
import Comment from "./Comment";

function Comments({ imageId }) {
  const comment = useRef();
  const [comments, setComments] = useState([]);

  useEffect(() => {
    const loader = async () => {
      const response = await fetch(`/api/comments/imageId=${imageId}`, {
        headers: {
          accepts: "application/json",
        },
      });
      const data = await response.json();
      setComments(data);
    };

    loader();
  }, [imageId]);

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
    <>
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
    </>
  );
}

export default Comments;
