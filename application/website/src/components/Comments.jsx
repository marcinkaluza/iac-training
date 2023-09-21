import { useState, useEffect, useRef } from "react";
import Comment from "./Comment";

function Comments({ user, imageId }) {
  const comment = useRef();
  const [comments, setComments] = useState([]);

  useEffect(() => {
    const load = async () => {
      const response = await fetch(`/api/comments?imageId=${imageId}`, {
        headers: {
          accepts: "application/json",
        },
      });
      const data = await response.json();
      setComments(data);
    };

    if (imageId) load();
  }, [imageId]);

  async function addComment(e) {
    e.preventDefault();

    const response = await fetch("/api/comments", {
      method: "POST",
      headers: {
        accepts: "application/json",
        "Content-Type": "application/json",
        authorization: `Bearer ${user.signInUserSession.idToken.jwtToken}`,
      },
      body: JSON.stringify({
        imageId: imageId,
        text: comment.current.value,
      }),
    });

    const newComment = await response.json();

    comment.current.value = "";

    setComments((current) => {
      const newComments = [newComment, ...current];
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
          <Comment key={c.commentId} comment={c} />
        ))}
      </div>
    </>
  );
}

export default Comments;
